# new db file 20/2/2026 
import sqlite3

CREATE_GLOSS_TABLE = "CREATE TABLE IF NOT EXISTS glosses(id INTEGER PRIMARY KEY, name TEXT, method TEXT, rating INTEGER, color TEXT, supplier_id INTEGER, FOREIGN KEY (supplier_id) REFERENCES suppliers(id));"

INSERT_GLOSS = "INSERT INTO glosses (name, method, rating, color, supplier_id) VALUES (?, ?, ?, ?, ?);"

DELETE_GLOSS = "DELETE FROM glosses WHERE id = ?;"

GET_ALL_GLOSSES = "SELECT * FROM glosses ORDER BY name ASC;"

GET_GLOSSES_BY_NAME = "SELECT * FROM glosses WHERE name = ?;"

GET_GLOSSES_IN_RATING_RANGE = "SELECT * FROM glosses WHERE rating BETWEEN ? AND ?;"

GET_BEST_PREP_FOR_GLOSS = """
SELECT * FROM glosses
WHERE name = ? 
ORDER BY rating DESC
LIMIT 1;"""

GET_GLOSSES_BY_SUPPLIER = "SELECT * FROM glosses WHERE supplier_id = ?;"

GET_SUPPLIER_INFO_FOR_GLOSS = """
SELECT suppliers.id, suppliers.supplier_name, suppliers.address, suppliers.phone
FROM glosses
JOIN suppliers ON glosses.supplier_id = suppliers.id
WHERE glosses.name = ?
ORDER BY glosses.rating DESC
LIMIT 1;
"""

# used forgien keys to make a relational db strucutre
# citation: https://www.knack.com/blog/how-to-design-an-effective-relational-database/
class glossDatabase:
    def __init__(self, db_name= 'data.db'):
        self.connection = sqlite3.connect('data.db')
        self.create_tables()
        self.connection.execute("PRAGMA foreign_keys = ON")

    def connect(self):
        return

    def create_tables(self):
        with self.connection:
            self.connection.execute(CREATE_GLOSS_TABLE)

    def add_gloss (self, gloss):
        with self.connection:
            self.connection.execute(INSERT_GLOSS, (
                gloss['name'],
                gloss['method'],
                gloss['rating'],
                gloss['color'],
                gloss['supplier_id']
            ))

    def delete_gloss (self, gloss_id):
        with self.connection:
            self.connection.execute(DELETE_GLOSS, (gloss_id,))

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

    def get_glosses_by_supplier(self, supplier_id):
        with self.connection:
            return self.connection.execute(GET_GLOSSES_BY_SUPPLIER,(supplier_id,)).fetchall()

    def get_supplier_info_for_gloss(self, name):
        with self.connection:
            return self.connection.execute(
                GET_SUPPLIER_INFO_FOR_GLOSS, (name,)).fetchone()
