from kettled.constants import EnumSuperclass, ICONS_ENUM

class DAEMON_ERROR_MESSAGES_ENUM(EnumSuperclass):
    FIRST_FORK_FAILED = f"{ICONS_ENUM.SKULL.value} Fork #1 failed: "
    SECOND_FORK_FAILED = f"{ICONS_ENUM.SKULL.value} Fork #2 failed: "
    SCHEDULER_NOT_RUNNING = f"{ICONS_ENUM.SKULL.value}  Scheduler not running..."