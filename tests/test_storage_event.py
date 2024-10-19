import pytest
from nuthatch.types import StorageEvent
from nuthatch.constants.enums import ERROR_MESSAGES
import seeds

def callback():
    return seeds.STORAGE_EVENT_CALLBACK_VALUE

def test_storage_event_init():
    test_event = StorageEvent(
        name=seeds.STORAGE_EVENT_NAME,
        date_time=seeds.STORAGE_EVENT_DATE,
        callback=lambda: callback()
    )

    assert test_event.name == seeds.STORAGE_EVENT_NAME
    assert test_event.expires_at == seeds.STORAGE_EVENT_TIMESTAMP
    assert test_event.callback() == seeds.STORAGE_EVENT_CALLBACK_VALUE

def test_missing_name():
    with pytest.raises(ValueError) as excinfo:
        StorageEvent(
            name=None,
            date_time=seeds.STORAGE_EVENT_DATE,
            callback=lambda: callback()
        )

    assert str(excinfo.value) == ERROR_MESSAGES.MISSING_EVENT_NAME.value

def test_missing_callback():
    with pytest.raises(ValueError) as excinfo:
        StorageEvent(
            name=seeds.STORAGE_EVENT_NAME,
            date_time=seeds.STORAGE_EVENT_DATE,
            callback=None
        )

    assert str(excinfo.value) == ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value

def test_unsupported_timestring_format():
    with pytest.raises(ValueError) as excinfo:
        StorageEvent(
            name=seeds.STORAGE_EVENT_NAME,
            date_time=seeds.STORAGE_EVENT_UNSUPPORTED_DATE,
            callback=lambda: callback()
        )
    
    assert str(excinfo.value) == ERROR_MESSAGES.UNSUPPORTED_DATE_FORMAT.value
