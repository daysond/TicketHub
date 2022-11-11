
from collections import namedtuple
from datetime import datetime
def get_menu_choice(menu=None, valid=None, submenu=None, subvalid=None):
    
    if menu is None:
        return ""
    
    while True:
        line = input(menu)
        if not line:
            print("Please select one of the options.")
        if line not in valid:
            print("ERROR only {0} are valid choices".format(
                  ", ".join(["'{0}'".format(x)
                  for x in sorted(valid)])))
        else:
            return line+get_menu_choice(submenu, subvalid)

# def get_user_input(**prompts):
def insert_menu(*prompts):
    obj_name = prompts[0]
    data = namedtuple('Data', [p for p in prompts[1:]])
    content = [input(f"Please enter the {p} of the {obj_name}: ") for p in prompts[1:]]
    return data(*content)

def get_bool(prompt):
    valid = frozenset('yn')
    while True:
        line = input(prompt + '[Y/N]: ')
        if not line or line.lower() not in valid:
            print("Please enter 'Y' or 'N'")
        else:
            return line.lower() == "y"               
    
def get_date(prompt):
    date_str = input(prompt)
    return datetime.strptime(date_str, '%m-%d-%Y').date()

def get_int(prompt):
    line = input(prompt)
    return line