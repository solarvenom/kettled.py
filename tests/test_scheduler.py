from nuthatch.scheduler import Scheduler

def test_scheduler_init():
    test_instance = Scheduler()
    assert test_instance.storage == {}
    assert test_instance.index == {}
