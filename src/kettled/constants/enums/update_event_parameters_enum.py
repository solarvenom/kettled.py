from .enums_superclass import GenericEnum

class UPDATE_EVENT_PARAMETERS_ENUM(GenericEnum):
    NEW_EVENT_NAME = "new_event_name"
    NEW_DATE_TIME = "new_date_time"
    NEW_RECURRENCY = "new_recurrency"
    NEW_FALLBACK_DIRECTIVE = "new_fallback_directive"
    NEW_CALLBACK = "new_callback"