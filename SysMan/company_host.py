from App.models import User, EMC, Event, Venue, Venue_Section, Seating, Concert
from App import db, app

import console

current_emc_id = -1

def main():
    
    #todo: current emc!!!
    global current_emc_id 
    current_emc_id = get_emc()
    
    crud = ("Would you like to (U)plode (M)odify (S)how or (D)elete data? or (Q)uit: ")
    valid = frozenset("umsd")
    
    submenu = ("Event (M)anagement Company  (E)vents (C)oncerts (V)enues  "
            "(Q)uit (B)ack: ")
    subvalid = frozenset("emcvqb")
    
    call = dict(um=insert_emc, ue=insert_event, uc=insert_concert, uv=insert_venue,
                sm=get_emc, se=get_event, sc=get_concert, sv=get_venue,
                mm=update_emc, me=update_event, mc=update_concert, mv=update_venue,
                dm=delete_emc, de=delete_event, dc=delete_concert, delete_venue=delete_venue, 
                b=back, q=quit)
    
    while True:
        action = console.get_menu_choice(crud, valid, submenu, subvalid)
        function = call[action]
        function()
        
#CRUD
#Create 
def insert_emc():
    res = console.insert_menu('company', 'name')
    id = insert_data(EMC(name = res.name))
    print(f'Data saved! Company {res.name} ID is {id} for you record.')
    
def insert_venue():
    res = console.insert_menu('venue', 'name', 'address', 'image_url')
    is_feat = console.get_bool("Should the venue be feature? ")
    id = insert_data(Venue(name = res.name, address = res.address, image_url = res.image_url, featured = is_feat))
    print(f'Data saved! Venue {res.name} ID is {id} for you record.')
    return id
 
def insert_event():
    
    cid = 0
    vid = 0
    if console.get_bool('Are you making new event for an existing concert? '):
        concert_list = [ f'ID: {c.id}   {c.name} by {c.artist}\n' for c in get_all(Concert)]
        cid = console.get_int('Please select the concert ID from below:\n' + ''.join(concert_list))
    else:
        cid = insert_concert()
    
    if console.get_bool('Is the event held in an existing venue? '):
        venue_list = [ f'ID: {v.id}   {v.name} located at {v.address}\n' for v in get_all(Venue)]
        vid = console.get_int('Please select the concert ID from below:\n' + ''.join(venue_list))
    else:
        vid = insert_venue()
    #TODO: insert seatings here
        
    date = console.get_date("Please Enter the date for the event MM-DD-YYYY. Eg. 09-19-2020: ")
    is_feat = console.get_bool("Should the event be feature? ")
    res = console.insert_menu('event', 'description', 'image_url')
    id = insert_data(Event(date = date, concert_id = cid, venue_id = vid, description = res.description, image_url = res.image_url, featured = is_feat, emc_id = current_emc_id))
    print(f'Data saved! Event ID is {id} for you record.')
    
def insert_concert():
    res = console.insert_menu('concert', 'name', 'artist')
    return insert_data(Concert(name = res.name, artist = res.artist))



def insert_seating():
    pass

def insert_venue_sec():
    pass

def insert_data(data):
    with app.app_context():
        db.session.add(data)
        db.session.flush()
        db.session.commit()
        return data.id

def get_all(obj):
    with app.app_context():
        return obj.query.all()
    

#Read
def get_emc():
    return 1

def get_event():
    pass

def get_concert():
    pass

def get_seating():
    pass

def get_venue():
    pass

def get_venue_sec():
    pass

#Uppdate
def update_emc():
    pass

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