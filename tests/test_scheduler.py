from nuthatch.scheduler import Scheduler
import seeds

def test_scheduler_init():
    test_instance = Scheduler()
    assert test_instance.storage == {}
    assert test_instance.index == {}

def test_scheduler_set():
    test_instance = Scheduler()
    test_instance.set(
        name=seeds.EVENT_NAME,
        date_time=seeds.EVENT_DATE,
        callback=seeds.EVENT_CALLBACK()
    )
    
    assert test_instance.storage[seeds.EVENT_TIMESTAMP][seeds.EVENT_NAME]() == seeds.EVENT_CALLBACK_VALUE
    assert test_instance.index[seeds.EVENT_NAME] == seeds.EVENT_TIMESTAMP