import re
from datetime import datetime
from nuthatch.constants.date_formats import DATE_FORMATS
from nuthatch.constants.enums import ERROR_MESSAGES

class StorageEvent:
    def __init__(self, name, date_time, callback):
        if name is None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
        if callback is None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value)
        self.name: str = name
        self.expires_at: int | None = self.get_timestamp(date_time)
        self.callback = callback

    @staticmethod
    def get_timestamp(date: str) -> int | None:
        matched_format = None
        for pattern in DATE_FORMATS.keys():
            if re.match(pattern, date):
                matched_format = int(datetime.timestamp(datetime.strptime(date, DATE_FORMATS[pattern])))
                break

        if not matched_format:
            raise ValueError(ERROR_MESSAGES.UNSUPPORTED_DATE_FORMAT.value)
        return matched_format
        
class StorageEventInput:
    def __init__(self, name, date_time, callback):
        self.name = name
        self.date_time = date_time
        self.callback = callback