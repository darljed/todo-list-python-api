import sqlite3, os
from model import Connection

class DBINIT:
    def __init__(self) -> None:
        self.connection = Connection().connection
        self.schema_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'schema.sql')
        self.db_init()

    def db_init(self):
        self.initialize_tables()

    def initialize_tables(self):
        try:
            with open(self.schema_path) as f:
                self.connection.executescript(f.read())
            print("tables initialized")
        except sqlite3.OperationalError as e:
            print(e)

if __name__ == "__main__":
    dbinit = DBINIT()