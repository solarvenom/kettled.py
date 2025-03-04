from .enum_superclass import EnumSuperclass

class FALLBACK_DIRECTIVES_ENUM(EnumSuperclass):
    IGNORE = "ignore"
    EXECUTE_AS_SOON_AS_POSSIBLE = "execute_as_soon_as_possible"
    EXECUTE_ON_NEXT_RECURRENCY = "execute_on_next_recurrency"
