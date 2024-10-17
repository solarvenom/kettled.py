from datetime import datetime

class StorageEvent:
    def __init__(self, name, date_time, callback):
        self.name: str = name
        self.expires_at: int = int(datetime.timestamp(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")))
        self.callback = callback
        

class StorageEventInput:
    def __init__(self, name, date_time, callback):
        self.name = name
        self.date_time = date_time
        self.callback = callback