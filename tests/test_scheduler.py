from datetime import datetime
from cauldrond.scheduler import Scheduler
from cauldrond.constants.enums import EVENT_PARAMETERS
import seeds

def init_scheduler_set_event():
    test_instance = Scheduler()
    test_instance.set(
        event_name=seeds.EVENT_NAME,
        date_time=seeds.EVENT_DATE,
        callback=seeds.callback()
    )
    return test_instance

def test_init():
    test_instance = Scheduler()
    assert test_instance.storage == {}
    assert test_instance.index == {}

def test_set():
    test_instance = init_scheduler_set_event()
    
    assert test_instance.storage[seeds.EVENT_TIMESTAMP][seeds.EVENT_NAME]() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == seeds.EVENT_TIMESTAMP

# def test_list(capsys):
#     test_instance = init_scheduler_set_event()

#     ISOFORMAT = datetime.fromtimestamp(seeds.EVENT_TIMESTAMP).isoformat()
#     test_instance.list()
#     captured = capsys.readouterr()
#     expected_stdout = "\n_______________________________________________________\n"
#     expected_stdout += ('| {:^5} | {:^20} | {:^20} |\n'.format(*["1", seeds.EVENT_NAME, ISOFORMAT]))
#     expected_stdout += "|_______|______________________|______________________|\n"
#     assert captured.out == expected_stdout

def test_remove():
    test_instance = init_scheduler_set_event()
    assert test_instance.storage[seeds.EVENT_TIMESTAMP][seeds.EVENT_NAME]() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == seeds.EVENT_TIMESTAMP
    test_instance.remove(seeds.EVENT_NAME)
    assert len(test_instance.storage) == 0
    assert len(test_instance.index) == 0

def test_get():
    test_instance = init_scheduler_set_event()
    assert test_instance.storage[seeds.EVENT_TIMESTAMP][seeds.EVENT_NAME]() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == seeds.EVENT_TIMESTAMP
    set_event = test_instance.get(seeds.EVENT_NAME)
    assert set_event[EVENT_PARAMETERS.EVENT_NAME.value] == seeds.EVENT_NAME
    assert set_event[EVENT_PARAMETERS.DATE_TIME.value] == seeds.EVENT_TIMESTAMP
    assert set_event[EVENT_PARAMETERS.CALLBACK.value]() == seeds.EVENT_CALLBACK_VALUE

def test_update():
    test_instance = init_scheduler_set_event()
    assert test_instance.storage[seeds.EVENT_TIMESTAMP][seeds.EVENT_NAME]() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == seeds.EVENT_TIMESTAMP
    test_instance.update(
        event_name=seeds.EVENT_NAME, 
        new_event_name = seeds.UPDATED_EVENT_NAME,
        new_date_time=seeds.UPDATED_EVENT_DATE,
        new_callback=seeds.updated_callback())
    assert test_instance.storage[seeds.UPDATED_EVENT_TIMESTAMP][seeds.UPDATED_EVENT_NAME]() == seeds.UPDATED_EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.UPDATED_EVENT_NAME] == seeds.UPDATED_EVENT_TIMESTAMP
