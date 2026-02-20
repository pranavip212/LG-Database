import sqlite3

############################# SUPPLIER DATABASE ##########################3
# NEW TABLE + SIMPLE FUNCTS
CREATE_SUPPLIER_TABLE = """
CREATE TABLE IF NOT EXISTS suppliers(id INTEGER PRIMARY KEY, supplier_name TEXT NOT NULL, address TEXT, phone TEXT );
"""
INSERT_SUPPLIER = "INSERT INTO suppliers (supplier_name, address, phone) VALUES (?, ?, ?)"
GET_ALL_SUPPLIERS = "SELECT * FROM suppliers ORDER BY supplier_name ASC;"
GET_SUPPLIERS_BY_ID = "SELECT * FROM suppliers WHERE id = ?;"

#SUPPLIER DB CLASS

class suppDatabase:
    def __init__(self, db_name= 'data.db'):
        self.connection = sqlite3.connect('data.db')
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute(CREATE_SUPPLIER_TABLE)

    def add_supplier (self, supplier_name, address, phone):
        with self.connection:
            self.connection.execute(INSERT_SUPPLIER, (supplier_name, address, phone))

    def get_all_suppliers(self):
       with self.connection:
           return self.connection.execute(GET_ALL_SUPPLIERS).fetchone()

    def get_suppliers_by_id(self, supplier_id):
        with self.connection:
            return self.connection.execute(GET_SUPPLIERS_BY_ID, (supplier_id,)).fetchone()
#pre populated supplier info for db (info is chat generated, and had some help debugging the populating code)
    def seed_suppliers(self):
        existing_suppliers = self.connection.execute("SELECT COUNT(*) FROM suppliers;").fetchone()[0]
        if existing_suppliers == 0:
            suppliers = [
                ("Glossy Co.", "123 Lipstick Lane", "416-555-1234"),
                ("Shiny Beauty", "456 Gloss Ave", "604-555-5678"),
                ("Velvet Glow Ltd.", "789 Shine Blvd", "212-555-9012")
            ]
            with self.connection:
                for supplier in suppliers:
                    self.connection.execute(
                        "INSERT INTO suppliers (supplier_name, address, phone) VALUES (?, ?, ?);",
                        supplier
                    )
