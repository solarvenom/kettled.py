EVENT_NAME = "test_event_name"
INCORRECT_EVENT_NAME = "incorrect_event_name"
OUTDATED_EVENT_DATE = "2024-10-17T14:28:00+02:00"
OUTDATED_EVENT_TIMESTAMP = 1729168080
EVENT_CALLBACK_VALUE = "Sitta europaea"
EVENT_UNSUPPORTED_DATE = "010203"
UPDATED_EVENT_NAME = "event2"
UPDATED_EVENT_TIMESTAMP = 1729427280
UPDATED_EVENT_DATE = "2024-10-20T14:28:00+02:00"
UPDATED_EVENT_CALLBACK_VALUE = "zZz zZz zZz"

def callback():
    return EVENT_CALLBACK_VALUE

def updated_callback():
    return UPDATED_EVENT_CALLBACK_VALUE
