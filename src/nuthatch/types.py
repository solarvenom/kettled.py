from datetime import datetime

class StorageEvent:
    def __init__(self, name, date_time, callback):
        self.name: str = name
        self.expires_at: int = self.convert_date_to_timestamp(date_time)
        self.callback = callback

    @staticmethod
    def convert_date_to_timestamp(date_str: str) -> int:
        return int(datetime.timestamp(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")))
        
class StorageEventInput:
    def __init__(self, name, date_time, callback):
        self.name = name
        self.date_time = date_time
        self.callback = callback