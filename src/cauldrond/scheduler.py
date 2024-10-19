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

    def set(self, name, date_time, callback):
        if name is None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
        if name in self.index:
            raise ValueError(ERROR_MESSAGES.NAME_NOT_UNIQUE.value)
        if callback is None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value)
        timestamp = self.get_timestamp(date_time)
        if timestamp is None:
            raise ValueError(ERROR_MESSAGES.UNSUPPORTED_DATE_FORMAT.value)
        if timestamp not in self.storage:
            self.storage[timestamp] = {}
        self.storage[timestamp][name] = lambda: callback
        self.index[name] = timestamp

    def list(self):
        event_list: list[list] = []
        index = 1
        for event_name, timestamp in self.index.items():
            event_list.append([index, event_name, datetime.fromtimestamp(timestamp).isoformat()])
            index += 1
        for event in event_list:
            print('| {:1} | {:^4} | {:>4} |'.format(*event))
