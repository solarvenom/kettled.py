from datetime import datetime
from tests.utils import init_scheduler_set_event, get_future_datetime
from cauldrond.constants.enums import ERROR_MESSAGES
import tests.seeds as seeds

tomorrows_datetime = get_future_datetime(1)
tomorrows_timestamp = int(datetime.timestamp(tomorrows_datetime))

def test_remove_event_success_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    test_instance.remove(seeds.EVENT_NAME)
    assert len(test_instance.storage) == 0
    assert len(test_instance.index) == 0

def test_remove_nonexistent_event_fail_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    try:
        test_instance.remove(seeds.UPDATED_EVENT_NAME)
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.EVENT_NAME_NOT_FOUND.value

def test_remove_event_with_empty_event_name_fail_case():
    test_instance = init_scheduler_set_event(tomorrows_datetime)
    try:
        test_instance.remove("")
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.EVENT_NAME_NOT_FOUND.value