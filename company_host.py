from App.models import User, EMC, Event, Venue, Venue_Section, Seating, Concert
from App import db, app
from sqlalchemy.exc import *
from decimal import *
import sys, threading, queue, console, concurrent.futures
import payment_gateway as pg

num_workers = 5
q = queue.Queue()

def main():
    
    crud = ("Would you like to (I)nsert (U)pdate (R)ead or (D)elete data? or (Q)uit: ")
    valid = frozenset("iurdq")
    
    submenu = ("Event (M)anagement Company  (E)vents (C)oncerts (V)enues (S)eatings "
            "(Q)uit (B)ack: ")
    subvalid = frozenset("emcvqbs")
    
    call = dict(im=insert_emc, ie=insert_event, ic=insert_concert, iv=insert_venue,
                rm=show_emcs, re=show_events, rc=show_concerts, rv=show_venues,
                um=update_emc, ue=update_event, uc=update_concert, uv=update_venue,
                dm=delete_emc, de=delete_event, dc=delete_concert, dv=delete_venue, 
                rs=show_seatings, us=update_seating,
                b=back, q=quit)
    
    while True:
        action = console.get_menu_choice(crud, valid, submenu, subvalid)
        if action[-1] == 'b':
            action = 'b'
        if action[-1] == 'q'or action[0] == 'q':
            action = 'q'            
        function = call[action]
        function()

#Helpers
def msg_succ():
    print("Operation succeeded!")

def msg_err(body,e):
    print(f"{body}: {e}")

def get_id_list(func, *args):
    return [e.id for e in func(*args)]

#Insert 
def insert_emc():
    res = console.get_data('company', 'name')
    id = db_add(EMC(name = res.name))
    print(f'Data saved! Company {res.name} ID is {id} for you record.')
    
def insert_venue():
    res = console.get_data('venue', 'name', 'address', 'image_url')
    is_feat = console.get_bool("Should the venue be feature? ")
    (ok, id) = db_add(Venue(name = res.name, address = res.address, image_url = res.image_url, featured = is_feat))
    if ok:
        sections = [insert_venue_sec(id) for i in range(console.get_int("Enter the number of sections of this venue: ", 1))]
        db_add_all(sections)
        
        print(f'Data saved! Venue {res.name} ID is {id} for you record.')
    return (ok, id)

def insert_venue_sec(venue_id):
    num_of_seats = console.get_int("Enter the number of seats of this section: ", 1)
    res = console.get_data('section', 'name')
    ven_sec = Venue_Section(num_of_seats = num_of_seats, sec_name = res.name, venue_id = venue_id)
    return ven_sec
 
def insert_event():
    cid = None
    vid = None
    current_emc_id = None
    
    current_emc_id = console.get_int("Please select the EMC (0 to quit): ", 0, valid=get_id_list(show_emcs))
    if current_emc_id == 0:
        return 

    if console.get_bool('Are you making new event for an existing concert? '):
        cid = console.get_int('Please select the concert ID (0 to quit): ', 0, valid=get_id_list(show_concerts))
        if cid == 0:
            return
    else:
        (cok, cid) = insert_concert()
    
        if not cok:
            return (False, None)
        
    if console.get_bool('Is the event held in an existing venue? '):
        vid = console.get_int('Please select the venue ID (0 to quit): ', 0, valid=get_id_list(show_venues))
        if vid == 0:
            return
    else:
        (vok, vid) = insert_venue()
        
        if not vok:
            return (False, None)

    current_sections = show_venue_sec(vid)
    sec_price = {}

    for section in current_sections:
        price = console.get_decimal(f"Please enter the price for section [{section.sec_name}]: ")
        sec_price[section.id] = price
    
    date = console.get_date("Please Enter the date for the event MM-DD-YYYY. Eg. 09-19-2020: ")
    is_feat = console.get_bool("Should the event be feature? ")
    res = console.get_data('event', 'description', 'image_url')
    percentage = console.get_int("Enter the percentage of seats available(0-100)[default:100]: ",0, 100, 100)
    (ok, id) = db_add(Event(date = date, concert_id = cid, venue_id = vid, description = res.description, 
                        image_url = res.image_url, featured = is_feat, 
                        emc_id = current_emc_id, availablePercentage = percentage))
   
    if not ok:
        return (False, None)
    
    seatings = [Seating(price=price, event_id=id, venue_section_id=sec_id) for sec_id, price in sec_price.items()]
    (s_ok, s_id_lst) = db_add_all(seatings)
    
    if s_ok:
        stripe_upload_seatings(s_id_lst)
    
    return(ok, id)

def insert_concert():
    res = console.get_data('concert', 'name', 'artist')
    (ok, id) = db_add(Concert(name = res.name, artist = res.artist))
    if ok:
        print(f'Data saved! Concert {res.name} added! ID is {id} for you record.')
    return (ok, id)

#stripe
def stripe_upload_seating(id):
    with app.app_context():
        try:
            s = Seating.query.filter_by(id=id).first()
            name = f's_{s.id}_e_{s.event_id}_vs_{s.venue_section}'
            price = s.price
            descr = f'{s.event.concert.name} by {s.event.concert.artist} at {s.venue_section.venue.name} on {s.event.date}'
            res = pg.create_prod(name, price, descr)
            s.stripe_prod_id = res["id"]
            s.stripe_prc_id = res["default_price"]
            print(f"Successfully added to stripe products! ID: {res['id']}")
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error uploading to Stripe: {e}")


def stripe_upload_seatings(id_lst):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(stripe_upload_seating, id_lst)

            
#Database query
def db_add_all(data):
    with app.app_context():
        try:
            db.session.add_all(data)
            db.session.flush()
            db.session.commit()
            return (True, [id for id in data.id])
        except Exception as e:
            db.session.rollback()
            msg_err("Error adding all data", e)
            return (False, None)
            
def db_add(data):
    with app.app_context():
        try:
            db.session.add(data)
            db.session.flush()
            db.session.commit()
            return (True, data.id)
        except Exception as e:
            db.session.rollback()
            msg_err("Error adding data", e)
            return (False, None)
        
def db_get_all(obj):
    with app.app_context():
        try:
            return obj.query.all()
        except Exception as e:
            msg_err("Error getting data", e) 
            return None
              
def db_get_instance(obj, id):
    with app.app_context():
        while True:
            try:
                res = obj.query.filter_by(id=id).first()
                return res
            except Exception as e:
                msg_err("Error", e)
                id = console.get_int("Please insert a valid ID: ")

#Read
def show_venue_sec(venue_id):
    with app.app_context():
        try:
            #session has to be open
            venue = Venue.query.filter_by(id=venue_id).first()
            sections = venue.sections
            header = f'{"ID": <5} {"Section Name": <20} {"Number of Seats":<10}'
            sec_list_str = [ f'{e.id: <5} {e.sec_name: <20} {e.num_of_seats:<10}' for e in sections]
            print(header)
            for e in sec_list_str:
                print(f"{e}")
            return sections
        except Exception as e:
            msg_err("Error getting data", e) 
            return None

def show_emcs():
    with app.app_context():
        try:
            emcs = EMC.query.all()
            header = f'{"ID": <5} {"Name": <30} {"Balance":<20}'
            emc_list_str = [ f'{e.id: <5} {e.name: <30} {e.balance:<20}' for e in emcs]
            event_header = f'            {"ID": <5} {"Name": <30} {"Artist":<20} {"Venue":<24} {"Date":<12} {"Description":<30}'
            emc_event_list_str =  [[f'            {e.id: <5} {e.concert.name: <30} {e.concert.artist:<20} {e.venue.name:<24} {str(e.date):<12} {e.description:<30}' for e in emc.events] for emc in emcs]
            for idx, s in enumerate(emc_list_str):
                print("*********************************************")
                print(header)
                print("*********************************************")
                print(f"{s} \n")
                if emc_event_list_str[idx]:
                    print("     Events: ")
                    print(event_header)
                    for e in emc_event_list_str[idx]:
                        print(f"{e}")
                    print("\n")
            return emcs
        except Exception as e:
            msg_err("Error getting data", e) 
            return None    

def show_events(emc_id=None):
    with app.app_context():
        try:
            events = Event.query.all() if emc_id is None else Event.query.filter_by(emc_id=emc_id).all()
            header = f'{"ID": <5} {"Name": <30} {"Artist":<20} {"Venue":<24} {"Date":<12} {"Description":<30}'
            event_list_str = [ f'{e.id: <5} {e.concert.name: <30} {e.concert.artist:<20} {e.venue.name:<24} {str(e.date):<12} {e.description:<30}' for e in events]
            print(header)
            for s in event_list_str:
                print(f"{s} \n")
            return events
        except Exception as e:
            msg_err("Error getting data", e) 
            return None    
        
def show_concerts():
    header = f'{"ID": <5} {"Name": <30} {"Artist":<20}'
    concerts = db_get_all(Concert)
    concert_list = [ f'{str(c.id):<5} {c.name:<30} {c.artist:<20}' for c in concerts]
    print(header)
    for s in concert_list:
        print(f"{s}")
    return concerts

def show_seatings(event_id=None):
    with app.app_context():
        try:
            if event_id is None:
                event_id = console.get_int("Please enter the event ID (0 to quit): ", 0, valid=get_id_list(show_events))
                if event_id == 0:
                   return
            seatings = Seating.query.filter_by(event_id = event_id)
            print("*****************************************************")
            print(f"Event: {seatings[0].event.concert.name}  Date: {seatings[0].event.date}")
            print("*****************************************************")
            header = f'{"ID": <5} {"Section":<20} {"Price":<10} {"Seats Sold":<10}'  
            seating_list_str = [ f'{str(s.id):<5} {s.venue_section.sec_name:<20} {str(s.price):<10} {s.seats_sold:<10}  ' for s in seatings]
            print(header)
            for s in seating_list_str:
                print(f"{s}")
            return seatings
        except Exception as e:
            msg_err("Error", e)
            return None
            
def show_venues():
    with app.app_context():
        try:
            venues = Venue.query.all()
            header = f'{"ID": <5} {"Name": <24} {"Address":<30} {"Sections":<60} {"#Seats":<48}'  
            venue_list_str = [ f'{str(v.id):<5} {v.name:<24} {v.address:<30} {"/".join([ s.sec_name for s in v.sections]):<60} {"/".join([ str(s.num_of_seats) for s in v.sections]):<48}' for v in venues]
            print(header)
            for s in venue_list_str:
                print(f"{s}")
            return venues
        except Exception as e:
            msg_err("Error getting data", e) 
            return None    

#Uppdate
def update_emc():
    with app.app_context():
        try:
            emc_id = console.get_int("Please enter the EMC ID (0 to quit): ", 0, valid = get_id_list(show_emcs))
            if emc_id == 0:
                return
            emc = EMC.query.filter_by(id=emc_id).first()
            res = console.update_data(name=(emc.name, str), balance=(emc.balance, Decimal))
            emc.name = res["name"]
            emc.balance = res["balance"]
            db.session.commit()
            msg_succ()
        except Exception as e:
            msg_err("Error updating EMC data", e)
            db.session.rollback()
    
def update_event():
    with app.app_context():
        try:
            emc_id = console.get_int("Please enter the EMC ID (0 to quit): ", 0, valid = get_id_list(show_emcs))
            if emc_id == 0:
                return
            eids = get_id_list(show_events, emc_id)
            if len(eids) > 0:
                event_id = console.get_int("Please enter the event ID (0 to quit): ", 0, valid = eids)
                event = Event.query.filter_by(id=event_id).first()
                new_date = console.get_date("Enter new date (press 'Enter' to skip): ", event.date)
                res = console.update_data(venue_id=(event.venue_id, int), description=(event.description, str), availablePercentage=(event.availablePercentage, int),
                                          image_url=(event.image_url, str))
                featured = console.get_bool("Featured event? [Y/N] (press 'Enter' to skip): ", event.featured)

                event.venue_id = res["venue_id"]
                event.description = res["description"]
                event.date = new_date
                event.featured = featured
                event.availablePercentage = res["availablePercentage"]
                event.image_url = res["image_url"]
                db.session.commit()
                msg_succ()
                if console.get_bool("Update seating information? : "):
                    update_seating(event_id)
            else:
                print("No event found!")
        except Exception as e:
            msg_err("Error updating event data", e)
            db.session.rollback()

def update_concert():
    with app.app_context():
        try:
            concert_id = console.get_int("Please enter the concert ID (0 to quit): ", 0, valid = get_id_list(show_concerts))
            if concert_id == 0:
                return
            concert = Concert.query.filter_by(id=concert_id).first()
            res = console.update_data(name=(concert.name, str), artist=(concert.artist, str))
            concert.name = res["name"]
            concert.artist = res["artist"]
            db.session.commit()
            msg_succ()
        except Exception as e:
            msg_err("Error updating concert data", e)
            db.session.rollback()

def update_seating(event_id):
    with app.app_context():
        try:
            seating_id = console.get_int("Please enter the seating ID (0 to quit): ", 0, valid = get_id_list(show_seatings, event_id))
            if seating_id == 0:
                return
            
            seating = Seating.query.filter_by(id=seating_id).first()
            res = console.update_data(price=(seating.price, Decimal), seats_sold=(seating.seats_sold, int))
            seating.price = res["price"]
            seating.seats_sold = res["seats_sold"]
            db.session.commit()
            
        except Exception as e:
            msg_err("Error updating seating", e)
            db.session.rollback()
            
def update_venue():
    with app.app_context():
        try:
            venue_id = console.get_int("Please enter the Venue ID (0 to quit): ", 0, valid=get_id_list(show_venues))
            if venue_id == 0:
                return
            
            venue = Venue.query.filter_by(id=venue_id).first()
            res = console.update_data(name=(venue.name, str), address=(venue.address, str),
                                      image_url=(venue.image_url, str))
            featured = console.get_bool("Featured venue? [Y/N] (press 'Enter' to skip): ", venue.featured)
            venue.name = res["name"]
            venue.address = res["address"]
            venue.image_url = res["image_url"]
            venue.featured = featured
            db.session.commit()
            msg_succ()
            if console.get_bool("Update section information? : "):
                update_venue_sec(venue_id)
            
        except Exception as e:
            msg_err("Error updating venue",e)
            db.session.rollback()

def update_venue_sec(venue_id):
    with app.app_context():
        try:
            sec_id = console.get_int("Please enter the section ID (0 to quit): ", 0, valid = get_id_list(show_venue_sec,venue_id))
            if sec_id == 0:
                return
            sec = Venue_Section.query.filter_by(id=sec_id).first()
            res = console.update_data(name=(sec.sec_name, str), num_of_seats=(sec.num_of_seats, int))
            sec.num_of_seats = res["num_of_seats"]
            sec.sec_name = res["name"]
            db.session.commit()
            msg_succ()
        except Exception as e:
            msg_err("Error updating EMC data", e)
            db.session.rollback()
    
#Delete
def delete_data(data_name, data_type, display_func, *args):
    with app.app_context():
        try:
            id = console.get_int(f"Please enter the {data_name} ID to delete (0 to quit): ", 0, valid=get_id_list(display_func, *args))
            if id == 0:
                return
            data_type.query.filter_by(id=id).delete()
            if console.get_bool("About to delete data, [Y] to confirm [N] to abort? "):
                db.session.commit()
                msg_succ()
            else:
                print("Operation cancelled.")
            return id
        except Exception as e:
            msg_err(f"Error deleteing {data_name} data", e)
            return None

#TODO: use returned id to delete related data to maintain referential integrity 
def delete_emc():
    delete_data("EMC", EMC, show_emcs)

def delete_event():
    valid = get_id_list(show_emcs).append(-1)
    id = console.get_int("Please enter the EMC ID for the events (0 to quit, -1 to show all): ", -1, valid = valid)
    if id == 0:
        return
    elif id == -1:
        delete_data("Event", Event, show_events)
    else:
        delete_data("Event", Event, show_events, id)

def delete_concert():
    delete_data("concert", Concert, show_concerts)

def delete_seating():
    
    id = console.get_int("Please enter the event ID for the seatings (0 to quit): ", 0, valid = get_id_list(show_events))
    if id == 0:
        return
    delete_data("seating", Seating, show_seatings, id)

def delete_venue():
    vid = delete_data("venue", Venue, show_venues)
    if vid:
        delete_venue_sec(vid)
        
def delete_venue_sec(venue_id):
    with app.app_context():
        try:
            Venue_Section.query.filter_by(venue_id=venue_id).delete()
        except Exception as e:
            msg_err("Error deleting sections",e)

#Sys  
def quit():
    sys.exit()

def back():
    pass

main()

#stripe set up
# id_lst = [x for x in range(1,14)]
# stripe_upload_seatings(id_lst)