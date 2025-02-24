from kettled.daemon.scheduler import Scheduler

def test_init_success_case():
    test_instance = Scheduler(in_memory_only_session=True)
    assert test_instance.in_memory_storage == {}
    assert test_instance.index == {}