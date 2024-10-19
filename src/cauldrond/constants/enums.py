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
    MISSING_EVENT_NAME = f"{ICONS.SKULL} Event name is required.\n"
    MISSING_EVENT_DATETIME = f"{ICONS.SKULL} Event date and time is required.\n"
    MISSING_EVENT_CALLBACK = f"{ICONS.SKULL} Event callback is required.\n"
    NAME_NOT_UNIQUE = f"{ICONS.SKULL} Event name must be unique.\n"

class MESSAGES(Enum):
    USAGE = f"{ICONS.CRYSTALL_BALL} Available commands: {COMMANDS.START.value} | {COMMANDS.STOP.value} | {COMMANDS.RESTART.value} | {COMMANDS.STATUS.value}\n"
    IS_ALREADY_RUNNING = f"{ICONS.CRYSTALL_BALL} Claudrond alredy running. Check uptime with 'claudrond status'.\n"
    IS_STARTED = f"{ICONS.CRYSTALL_BALL} Claudrond started\n"
    IS_DOWN = f"{ICONS.CRYSTALL_BALL} Claudrond is down\n"
