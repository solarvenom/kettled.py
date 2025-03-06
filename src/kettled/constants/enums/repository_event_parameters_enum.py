from .enum_superclass import EnumSuperclass

class REPOSITORY_EVENT_PARAMETERS_ENUM(EnumSuperclass):
    EVENT_NAME = "event_name"
    TIMESTAMP = "timestamp"
    RECURRENCY = "recurrency"
    FALLBACK_DIRECTIVE = "fallback_directive"
    CALLBACK = "callback"