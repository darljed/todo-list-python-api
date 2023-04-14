import sqlite3
from model import Connection

class DBINIT:
    def __init__(self) -> None:
        self.connection = Connection().connection
        self.db_init()

    def db_init(self):
        self.initialize_tables()

    def initialize_tables(self):
        try:
            with open('schema.sql') as f:
                self.connection.executescript(f.read())
            print("tables initialized")
        except sqlite3.OperationalError as e:
            print(e)

if __name__ == "__main__":
    dbinit = DBINIT()