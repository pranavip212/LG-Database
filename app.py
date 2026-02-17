from database1 import glossDatabase
db = glossDatabase()
# time stamp tues 8 = 33.28
MENU_PROMPT = """ ---- Lip gloss Finder App ----
Please choose one of these options 
1) Add new lip gloss
2) See all lip glosses 
3) Find a gloss by name
4) See the best way to apply a gloss
5) Delete a gloss
6) Find lip glosses in a range (ie. Products between 70-90 rating)
7) Exit. 

Your selection: """

def menu():
    #self.connection = database1.connect()
    #database1.create_tables(self.connection)

    while (user_input := input(MENU_PROMPT)) != '7':
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

        else: print('Invalid input, please try again.')


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
        print(f"{gloss[1]} ({gloss[2]}) - {gloss[3]}/100 ")
    input("\n\n press enter to continue \n\n")

def prompt_add_new_gloss(db):
    name = input('enter gloss name: ')
    method = input('Enter how you wore it (ie. lipstick, lip liner, or alone): ')
    rating = int(input('Enter your rating (0-100): '))
    color = input('What color was the lip gloss: ')
    gloss = {
        "name": name,
        "method": method,
        "rating": rating,
        "color": color
    }
    db.add_gloss(gloss)
    input("\n\n press enter to continue \n\n")

menu()