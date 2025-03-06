import re
from datetime import datetime
from kettled.constants import DATE_FORMATS, ERROR_MESSAGES_ENUM

def calculate_timestamp(date) -> int:
    try:
        date_time = int(date)
        if datetime.timestamp(datetime.now()) > date_time:
            raise ValueError(ERROR_MESSAGES_ENUM.TIMESTAMP_OUTDATED.value)
        return date_time
    except ValueError:
        timestamp = None
        for pattern in DATE_FORMATS.keys():
            if re.match(pattern, date):
                timestamp = int(datetime.timestamp(datetime.strptime(date, DATE_FORMATS[pattern])))
                break
        if timestamp == None:
            raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_DATE_FORMAT.value)
        return timestamp