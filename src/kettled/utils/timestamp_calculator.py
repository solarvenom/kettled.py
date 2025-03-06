import re
from datetime import datetime, date
from kettled.constants import ERROR_MESSAGES_ENUM
from .constants import DATE_FORMATS

def calculate_timestamp(specified_datetime) -> int:
    try:
        date_time = int(specified_datetime)
        if datetime.timestamp(datetime.now()) > date_time:
            raise ValueError(ERROR_MESSAGES_ENUM.TIMESTAMP_OUTDATED.value)
        return date_time
    except ValueError:
        timestamp = None
        if re.match(r"^\d{2}:\d{2}:\d{2}$", specified_datetime):
            time = datetime.strptime(specified_datetime, "%H:%M:%S").time()
            today_date = date.today()
            date_time = datetime.combine(today_date, time)
            timestamp = date_time.timestamp()
        else:
            for pattern in DATE_FORMATS.keys():
                if re.match(pattern, specified_datetime):
                    timestamp = int(datetime.timestamp(datetime.strptime(specified_datetime, DATE_FORMATS[pattern])))
                    break
            if timestamp == None:
                raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_DATE_FORMAT.value)
        return timestamp