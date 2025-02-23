from .enums_superclass import GenericEnum

class FALLBACK_DIRECTIVES_ENUM(GenericEnum):
    IGNORE = "ignore"
    EXECUTE_AS_SOON_AS_POSSIBLE = "execute_as_soon_as_possible"
    EXECUTE_ON_NEXT_RECURRENCY = "execute_on_next_recurrency"
