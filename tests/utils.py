from datetime import datetime, timedelta
from cauldrond.scheduler import Scheduler
import tests.seeds as seeds

def init_scheduler_set_event(event_datetime):
    test_instance = Scheduler()
    test_instance.set(
        event_name=seeds.EVENT_NAME,
        date_time=str(event_datetime),
        callback=seeds.callback
    )
    return test_instance

def get_tomorrows_datetime():
    tomorrows_date_time = datetime.now() + timedelta(days=1)
    return datetime.strptime(str(tomorrows_date_time), "%Y-%m-%d %H:%M:%S.%f")
