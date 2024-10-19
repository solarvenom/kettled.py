import pytest
from nuthatch.types import StorageEvent
from nuthatch.constants.enums import ERROR_MESSAGES

test_name = "nuthatch"
test_date = "2024-10-17T14:28:00+02:00"
test_timestamp = 1729168080
test_phrase = "Sitta europaea"

def callback():
    return test_phrase

def test_storage_event_init():
    test_event = StorageEvent(
        name=test_name,
        date_time=test_date,
        callback=lambda: callback()
    )

    assert test_event.name == test_name
    assert test_event.expires_at == test_timestamp
    assert test_event.callback() == test_phrase

def test_missing_name():
    with pytest.raises(ValueError) as excinfo:
        StorageEvent(
            name=None,
            date_time=test_date,
            callback=lambda: callback()
        )

    assert str(excinfo.value) == ERROR_MESSAGES.MISSING_EVENT_NAME.value

def test_missing_callback():
    with pytest.raises(ValueError) as excinfo:
        StorageEvent(
            name=test_name,
            date_time=test_date,
            callback=None
        )

    assert str(excinfo.value) == ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value

def test_unsupported_timestring_format():
    with pytest.raises(ValueError) as excinfo:
        StorageEvent(
            name=test_name,
            date_time="010203",
            callback=lambda: callback()
        )
    
    assert str(excinfo.value) == ERROR_MESSAGES.UNSUPPORTED_DATE_FORMAT.value
