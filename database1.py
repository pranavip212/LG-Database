import sqlite3

CREATE_GLOSS_TABLE = "CREATE TABLE IF NOT EXISTS glosses(id INTEGER PRIMARY KEY, name TEXT, method TEXT, rating INTEGER, color TEXT);"

INSERT_GLOSS = "INSERT INTO glosses (name, method, rating, color) VALUES (?, ?, ?, ?);"

DELETE_GLOSS = "DELETE FROM glosses WHERE id = ?;"

GET_ALL_GLOSSES = "SELECT * FROM glosses ORDER BY name ASC;"

GET_GLOSSES_BY_NAME = "SELECT * FROM glosses WHERE name = ?;"

GET_GLOSSES_IN_RATING_RANGE = "SELECT * FROM glosses WHERE rating BETWEEN ? AND ?;"

GET_BEST_PREP_FOR_GLOSS = """
SELECT * FROM glosses
WHERE name = ? 
ORDER BY rating DESC
LIMIT 1;"""

GET_SUPPLIER_NAME = "SELECT * FROM glosses WHERE supplier = ?;"

class glossDatabase:
    def __init__(self, db_name= 'data.db'):
        self.connection = sqlite3.connect('data.db')
        self.create_tables()

    def connect(self):
        return

    def create_tables(self):
        with self.connection:
            self.connection.execute(CREATE_GLOSS_TABLE)

    def add_gloss (self, gloss):
        with self.connection:
            self.connection.execute(INSERT_GLOSS, (gloss['name'], gloss['method'], gloss['rating'], gloss['color']))

    def delete_gloss (self, gloss_id):
        with self.connection:
            self.connection.execute(DELETE_GLOSS, (gloss_id,))
        #doesnt delete anything but also doesnt cras hthe thingy
    def get_all_glosses(self):
        with self.connection:
            return self.connection.execute(GET_ALL_GLOSSES).fetchall()

    def get_glosses_in_rating_range (self, min_range, max_range):
            with self.connection:
                return self.connection.execute(GET_GLOSSES_IN_RATING_RANGE, (min_range, max_range)).fetchall()

    def get_glosses_by_name(self, name):
        with self.connection:
            return self.connection.execute(GET_GLOSSES_BY_NAME, (name,)).fetchall()

    def get_best_prep_for_gloss(self, name):
        with self.connection:
            return self.connection.execute(GET_BEST_PREP_FOR_GLOSS, (name,)).fetchone()

    def get_supplier_name (self, supplier)
        with self.connection:
            return self.connection.execute(GET_SUPPLIER_NAME, (supplier,)).fetchone()












""" import sqlite3

CREATE_GLOSS_TABLE = "CREATE TABLE IF NOT EXISTS glosses(id INTEGER PRIMARY KEY, name TEXT, method TEXT, rating INTEGER, color TEXT);"

INSERT_GLOSS = "INSERT INTO glosses (name, method, rating, color) VALUES (?, ?, ?, ?);"

DELETE_GLOSS = "DELETE FROM glosses WHERE name = ?;"
GET_ALL_GLOSSES = "SELECT * FROM glosses;"

GET_GLOSSES_BY_NAME = "SELECT * FROM glosses WHERE name = ?;"

GET_GLOSSES_IN_RATING_RANGE = "SELECT * FROM glosses WHERE rating BETWEEN ? AND ?;"

GET_BEST_PREP_FOR_GLOSS = #add 3 quotes start here wnd on 76
#SELECT * FROM glosses
#WHERE name = ? 
#ORDER BY rating DESC
#LIMIT 1;


def get_glosses_in_rating_range(connection, min_range, max_range):
    with connection:
        return connection.execute(GET_GLOSSES_IN_RATING_RANGE, (min_range, max_range)).fetchall()
        #connection.execute(GET_GLOSSES_IN_RATING_RANGE, (29, 80)).fetchall()
def connect():
    return sqlite3.connect('data.db')


def create_tables(connection):
    with connection:
        connection.execute(CREATE_GLOSS_TABLE)


def add_gloss(connection, name, method, rating, color):
    with connection:
        connection.execute(INSERT_GLOSS, (name, method, rating, color))

def delete_gloss (connection, name):
    with connection:
        connection.execute(DELETE_BEAN, (name,))


def get_all_glosses(connection):
    with connection:
        return connection.execute(GET_ALL_GLOSSES).fetchall()


def get_glosses_by_name(connection, name):
    with connection:
        return connection.execute(GET_GLOSSES_BY_NAME, (name,)).fetchall()


def get_best_prep_for_gloss(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREP_FOR_GLOSS, (name,)).fetchone()




"""