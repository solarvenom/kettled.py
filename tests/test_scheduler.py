from datetime import datetime
from cauldrond.scheduler import Scheduler
import seeds

def init_scheduler_set_event():
    test_instance = Scheduler()
    test_instance.set(
        event_name=seeds.EVENT_NAME,
        date_time=seeds.EVENT_DATE,
        callback=seeds.EVENT_CALLBACK()
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

def test_list(capsys):
    test_instance = init_scheduler_set_event()

    ISOFORMAT = datetime.fromtimestamp(seeds.EVENT_TIMESTAMP).isoformat()
    test_instance.list()
    captured = capsys.readouterr()
    assert captured.out == f"| 1 | {seeds.EVENT_NAME} | {ISOFORMAT} |\n"

def test_remove():
    test_instance = init_scheduler_set_event()
    assert test_instance.storage[seeds.EVENT_TIMESTAMP][seeds.EVENT_NAME]() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == seeds.EVENT_TIMESTAMP
    test_instance.remove(seeds.EVENT_NAME)
    assert len(test_instance.storage) == 0
    assert len(test_instance.index) == 0