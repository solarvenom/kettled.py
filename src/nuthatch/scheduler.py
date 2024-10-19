from nuthatch.types import StorageEvent, StorageEventInput

class Scheduler:
    def __init__(self):
        self.storage: dict[int, list] = {}
        self.index: dict[str, int] = {}

    def set(self, timestamp: int, event: StorageEventInput):
        self.storage[timestamp].append(
            StorageEvent(
                name = event.name,
                date_time = event.date_time,
                callback =lambda: event.callback))

    