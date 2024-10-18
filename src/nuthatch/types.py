from datetime import datetime

class StorageEvent:
    def __init__(self, name, date_time, callback):
        self.name: str = name
        self.expires_at: int = self.get_timestamp(date_time)
        self.callback = callback

    @staticmethod
    def get_timestamp(date: str) -> int:
        # return int(datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S")))
        return int(datetime.timestamp(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")))
        
class StorageEventInput:
    def __init__(self, name, date_time, callback):
        self.name = name
        self.date_time = date_time
        self.callback = callback