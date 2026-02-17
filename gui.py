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