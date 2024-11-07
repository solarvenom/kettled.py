import pytest
from datetime import datetime
from kettled.daemon.scheduler import Scheduler
from kettled.constants.enums import ERROR_MESSAGES
from tests.utils import get_future_datetime
import tests.seeds as seeds

tomorrows_datetime = get_future_datetime(1)
tomorrows_timestamp = int(datetime.timestamp(tomorrows_datetime))

def test_set_event_success_case():
    test_instance = Scheduler()
    test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_datetime), callback=seeds.callback)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp

def test_set_event_with_duplicate_name_fail_case():
    test_instance = Scheduler()
    test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_datetime), callback=seeds.callback)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    try:
        test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_datetime), callback=seeds.callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.EVENT_NAME_NOT_UNIQUE.value

def test_set_event_with_none_name_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name=None, date_time=str(tomorrows_datetime), callback=seeds.callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.MISSING_EVENT_NAME.value

def test_set_event_with_name_empty_string_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name="", date_time=str(tomorrows_datetime), callback=seeds.callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.MISSING_EVENT_NAME.value

def test_set_event_with_datetime_none_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name=seeds.EVENT_NAME, date_time=None, callback=seeds.callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.MISSING_EVENT_DATETIME.value

def test_set_event_with_datetime_empty_string_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name=seeds.EVENT_NAME, date_time="", callback=seeds.callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.UNSUPPORTED_DATE_FORMAT.value

def test_set_event_with_datetime_timestamp_integer_success_case():
    test_instance = Scheduler()
    test_instance.set(event_name=seeds.EVENT_NAME, date_time=tomorrows_timestamp, callback=seeds.callback)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp

def test_set_event_with_datetime_timestamp_string_success_case():
    test_instance = Scheduler()
    test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_timestamp), callback=seeds.callback)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp

def test_set_event_with_unsupported_datetime_formate_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name=seeds.EVENT_NAME, date_time=seeds.EVENT_UNSUPPORTED_DATE, callback=seeds.callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.UNSUPPORTED_DATE_FORMAT.value

@pytest.mark.skip(reason="skip untill .set() function datetime input rework")
def test_set_event_with_outdated_datetime_timestamp_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(seeds.OUTDATED_EVENT_TIMESTAMP), callback=seeds.callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.TIMESTAMP_OUTDATED.value

def test_set_event_with_outdated_datetime_string_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(seeds.OUTDATED_EVENT_DATE), callback=seeds.callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.TIMESTAMP_OUTDATED.value

def test_set_event_with_callback_none_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_timestamp), callback=None)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value

def test_set_event_with_callback_empty_string_fail_case():
    test_instance = Scheduler()
    try:
        test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_timestamp), callback="")
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value

def test_set_event_with_existing_name_with_spaces_fail_case():
    test_instance = Scheduler()
    test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_timestamp), callback="")
    try:
        test_instance.set(event_name="    "+seeds.EVENT_NAME+"     ", date_time=str(tomorrows_timestamp), callback="")
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.EVENT_NAME_NOT_UNIQUE.value
