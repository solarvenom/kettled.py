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
                                recurrency TEXT NOT NULL,
                                fallback_directive TEXT NOT NULL,
                                callback TEXT NOT NULL);
                            """)
        self.connection.commit()
        
    def insert_event(self, event_name, timestamp, recurrency, fallback_directive, callback):
        self.cursor.execute(
            "INSERT INTO events (event_name, timestamp, recurrency, fallback_directive, callback) VALUES (?, ?, ?, ?, ?);",
            (event_name, timestamp, recurrency, fallback_directive, callback)
        )
        self.connection.commit()

    def delete_event_by_name(self, event_name):
        self.cursor.execute("DELETE FROM events WHERE event_name = ?;", (event_name,))
        self.connection.commit()

    def update_event_by_name(
        self, 
        event_name, 
        new_event_name = None, 
        new_timestamp = None,
        new_recurrency = None, 
        new_fallback_directive = None,
        new_callback = None):
        updates = []
        params = []
        query = "UPDATE events SET"
        if new_event_name != None: 
            updates.append("event_name = ?")
            params.append(event_name)
        if new_timestamp != None: 
            updates.append("timestamp = ?")
            params.append(new_timestamp)
        if new_recurrency != None:
            updates.append("recurrency = ?")
            params.append(new_recurrency)
        if new_fallback_directive != None:
            updates.append("fallback_directive = ?")
            params.append(new_fallback_directive)
        if new_callback != None:
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