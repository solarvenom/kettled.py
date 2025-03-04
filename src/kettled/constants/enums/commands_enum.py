from .enums_superclass import EnumSuperclass

class COMMANDS_ENUM(EnumSuperclass):
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
    LIST = "list"
    ADD = "add"
    DELETE = "delete"
    UPDATE = "update"