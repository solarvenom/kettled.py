from datetime import datetime
from kettled.constants.enums import ERROR_MESSAGES
from tests.utils import get_future_datetime, init_scheduler_set_event
import tests.seeds as seeds

tomorrows_datetime = get_future_datetime(1)
tomorrows_timestamp = int(datetime.timestamp(tomorrows_datetime))
after_tomorrows_datetime = get_future_datetime(2)
after_tomorrows_timestamp = int(datetime.timestamp(after_tomorrows_datetime))

def test_update_event_all_fields_success_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    test_instance.update(
        event_name=seeds.EVENT_NAME,
        new_event_name=seeds.UPDATED_EVENT_NAME,
        new_date_time=str(after_tomorrows_datetime),
        new_callback=seeds.updated_callback)
    try:
        assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    except KeyError:
        assert True
    try:
        assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    except KeyError:
        assert True
    assert test_instance.in_memory_storage[after_tomorrows_timestamp][seeds.UPDATED_EVENT_NAME]()() == seeds.UPDATED_EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.UPDATED_EVENT_NAME] == after_tomorrows_timestamp

def test_update_nonexistend_event_fail_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    try:
        test_instance.update(event_name="somthing else")
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.EVENT_NAME_NOT_FOUND.value

def test_update_event_with_nonunique_new_name_fail_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    test_instance.set(
        event_name=seeds.UPDATED_EVENT_NAME,
        date_time=str(after_tomorrows_datetime),
        callback=seeds.callback)
    try:
        test_instance.update(
            event_name=seeds.EVENT_NAME,
            new_event_name=seeds.UPDATED_EVENT_NAME)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.EVENT_NAME_NOT_UNIQUE.value

def test_update_event_with_name_empty_string_fail_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    try:
        test_instance.update(
            event_name="",
            new_event_name=seeds.UPDATED_EVENT_NAME,
            new_date_time=str(after_tomorrows_datetime),
            new_callback=seeds.updated_callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.MISSING_EVENT_NAME.value

def test_update_event_with_name_none_fail_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    try:
        test_instance.update(
            event_name=None,
            new_event_name=seeds.UPDATED_EVENT_NAME,
            new_date_time=str(after_tomorrows_datetime),
            new_callback=seeds.updated_callback)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.MISSING_EVENT_NAME.value

def test_update_event_datetime_success_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    test_instance.update(
        event_name=seeds.EVENT_NAME,
        new_event_name=None,
        new_date_time=str(after_tomorrows_datetime),
        new_callback=None)
    assert test_instance.in_memory_storage[after_tomorrows_timestamp][seeds.EVENT_NAME]()()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == after_tomorrows_timestamp

def test_update_event_datetime_other_fields_empty_success_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    test_instance.update(
        event_name=seeds.EVENT_NAME,
        new_event_name="",
        new_date_time=str(after_tomorrows_datetime),
        new_callback="")
    assert test_instance.in_memory_storage[after_tomorrows_timestamp][seeds.EVENT_NAME]()()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == after_tomorrows_timestamp

def test_update_event_callback_success_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    test_instance.update(
        event_name=seeds.EVENT_NAME,
        new_event_name=None,
        new_date_time=None,
        new_callback=seeds.updated_callback)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.UPDATED_EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp


def test_update_event_callback_other_fields_empty_success_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    test_instance.update(
        event_name=seeds.EVENT_NAME,
        new_event_name="",
        new_date_time="",
        new_callback=seeds.updated_callback)
    assert test_instance.in_memory_storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.UPDATED_EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp