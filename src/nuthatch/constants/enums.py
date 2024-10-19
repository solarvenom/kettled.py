from enum import Enum
from env import ICON, ERROR_ICON

class COMMANDS(Enum):
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
    LIST = "list"

class ERROR_MESSAGES(Enum):
    UNSUPPORTED_DATE_FORMAT = f"{ERROR_ICON} Unsupported date format.\n"
    UNKNOWN_COMMAND = f"{ERROR_ICON} Unknown command.\n"
    MISSING_EVENT_NAME = f"{ERROR_ICON} Event name is missing.\n"
    MISSING_EVENT_CALLBACK = f"{ERROR_ICON} Event callback is missing.\n"

class MESSAGES(Enum):
    USAGE = f"{ICON} Available commands: {COMMANDS.START.value} | {COMMANDS.STOP.value} | {COMMANDS.RESTART.value} | {COMMANDS.STATUS.value}\n"
    IS_ALREADY_RUNNING = f"{ICON} Nuthatch alredy running. Check uptime with 'nuthatch status'.\n"
    IS_STARTED = f"{ICON} Nuthatch started\n"
    IS_DOWN = f"{ICON} Nuthatch is down\n"
    