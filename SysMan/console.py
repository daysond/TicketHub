
from collections import namedtuple
from datetime import datetime
from decimal import *

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
def update_menu(**prompts):
      for key, value in prompts.items():
        while True:
            try:
                line = input(f"Enter new {key} [{value[0]}] (press enter skip): ")
                newVal = value[1](line)
                break
            except:
                print(f"Please enter a valid {key}")
                
        
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
    while True:
        line = input(prompt)
        if not line:
            print("Please enter a value.")
        else:
            try:
                date = datetime.strptime(line, '%m-%d-%Y').date()
                return date
            except ValueError:
                print('\nPlease enter a valid date: ')

def get_int(prompt, minimum=None, maximum=None, default=None):
    while True:
        line = input(prompt)
        if not line:
            print("Please enter a value.")
        if not line and default is not None:
            return default
        else:
            try:
                num = int(line)
                if (minimum is not None and num < minimum) or (maximum is not None and num > maximum):
                    print("Invalid choice!")
                else:
                    return num
            except ValueError:
                print('\nPlease enter a valid integer: ')
                
def get_decimal(prompt, minimum=None, maximum=None):
    while True:
        line = input(prompt)
        if not line:
            print("Please enter a value.")
        else:
            try:
                num = Decimal(line)
                if (minimum is not None and num < minimum) or (maximum is not None and num > maximum):
                    print("Invalid choice!")
                else:
                    return num
            except ValueError:
                print('\nPlease enter a valid integer: ')
        
