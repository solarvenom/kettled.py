from enum import Enum

class FALLBACK_DIRECTIVES_ENUM(Enum):
    IGNORE = "ignore"
    EXECUTE_AS_SOON_AS_POSSIBLE = "execute_as_soon_as_possible"
    EXECUTE_ON_NEXT_RECURRENCY = "execute_on_next_recurrency"
