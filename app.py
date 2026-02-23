import csv
from database1 import glossDatabase
from supplierDatabase import suppDatabase
gloss_db = glossDatabase()
supplier_db = suppDatabase()
supplier_db.prep_suppliers() # to bring in the prepopulated suppliers

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
9) Add glosses from a CSV file
10) Exit. 

Your selection: """

def menu():
    #self.connection = database1.connect()
    #database1.create_tables(self.connection)

    while (user_input := input(MENU_PROMPT)) != '10':
        if user_input == '1':
            prompt_add_new_gloss(gloss_db)
        elif user_input == '2':
            prompt_see_all_glosses(gloss_db, supplier_db)
        elif user_input == '3':
            prompt_find_gloss(gloss_db)
        elif user_input == '4':
            prompt_find_best_method(gloss_db)
        elif user_input == '5':
            prompt_delete_gloss(gloss_db)
        elif user_input == '6':
            get_glosses_by_range(gloss_db)
        elif user_input == '7':
            prompt_find_by_supplier(gloss_db)
        elif user_input == '8':
            get_supplier_info(supplier_db, gloss_db)
        elif user_input == '9':
            populate_glosses_from_csv(gloss_db, supplier_db)
        else:
            print('Invalid input, please try again.')

def get_glosses_by_range(gloss_db):
    min_rating = int(input('Enter a minimum for your range (0-100) \n'))
    max_rating = int(input('Enter a maximum for your range (0-100)\n'))
    glosses = gloss_db.get_glosses_in_rating_range(min_rating, max_rating)
    try:
        if glosses:
            for gloss in glosses:
                print(f"{gloss[1]} ({gloss[2]}) - {gloss[3]}/100 ")
        else:
            print('No glosses found in this range')
    except ValueError:
        print('Please enter a valid number')


def prompt_delete_gloss(gloss_db):
    gloss_id = input('Enter the gloss ID to delete: ')
    try:
        gloss_id = int(gloss_id)
        gloss_db.delete_gloss(gloss_id)
        print("Gloss deleted successfully.")
    except ValueError:
        print("Please enter a valid numeric ID.")

    input("\n\n Press enter to continue \n\n")


def prompt_find_best_method(gloss_db):
    name = input('Enter gloss name to find: ')
    best_method = gloss_db.get_best_prep_for_gloss(name)
    print(f"The best application method for {name} is: {best_method[2]}")
    input("\n\n press enter to continue \n\n")

def prompt_find_gloss(gloss_db):
    name = input('Enter gloss name to find: ')
    results = gloss_db.get_glosses_by_name(name)
    for gloss in results:
        print(gloss)
            #f"{gloss[1]} ({gloss[2]}) - {gloss[3]}/100 ")
    input("\n\n press enter to continue \n\n")

def prompt_see_all_glosses(gloss_db, supplier_db):
    glosses = gloss_db.get_all_glosses()
    # print("DEBUG:", glosses)

    if not glosses:
        print("No glosses found.")
    else:
        for gloss in glosses:
            supplier = supplier_db.get_suppliers_by_id(gloss[5])
            supplier_name = supplier[1]
        # supplier id is in both dbs and links them. When I pass the id into the function
        # that gets the supplier info from the id, I return can all the supplier info. However, I limit here to just the supplier name
            print(f"""
    ID: {gloss[0]}
    Name: {gloss[1]}
    Method: {gloss[2]}
    Rating: {gloss[3]}/100
    Color: {gloss[4]}
    Supplier: {supplier_name}
    -------------------------
    """)
# no point in displaying supp id, cause no user would have a use for it. They can look it up w option 8 if needed.
# the id is mentioned in code as the foreign key
    input("\nPress enter to continue\n")

# start at index 1 to not show gloss id. gloss id is used to makesure user does not dleete more than one gloss with the same name

def prompt_add_new_gloss(gloss_db):
    name = input('enter gloss name: ')
    method = input('Enter how you wore it: ')
    rating = int(input('Enter your rating (0-100): '))
    color = input('What color was the lip gloss: ')

    suppliers = supplier_db.get_all_suppliers()
    print("\nAvailable suppliers:")
    for sup in suppliers:
        print(f"{sup[0]} - {sup[1]}")  # shows id and name

    supplier_id = int(input('Choose supplier ID from list: '))

    if not suppliers:
        print("No suppliers found. Add suppliers")
        return

    gloss = {
        "name": name,
        "method": method,
        "rating": rating,
        "color": color,
        "supplier_id": supplier_id
    }

    gloss_db.add_gloss(gloss)
    print("Gloss added successfully!")

"""def prompt_add_new_gloss(gloss_db):
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
    gloss_db.add_gloss(gloss)
    input("\n\n Gloss added. Press enter to continue \n\n")
"""
def prompt_find_by_supplier(gloss_db):
#trying out a nested if else loop in try/execpt
    suppliers = supplier_db.get_all_suppliers()
    print("\n All Suppliers: ")
    for sup in suppliers:
        print(f"{sup[0]} - {sup[1]}")

    try:
        supplier_id = int(input('Enter supplier ID to filter glosses by '))
        glosses = gloss_db.get_glosses_by_supplier(supplier_id)
        if glosses:
            for gloss in glosses:
                print(f"""
        Name: {gloss[1]}
        Method: {gloss[2]}
        Rating: {gloss[3]}/100
        Color: {gloss[4]}
        -------------------------
        """)
        else:
            print("No glosses found for this supplier.")

    except ValueError:
        print("Please enter a valid number.")

    input("\nPress enter to continue\n")

# funct related to supplier relational db
def get_supplier_info(supplier_db, gloss_db):
    name = input("Enter gloss name to look up supplier info: ")

    supplier_info = gloss_db.get_supplier_info_for_gloss(name)

    if supplier_info:
        print(f"""
Supplier ID: {supplier_info[0]}
Supplier Name: {supplier_info[1]}
Address: {supplier_info[2]}
Phone: {supplier_info[3]}
        """)
    else:
        print("No supplier found for that gloss.")

    input("\nPress enter to continue\n")

def populate_glosses_from_csv(gloss_db, supplier_db):
    with open ('glosses.csv', 'r') as file:
        reader = csv.DictReader(file)
        suppliers = supplier_db.get_all_suppliers()

        for row in reader: # meant to determine a supplier id by matching the name
            # not as simple but it keeps the funct relational, and works better if you plan to use supplier info/develop related functions more in the future
            supplier_id = None
            for s in suppliers:
                if s[1] == row['supplier_name']:  # s[1] is supplier_name
                    supplier_id = s[0]  # s[0] is supplier_id
                    break

            gloss = {
                "name": row['name'],
                "method": row['method'],
                "rating": int(row['rating']),
                "color": row['color'],
                "supplier_id": supplier_id
            }

            gloss_db.add_gloss(gloss)


    print("CSV data successfully added to the database!")



menu()
