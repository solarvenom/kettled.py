from nuthatch.scheduler import Scheduler
from nuthatch.types import StorageEventInput

def test_scheduler_init():
    test_instance = Scheduler()
    assert test_instance.storage == {}
    assert test_instance.index == {}
