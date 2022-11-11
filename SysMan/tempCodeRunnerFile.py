def main():
    
    crud = ("Would you like to (U)plode (M)odify (S)how or (D)elete data?(Q)uit: ")
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