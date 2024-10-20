from enum import Enum

class ICONS(Enum):
    CRYSTALL_BALL = "🔮"
    SKULL = "☠️"

class COMMANDS(Enum):
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
    LIST = "list"
    ADD = "add"

class ERROR_MESSAGES(Enum):
    UNSUPPORTED_DATE_FORMAT = f"{ICONS.SKULL.value}  Unsupported date format.\n"
    UNKNOWN_COMMAND = f"{ICONS.SKULL.value}  Unknown command.\n"
    MISSING_EVENT_NAME = f"{ICONS.SKULL.value}  event_name is required.\n"
    MISSING_EVENT_DATETIME = f"{ICONS.SKULL.value}  event_date and time is required.\n"
    MISSING_EVENT_CALLBACK = f"{ICONS.SKULL.value}  Callback is required.\n"
    NAME_NOT_UNIQUE = f"{ICONS.SKULL.value}  event_name must be unique.\n"
    INSUFFICIENT_UPDATE_ARGS = f"{ICONS.SKULL.value}  event_name and new event_date or callback is required.\n"
    EVENT_NAME_NOT_FOUND = f"{ICONS.SKULL.value}  event with specified name not found.\n"
    NO_EVENTS_SCHEDULED = f"{ICONS.SKULL.value}  No events scheduled at the moment.\n"

class MESSAGES(Enum):
    USAGE = f"{ICONS.CRYSTALL_BALL.value} Available commands: {COMMANDS.START.value} | {COMMANDS.STOP.value} | {COMMANDS.RESTART.value} | {COMMANDS.STATUS.value}\n"
    IS_ALREADY_RUNNING = f"{ICONS.CRYSTALL_BALL.value} Cauldrond alredy running. Check uptime with 'cauldrond status'.\n"
    IS_STARTED = f"{ICONS.CRYSTALL_BALL.value} Cauldrond started.\n"
    IS_DOWN = f"{ICONS.CRYSTALL_BALL.value} Cauldrond is down.\n"
    EVENT_ADDED = f"{ICONS.CRYSTALL_BALL.value} Event scheduled.\n"

class EVENT_PARAMETERS(Enum):
    EVENT_NAME = "event_name"
    DATE_TIME = "date_time"
    CALLBACK = "callback"
