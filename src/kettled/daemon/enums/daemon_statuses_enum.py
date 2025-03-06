from kettled.constants import EnumSuperclass, ICONS_ENUM
from kettled.constants.env import PID_FILE, DAEMON_NAME

class DAEMON_STATUSES_ENUM(EnumSuperclass):
    IS_ALREADY_RUNNING = f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} alredy running. check uptime with '{DAEMON_NAME} status'."
    IS_NOT_RUNNING = f"{ICONS_ENUM.KETTLE.value} pidfile {PID_FILE} does not exist. {DAEMON_NAME} not running?"
    IS_TERMINATED = f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} was terminated."
    IS_STARTED = f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} started."
    IS_DOWN = f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} is down."