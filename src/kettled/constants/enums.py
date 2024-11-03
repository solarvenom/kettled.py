from enum import Enum
from kettled.constants.env import DAEMON_NAME, PID_FILE

class ICONS(Enum):
    KETTLE = "🫖"
    SKULL = "☠️"
    FIX = "🛠️"
    FEATURE = "✨"

class COMMANDS(Enum):
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
    LIST = "list"
    ADD = "add"
    DELETE = "delete"
    UPDATE = "update"

class ERROR_MESSAGES(Enum):
    UNSUPPORTED_DATE_FORMAT = f"{ICONS.SKULL.value}  unsupported date format.\n"
    UNKNOWN_COMMAND = f"{ICONS.SKULL.value}  unknown command.\n"
    MISSING_EVENT_NAME = f"{ICONS.SKULL.value}  event_name is required.\n"
    MISSING_EVENT_DATETIME = f"{ICONS.SKULL.value}  event_date and time is required.\n"
    MISSING_EVENT_CALLBACK = f"{ICONS.SKULL.value}  callback is required.\n"
    EVENT_NAME_NOT_UNIQUE = f"{ICONS.SKULL.value}  event_name must be unique.\n"
    INSUFFICIENT_UPDATE_ARGS = f"{ICONS.SKULL.value}  event_name and new event_date or callback is required.\n"
    EVENT_NAME_NOT_FOUND = f"{ICONS.SKULL.value}  event with specified name not found.\n"
    NO_EVENTS_SCHEDULED = f"{ICONS.SKULL.value}  no events scheduled at the moment.\n"
    SCHEDULER_NOT_RUNNING = f"{ICONS.SKULL.value}  scheduler not running...\n"
    TIMESTAMP_OUTDATED = f"{ICONS.SKULL.value}  date_time must specify a future date.\n"

class MESSAGES(Enum):
    USAGE = f"{ICONS.KETTLE.value} available commands: {COMMANDS.START.value} | {COMMANDS.STOP.value} | {COMMANDS.RESTART.value} | {COMMANDS.STATUS.value}\n"
    IS_ALREADY_RUNNING = f"{ICONS.KETTLE.value} {DAEMON_NAME} alredy running. check uptime with '{DAEMON_NAME} status'.\n"
    IS_STARTED = f"{ICONS.KETTLE.value} {DAEMON_NAME} started.\n"
    IS_DOWN = f"{ICONS.KETTLE.value} {DAEMON_NAME} is down.\n"
    IS_NOT_RUNNING = f"{ICONS.KETTLE.value} pidfile {PID_FILE} does not exist. {DAEMON_NAME} not running?\n"
    EVENT_ADDED = f"{ICONS.KETTLE.value} event scheduled.\n"
    IS_TERMINATED = f"{ICONS.KETTLE.value} {DAEMON_NAME} was terminated.\n"

class EVENT_PARAMETERS(Enum):
    EVENT_NAME = "event_name"
    DATE_TIME = "date_time"
    CALLBACK = "callback"

class UPDATE_EVENT_PARAMETERS(Enum):
    NEW_EVENT_NAME = "new_event_name"
    NEW_DATE_TIME = "new_date_time"
    NEW_CALLBACK = "new_callback"

class COMMAND_PIPE(Enum):
    COMMAND = "command"
    DATA = "data"

class TERMINAL_PROMPTS(Enum):
    ADD_EVENT_NAME = f"{ICONS.KETTLE.value} Please enter event name: "
    ADD_EVENT_DATE_TIME = f"{ICONS.KETTLE.value} Please enter event scheduled date: "
    ADD_EVENT_CALLBACK = f"{ICONS.KETTLE.value} Please enter event callback: "
    DELETE_EVENT_NAME = f"{ICONS.KETTLE.value} Please enter the name of event to be deleted: "
    UPDATE_EVENT_NAME = f"{ICONS.KETTLE.value} Please enter the name of event be modified: "
    UPDATE_NEW_EVENT_NAME = f"{ICONS.KETTLE.value} Please enter the new event name or leave blank to leave unchanged: "
    UPDATE_NEW_DATE_TIME = f"{ICONS.KETTLE.value} Please enter the new event schdeuled date or leave blank to leave unchanged: "
    UPDATE_NEW_CALLBACK = f"{ICONS.KETTLE.value} Please enter the new event callback or leave blank to leave unchanged: "