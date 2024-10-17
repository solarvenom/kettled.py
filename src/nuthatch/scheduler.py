from dataclasses import dataclass, field
from nuthatch.types import StorageEvent, StorageEventInput

@dataclass
class Scheduler:
    storage: dict[int, list[StorageEvent]] = field(default_factory=dict[int, list[StorageEvent]])
    index: dict[str, int] = field(default_factory=dict[str, int])

    def add(self, timestamp: int, event: StorageEventInput):
        self.storage[timestamp].append(
            StorageEvent(
                name=event.name,
                date_time=event.date_time, 
                callback=lambda: event.callback))
        