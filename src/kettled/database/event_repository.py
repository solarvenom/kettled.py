import sqlite3
from kettled.constants.env import DB_FILE

class EventRepository():
    def __init__(self):
        self.connection: sqlite3.Connection = sqlite3.connect(DB_FILE)
        self.connection.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        self.create_storage_table()
        
    def create_storage_table(self):
        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS events (
                                id INTEGER PRIMARY KEY,
                                event_name TEXT UNIQUE NOT NULL,
                                timestamp TIMESTAMP NOT NULL,
                                callback TEXT NOT NULL);
                            """)
        self.connection.commit()
        
    def insert_event(self, event_name, timestamp, callback):
        self.cursor.execute(
            "INSERT INTO events (event_name, timestamp, callback) VALUES (?, ?, ?);",
            (event_name, timestamp, callback)
        )
        self.connection.commit()

    def delete_event_by_name(self, event_name):
        self.cursor.execute("DELETE FROM events WHERE event_name = ?;", (event_name,))
        self.connection.commit()

    def update_event_by_name(self, event_name, new_event_name = None, new_timestamp = None, new_callback = None):
        updates = []
        params = []
        query = "UPDATE events SET"
        if new_event_name is not None: 
            updates.append("event_name = ?")
            params.append(event_name)
        if new_timestamp is not None: 
            updates.append("timestamp = ?")
            params.append(new_timestamp)
        if new_callback is not None:
            updates.append("callback = ?")
            params.append(new_callback)
        query += " " + ", ".join(updates)
        query += "WHERE event_name = ?;"
        params.append(event_name)

        self.cursor.execute(query, params)
        self.connection.commit()

    def get_all_events(self):
        all_events = self.cursor.execute("SELECT * from events")
        self.connection.commit()
        return all_events