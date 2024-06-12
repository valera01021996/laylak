import sqlite3

def connect_database(db_path: str =  "../database.sqlite") -> tuple:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return connection, cursor