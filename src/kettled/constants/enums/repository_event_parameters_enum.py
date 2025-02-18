from enum import Enum

class REPOSITORY_EVENT_PARAMETERS_ENUM(Enum):
    EVENT_NAME = "event_name"
    TIMESTAMP = "timestamp"
    RECURRENCY = "recurrency"
    FALLBACK_DIRECTIVE = "fallback_directive"
    CALLBACK = "callback"