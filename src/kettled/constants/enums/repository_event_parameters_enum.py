from .enums_superclass import GenericEnum

class REPOSITORY_EVENT_PARAMETERS_ENUM(GenericEnum):
    EVENT_NAME = "event_name"
    TIMESTAMP = "timestamp"
    RECURRENCY = "recurrency"
    FALLBACK_DIRECTIVE = "fallback_directive"
    CALLBACK = "callback"