from datetime import datetime
from cauldrond.scheduler import Scheduler
from cauldrond.constants.enums import EVENT_PARAMETERS
from tests.utils import get_future_datetime
import tests.seeds as seeds

tomorrows_date_time = get_future_datetime(1)
tomorrows_timestamp = int(datetime.timestamp(tomorrows_date_time))

def test_get_success_case():
    test_instance = Scheduler()
    test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_date_time), callback=seeds.callback)
    assert test_instance.storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    added_event = test_instance.get(seeds.EVENT_NAME)
    assert added_event[EVENT_PARAMETERS.EVENT_NAME.value] == seeds.EVENT_NAME
    assert added_event[EVENT_PARAMETERS.DATE_TIME.value] == tomorrows_timestamp
    assert added_event[EVENT_PARAMETERS.CALLBACK.value]()() == seeds.EVENT_CALLBACK_VALUE

def test_get_fail_case():
    test_instance = Scheduler()
    test_instance.set(event_name=seeds.EVENT_NAME, date_time=str(tomorrows_date_time), callback=seeds.callback)
    assert test_instance.storage[tomorrows_timestamp][seeds.EVENT_NAME]()() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == tomorrows_timestamp
    try:
        test_instance.get(seeds.INCORRECT_EVENT_NAME)
    except KeyError:
        assert True