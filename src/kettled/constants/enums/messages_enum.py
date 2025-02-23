from .enums_superclass import GenericEnum
from kettled.constants.enums.icons_enum import ICONS_ENUM
from kettled.constants.enums.commands_enum import COMMANDS_ENUM
from kettled.constants.env import DAEMON_NAME, PID_FILE

class MESSAGES_ENUM(GenericEnum):
    USAGE = f"{ICONS_ENUM.KETTLE.value} available commands: {COMMANDS_ENUM.START.value} | {COMMANDS_ENUM.STOP.value} | {COMMANDS_ENUM.RESTART.value} | {COMMANDS_ENUM.STATUS.value}\n"
    IS_ALREADY_RUNNING = f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} alredy running. check uptime with '{DAEMON_NAME} status'.\n"
    IS_STARTED = f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} started.\n"
    IS_DOWN = f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} is down.\n"
    IS_NOT_RUNNING = f"{ICONS_ENUM.KETTLE.value} pidfile {PID_FILE} does not exist. {DAEMON_NAME} not running?\n"
    EVENT_ADDED = f"{ICONS_ENUM.KETTLE.value} event scheduled.\n"
    IS_TERMINATED = f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} was terminated.\n"