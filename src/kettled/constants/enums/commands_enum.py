from .enums_superclass import GenericEnum

class COMMANDS_ENUM(GenericEnum):
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
    LIST = "list"
    ADD = "add"
    DELETE = "delete"
    UPDATE = "update"