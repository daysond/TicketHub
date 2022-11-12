from App.models import User, EMC, Event, Venue, Venue_Section, Seating, Concert
from App import db, app
from sqlalchemy.exc import *
from decimal import *

import console

current_emc_id = -1

def main():
    
    global current_emc_id 
    current_emc_id = 1
    show_seatings()
    crud = ("Would you like to (U)plode (M)odify (S)how or (D)elete data? or (Q)uit: ")
    valid = frozenset("umsd")
    
    submenu = ("Event (M)anagement Company  (E)vents (C)oncerts (V)enues  "
            "(Q)uit (B)ack: ")
    subvalid = frozenset("emcvqb")
    
    call = dict(um=insert_emc, ue=insert_event, uc=insert_concert, uv=insert_venue,
                sm=show_emcs, se=show_events, sc=show_concerts, sv=show_venues,
                mm=update_emc, me=update_event, mc=update_concert, mv=update_venue,
                dm=delete_emc, de=delete_event, dc=delete_concert, delete_venue=delete_venue, 
                b=back, q=quit)
    
    while True:
        action = console.get_menu_choice(crud, valid, submenu, subvalid)
        function = call[action]
        function()
        
#CRUD #TODO: HANDLE ADDRESS UNIQUE
#Create 
def insert_emc():
    res = console.insert_menu('company', 'name')
    id = database_add(EMC(name = res.name))
    print(f'Data saved! Company {res.name} ID is {id} for you record.')
    
def insert_venue():
    res = console.insert_menu('venue', 'name', 'address', 'image_url')
    is_feat = console.get_bool("Should the venue be feature? ")
    (ok, id) = database_add(Venue(name = res.name, address = res.address, image_url = res.image_url, featured = is_feat))
    if ok:
        sections = [create_venue_sec(id) for i in range(console.get_int("Enter the number of sections of this venue: ", 1))]
        database_add_all(sections)
        
        print(f'Data saved! Venue {res.name} ID is {id} for you record.')
    return (ok, id)

def create_venue_sec(venue_id):
    num_of_seats = console.get_int("Enter the number of seats of this section: ", 1)
    res = console.insert_menu('section', 'name')
    ven_sec = Venue_Section(num_of_seats = num_of_seats, sec_name = res.name, venue_id = venue_id)
    return ven_sec
 
def insert_event():
    
    cid = 0
    vid = 0
    if console.get_bool('Are you making new event for an existing concert? '):
        # header = f'{"ID": <5} {"Name": <30} {"Artist":<20}\n'
        # concert_list = [ f'{str(c.id):<5} {c.name:<30} {c.artist:<20}\n' for c in get_all(Concert)]
        # concert_list.insert(0, header)
        # cid = console.get_int('Please select the concert ID from below:\n' + ''.join(concert_list), 1, len(concert_list))
        clen = len(show_concerts())
        cid = console.get_int('Please select the concert ID: ', 1, clen)
    else:
        (cok, cid) = insert_concert()
    
        if not cok:
            return (False, None)
        
    if console.get_bool('Is the event held in an existing venue? '):
        # header = f'{"ID": <5} {"Name": <24} {"Address":<30} {"Sections":<48} {"#Seats":<48}\n'
        # venue_list = [ f'{str(v.id):<5} {v.name:<24} {v.address:<30}\n' for v in get_all(Venue)]
        # venue_list.insert(0, header)
        vlen = len(show_venues())
        vid = console.get_int('Please select the venue ID: ', 1, vlen)
        # vid = console.get_int('Please select the concert ID from below:\n' + ''.join(venue_list),1,len(venue_list))
    else:
        (vok, vid) = insert_venue()
        
        if not vok:
            return (False, None)

    current_sections = get_venue_sec(vid)
    sec_price = {}

    for section in current_sections:
        price = console.get_decimal(f"Please enter the price for section [{section.sec_name}]: ")
        sec_price[section.id] = price
    
    date = console.get_date("Please Enter the date for the event MM-DD-YYYY. Eg. 09-19-2020: ")
    is_feat = console.get_bool("Should the event be feature? ")
    res = console.insert_menu('event', 'description', 'image_url')
    percentage = console.get_int("Enter the percentage of seats available(0-100)[default:100]: ",0, 100, 100)
    (ok, id) = database_add(Event(date = date, concert_id = cid, venue_id = vid, description = res.description, 
                        image_url = res.image_url, featured = is_feat, 
                        emc_id = current_emc_id, availablePercentage = percentage))
   
    if not ok:
        return (False, None)
    
    seatings = [Seating(price=price, event_id=id, venue_section_id=sec_id) for sec_id, price in sec_price.items()]
    database_add_all(seatings)
    
    return(ok, id)
    
def insert_concert():
    res = console.insert_menu('concert', 'name', 'artist')
    (ok, id) = database_add(Concert(name = res.name, artist = res.artist))
    if ok:
        print(f'Data saved! Concert {res.name} added! ID is {id} for you record.')
    return (ok, id)

def database_add_all(data):
    with app.app_context():
        db.session.add_all(data)
        db.session.commit()

def database_add(data):
    with app.app_context():
        try:
            db.session.add(data)
            db.session.flush()
            db.session.commit()
            return (True, data.id)
        except IntegrityError:
            db.session.rollback()
            print("Error adding data.")
            return (False, None)
        
def get_all(obj):
    with app.app_context():
        return obj.query.all()

def get_instance(obj, id):
    with app.app_context():
        while True:
            try:
                res = obj.query.filter_by(id=id).first()
                return res
            except InterfaceError:
                id = console.get_int("Error, please insert a valid ID: ")
    
def get_venue_sec(venue_id):
    with app.app_context():
        #session has to be open
        venue = Venue.query.filter_by(id=venue_id).first()
        sections = venue.sections
        return sections
#Read
def show_emcs():
    with app.app_context():
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
            print("Events: \n")
            for e in emc_event_list_str[idx]:
                print(event_header)
                print(f"{e}\n")

def show_events():
    with app.app_context():
        events = Event.query.all()
        header = f'{"ID": <5} {"Name": <30} {"Artist":<20} {"Venue":<24} {"Date":<12} {"Description":<30}'
        event_list_str = [ f'{e.id: <5} {e.concert.name: <30} {e.concert.artist:<20} {e.venue.name:<24} {str(e.date):<12} {e.description:<30}' for e in events]
        print(header)
        for s in event_list_str:
            print(f"{s} \n")
        
def show_concerts():
    header = f'{"ID": <5} {"Name": <30} {"Artist":<20}'
    concert_list = [ f'{str(c.id):<5} {c.name:<30} {c.artist:<20}' for c in get_all(Concert)]
    print(header)
    for s in concert_list:
        print(f"{s}")
    return concert_list

#TODO:remove default
def show_seatings(event_id=1):
    with app.app_context():
        seatings = Seating.query.filter_by(event_id = event_id)
        header = f'{"ID": <5} {"Section":<20} {"Price":<10} {"Seats Sold":<10} {"Event":<30}'  
        seating_list_str = [ f'{str(s.id):<5} {s.venue_section.sec_name:<20} {str(s.price):<10} {s.seats_sold:<10}  {s.event.concert.name:<30}' for s in seatings]
        print(header)
        for s in seating_list_str:
            print(f"{s}")
        return seating_list_str

def show_venues():
    with app.app_context():
        venues = Venue.query.all()
        header = f'{"ID": <5} {"Name": <24} {"Address":<30} {"Sections":<60} {"#Seats":<48}'  
        venue_list_str = [ f'{str(v.id):<5} {v.name:<24} {v.address:<30} {"/".join([ s.sec_name for s in v.sections]):<60} {"/".join([ str(s.num_of_seats) for s in v.sections]):<48}' for v in venues]
        print(header)
        for s in venue_list_str:
            print(f"{s}")
        return venue_list_str

#Uppdate
def update_emc():
    input_id = console.get_int("Please enter the EMC ID: ", 0)
    emc = get_instance(EMC, input_id)
    console.update_menu(name=(emc.name, str), balance=(emc.balance, Decimal))
    
    
def update_event():
    pass

def update_concert():
    pass

def update_seating():
    pass

def update_venue():
    pass

def update_venue_sec():
    pass

#Delete
def delete_emc():
    pass

def delete_event():
    pass

def delete_concert():
    pass

def delete_seating():
    pass

def delete_venue():
    pass

def delete_venue_sec():
    pass

def quit():
    pass

def back():
    pass

main()