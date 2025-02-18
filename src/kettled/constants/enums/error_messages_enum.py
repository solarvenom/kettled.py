from enum import Enum
from kettled.constants.enums.icons_enum import ICONS_ENUM

class ERROR_MESSAGES_ENUM(Enum):
    UNSUPPORTED_DATE_FORMAT = f"{ICONS_ENUM.SKULL.value}  unsupported date format.\n"
    UNKNOWN_COMMAND = f"{ICONS_ENUM.SKULL.value}  unknown command.\n"
    MISSING_EVENT_NAME = f"{ICONS_ENUM.SKULL.value}  event_name is required.\n"
    MISSING_EVENT_DATETIME = f"{ICONS_ENUM.SKULL.value}  event_date and time is required.\n"
    MISSING_EVENT_CALLBACK = f"{ICONS_ENUM.SKULL.value}  callback is required.\n"
    EVENT_NAME_NOT_UNIQUE = f"{ICONS_ENUM.SKULL.value}  event_name must be unique.\n"
    INSUFFICIENT_UPDATE_ARGS = f"{ICONS_ENUM.SKULL.value}  event_name and new event_date or callback is required.\n"
    EVENT_NAME_NOT_FOUND = f"{ICONS_ENUM.SKULL.value}  event with specified name not found.\n"
    NO_EVENTS_SCHEDULED = f"{ICONS_ENUM.SKULL.value}  no events scheduled at the moment.\n"
    SCHEDULER_NOT_RUNNING = f"{ICONS_ENUM.SKULL.value}  scheduler not running...\n"
    TIMESTAMP_OUTDATED = f"{ICONS_ENUM.SKULL.value}  date_time must specify a future date.\n"
    DB_CONNECTION_FAILED = f"{ICONS_ENUM.SKULL.value}  DB connection failed.\n"