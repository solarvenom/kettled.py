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

class ERROR_MESSAGES(Enum):
    UNSUPPORTED_DATE_FORMAT = f"{ICONS.SKULL} Unsupported date format.\n"
    UNKNOWN_COMMAND = f"{ICONS.SKULL} Unknown command.\n"
    MISSING_EVENT_NAME = f"{ICONS.SKULL} event_name is required.\n"
    MISSING_EVENT_DATETIME = f"{ICONS.SKULL} event_date and time is required.\n"
    MISSING_EVENT_CALLBACK = f"{ICONS.SKULL} Callback is required.\n"
    NAME_NOT_UNIQUE = f"{ICONS.SKULL} event_name must be unique.\n"
    INSUFFICIENT_UPDATE_ARGS = f"{ICONS.SKULL} event_name and new event_date or callback is required.\n"
    EVENT_NAME_NOT_FOUND = f"{ICONS.SKULL} event with specified name not found.\n"

class MESSAGES(Enum):
    USAGE = f"{ICONS.CRYSTALL_BALL} Available commands: {COMMANDS.START.value} | {COMMANDS.STOP.value} | {COMMANDS.RESTART.value} | {COMMANDS.STATUS.value}\n"
    IS_ALREADY_RUNNING = f"{ICONS.CRYSTALL_BALL} Cauldrond alredy running. Check uptime with 'cauldrond status'.\n"
    IS_STARTED = f"{ICONS.CRYSTALL_BALL} Cauldrond started.\n"
    IS_DOWN = f"{ICONS.CRYSTALL_BALL} Cauldrond is down.\n"

class EVENT_PARAMETERS(Enum):
    EVENT_NAME = "event_name"
    DATE_TIME = "date_time"
    CALLBACK = "callback"
