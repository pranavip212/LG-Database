from tkinter import *
from database1 import glossDatabase
import random
from tkinter import messagebox
import tkinter.font as tkfont
from time import strftime

db = glossDatabase()

root = Tk()
root.title("Gloss App ;)")
root.geometry('700x700')


mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
#mainframe.pack(pady = 100, padx = 100)

###GLOBALS
gloss_data = []  # global list to store rows
font_is_large = False
timestamp_visible = False
##################################FUNCTIONS / FUNCTIONALITY#######################
def add_gloss():
    name = name_entry.get()
    method = method_entry.get()
    rating = rating_entry.get()
    color = color_entry.get()

    if not name or not method or not rating or not color:
        messagebox.showerror("Error", "You forgot to enter all the feilds")
        return

    try:
        rating = int(rating )
    except ValueError:
        messagebox.showerror("Error", "Rating must be a number")

    db.add_gloss({
        "name": name,
        "method": method,
        "rating": rating,
        "color": color
    })
    refresh_list()
    clear_entries()

###used chat gpt for delete gloss funct
def delete_gloss():
    global gloss_data
    selected_index = gloss_list.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Select a gloss to delete")
        return

    index = selected_index[0]
    gloss_id = gloss_data[index][0]  # Get the ID from stored row

    print("Selected index:", index)
    print("Gloss ID being sent to DB:", gloss_id)

    # Optional confirmation
    if messagebox.askyesno("Confirm Delete", f"Delete '{gloss_data[index][1]}'?"):
        db.delete_gloss(gloss_id)
        refresh_list()



def clear_entries():
    name_entry.delete(0, END)
    method_entry.delete(0, END)
    rating_entry.delete(0, END)
    color_entry.delete(0, END)


def refresh_list():
    global gloss_data
    gloss_list.delete(0, END)

    gloss_data = db.get_all_glosses()  # store rows for deletion

    for gloss in gloss_data:
        display = f"{gloss[0]} | {gloss[1]} | {gloss[2]} | {gloss[3]} | {gloss[4]}"
        gloss_list.insert(END, display)

################################### L A B E L S ###############################

label = Label(root, text="Gloss Database", font =("Arial", 18))
label.grid(pady=20)

#################### little clock / timestamp req
time_stamp = Label(root, font=('calibri', 18, 'bold'), background='black', foreground='white')
time_stamp.grid(row=1,column = 2)

######################## INPUT FEILDS  ################
Label(root, text="Name").grid(row=2, column=0)
name_entry = Entry(root)
name_entry.grid(row=2, column=1)

Label(root, text="Method of Application").grid(row=3, column=0)
method_entry = Entry(root)
method_entry.grid(row=3, column=1)

Label(root, text="Rating (0-100)").grid(row=4, column=0)
rating_entry = Entry(root)
rating_entry.grid(row=4, column=1)

Label(root, text="Color").grid(row=5, column=0)
color_entry = Entry(root)
color_entry.grid(row=5, column=1)
 #################################### B U T T O N S #####################
Button(root, text="Add Gloss", width=15, command=add_gloss).grid(row=6, column=0, pady=10)
Button(root, text="Delete Gloss", width=15, command=delete_gloss).grid(row=6, column=1, pady=10)
Button(root, text="Refresh", width=15, command=refresh_list).grid(row=7, column=0, columnspan=2)
Button(root, text="Clear", width=15, command=clear_entries).grid(row=8, column=0, columnspan=2, pady=5)


gloss_list = Listbox(root, width=50)
gloss_list.grid(row=9, column=1, columnspan=1, pady=15)

#########################################  DROP DOWN MENU ###############################
def change_dropdown(*args):
    selection = tkvar.get()
    if selection == "Toggle font":
        toggle_font()
    elif selection == "timestamp on/off":
        toggle_timestamp()

        # do other 'stuff' here
       # new_font = ("Helvetica", 16, "bold")
    # add more here



#### refactoring the font code into a funct for readability/cleanness

def toggle_font():
    global font_is_large
    default_font = tkfont.nametofont("TkDefaultFont")

    if not font_is_large:
        default_font.config(family = "Papyrus", size=10)
        font_is_large = True
    else:
        default_font.config(family = "Arial", size=10)
        font_is_large = False

def update_time():
    current_time = strftime('%H:%M:%S %p')  # format the time
    time_stamp.config(text=current_time)
    time_stamp.after(1000, update_time)  # call itself again after 1 second

def toggle_timestamp():
    global timestamp_visible
    timestamp_visible = not timestamp_visible

    if timestamp_visible:
        time_stamp.grid(row=1, column=1, columnspan=2, pady=10)  # place it nicely
        update_time()
    else:
        time_stamp.grid_remove()




###############################################################
# -------------The drop down menu code is below ---------------
# Create a Tkinter variable
tkvar = StringVar(root)
tkvar.set('SETTING MENU') # set the default option
# link function to change dropdown
tkvar.trace('w', change_dropdown)


# list with options
choices = ['Toggle font','encryption on/off',
            'timestamp on/off']


optionmenu = OptionMenu(mainframe, tkvar, *choices)
optionmenu.config(width=30)
optionmenu.grid(row = 1, column =1)

# Load existing glosses on startup
refresh_list()
root.mainloop()

#new gui code
"""from database1 import glossDatabase
from suppliers_db import supplierDatabase
gloss_db = glossDatabase()
supplier_db = supplierDatabase()

# time stamp tues 8 = 33.28
MENU_PROMPT = """ ---- Lip gloss Finder App ----
Please choose one of these options 
1) Add new lip gloss
2) See all lip glosses 
3) Find a gloss by name
4) See the best way to apply a gloss
5) Delete a gloss
6) Find lip glosses in a range (ie. Products between 70-90 rating)
7) Find glosses by supplier ID
8) Look up supplier info
9) Exit. 

Your selection: """

def menu():
    #self.connection = database1.connect()
    #database1.create_tables(self.connection)

    while (user_input := input(MENU_PROMPT)) != '9':
        if user_input == '1':
            prompt_add_new_gloss(db)
        elif user_input == '2':
            prompt_see_all_glosses(db)
        elif user_input == '3':
            prompt_find_gloss(db)
        elif user_input == '4':
            prompt_find_best_method(db)
        elif user_input == '5':
            prompt_delete_gloss(db)
        elif user_input == '6':
            get_glosses_by_range(db)
        elif user_input == '7':
            prompt_find_by_supplier(db)
        elif user_input == '8':
            pass
        else:
            print('Invalid input, please try again.')

def get_glosses_by_range(db):
    min_rating = int(input('Enter a minimum for your range (0-100) \n'))
    max_rating = int(input('Enter a maximum for your range (0-100)\n'))
    glosses = db.get_glosses_in_rating_range(min_rating, max_rating)
    try:
        if glosses:
            for gloss in glosses:
                print(f"{gloss[1]} ({gloss[2]}) - {gloss[3]}/100 ")
        else:
            print('No glosses found in this range')
    except ValueError:
        print('Please enter a valid number')


def prompt_delete_gloss(db):
    name = input('Enter the gloss name to delete: ')
    db.delete_gloss(name)
    print(f"All glosses named '{name}' have been deleted")
    input("\n\n press enter to continue \n\n")


def prompt_find_best_method(db):
    name = input('Enter gloss name to find: ')
    best_method = db.get_best_prep_for_gloss(name)
    print(f"The best application method for {name} is: {best_method[2]}")
    input("\n\n press enter to continue \n\n")

def prompt_find_gloss(db):
    name = input('Enter gloss name to find: ')
    results = db.get_glosses_by_name(name)
    for gloss in results:
        print(gloss)
            #f"{gloss[1]} ({gloss[2]}) - {gloss[3]}/100 ")
    input("\n\n press enter to continue \n\n")

def prompt_see_all_glosses(db):
    glosses = db.get_all_glosses()
    for gloss in glosses:
        print(f"""
        Name: {gloss[1]}
        Method: {gloss[2]}
        Rating: {gloss[3]}/100
        Color: {gloss[4]}
        Supplier ID: {gloss[5]}
        Supplier Name: {gloss[6]}
        -------------------------
        """)

    input("\nPress enter to continue\n")

def prompt_add_new_gloss(db):
    name = input('enter gloss name: ')
    method = input('Enter how you wore it (ie. lipstick, lip liner, or alone): ')
    rating = int(input('Enter your rating (0-100): '))
    color = input('What color was the lip gloss: ')
    supplier_id = int(input('Enter supplier ID (number): '))
    supplier_name = input('Enter supplier name: ')

    gloss = {
        "name": name,
        "method": method,
        "rating": rating,
        "color": color,
        "supplier_id": supplier_id,
        "supplier_name": supplier_name
    }
    db.add_gloss(gloss)
    input("\n\n Gloss added. Press enter to continue \n\n")

def prompt_find_by_supplier(db):
#trying out a nested if else loop in try/execpt
    try:
        supplier_id = int(input('Enter supplier ID: '))
        glosses = db.get_glosses_by_supplier(supplier_id)

        if glosses:
            for gloss in glosses:
                print(f"""
        Name: {gloss[1]}
        Method: {gloss[2]}
        Rating: {gloss[3]}/100
        Color: {gloss[4]}
        Supplier: {gloss[6]}
        -------------------------
        """)
        else:
            print("No glosses found for this supplier.")

    except ValueError:
        print("Please enter a valid number.")

    input("\nPress enter to continue\n")

# funct related to supplier relational db
def get_supplier_info(supplier_db, gloss_db):
# this funct will ask for a gloss name, and give the related supplier info
gloss_name = input("Enter the gloss name: ")
glosses = gloss_db.get_glosses_by_name(gloss_name)

if not glosses:
    print("No glosses found for this supplier.")
    input("\nPress enter to continue\n")
    return
else:
    for gloss in glosses:
        supplier_id = gloss[5]
        supplier = supplier_db.get_supplier_by_id(supplier_id)

        if supplier:
            print(f"""
        Name: {supplier[1]}
        Adress: {supplier[2]}
        Phone: {supplier[3]}
        """)
        else:
            print("No suppliers found for this gloss.")
            input("\nPress enter to continue\n")


menu()"""
