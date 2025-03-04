from kettled.constants import EnumSuperclass

class DAEMON_COMMANDS_ENUM(EnumSuperclass):
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
    LIST = "list"
    ADD = "add"
    DELETE = "delete"
    UPDATE = "update"