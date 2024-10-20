import re
from datetime import datetime
from cauldrond.constants.date_formats import DATE_FORMATS
from cauldrond.constants.enums import ERROR_MESSAGES

class Scheduler:
    def __init__(self):
        self.storage: dict[int, dict] = {}
        self.index: dict[str, int] = {}
    
    @staticmethod
    def get_timestamp(date: str) -> int | None:
        matched_format = None
        for pattern in DATE_FORMATS.keys():
            if re.match(pattern, date):
                matched_format = int(datetime.timestamp(datetime.strptime(date, DATE_FORMATS[pattern])))
                break
        return matched_format

    def get(self, event_name):
        timestamp = self.index[event_name]
        if timestamp is None:
            raise ValueError(ERROR_MESSAGES.EVENT_NAME_NOT_FOUND.value)
        callback = self.storage[timestamp][event_name]
        return { "event_name": event_name, "date_time": timestamp, "callback": callback }

    def set(self, event_name, date_time, callback):
        if event_name is None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
        if event_name in self.index:
            raise ValueError(ERROR_MESSAGES.NAME_NOT_UNIQUE.value)
        if date_time is None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_DATETIME.value)
        if callback is None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value)
        timestamp = self.get_timestamp(date_time)
        if timestamp is None:
            raise ValueError(ERROR_MESSAGES.UNSUPPORTED_DATE_FORMAT.value)
        if timestamp not in self.storage:
            self.storage[timestamp] = {}
        self.storage[timestamp][event_name] = lambda: callback
        self.index[event_name] = timestamp

    def list(self):
        event_list: list[list] = []
        index = 1
        for event_name, timestamp in self.index.items():
            event_list.append([index, event_name, datetime.fromtimestamp(timestamp).isoformat()])
            index += 1
        for event in event_list:
            print('| {:1} | {:^4} | {:>4} |'.format(*event))

    def remove(self, event_name):
        if event_name not in self.index.keys():
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
        event_timestamp = self.index[event_name]
        if len(self.storage[event_timestamp]) > 1:
            self.storage[event_timestamp].pop(event_name)
        else:
            self.storage.pop(event_timestamp)
        self.index.pop(event_name)

    def update(self, event_name, date_time, callback):
        if event_name is None or (date_time is None and callback is None):
            raise ValueError(ERROR_MESSAGES.INSUFFICIENT_UPDATE_ARGS.value)
        event_to_update = self.get(event_name)
        if date_time is not None:
            event_to_update["date_time"] = date_time
        if callback is not None:
            event_to_update["callback"] = callback
        self.remove(event_name)
        self.set(
            event_name=event_to_update["event_name"], 
            date_time=event_to_update["date_time"], 
            callback=event_to_update["callback"])
