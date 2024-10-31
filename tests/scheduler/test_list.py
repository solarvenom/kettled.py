import pytest
from datetime import datetime
from cauldrond.scheduler import Scheduler
from tests.utils import init_scheduler_set_event, get_tomorrows_datetime
from cauldrond.constants.enums import ERROR_MESSAGES
import tests.seeds as seeds

tomorrows_datetime = get_tomorrows_datetime()
tomorrows_timestamp = int(datetime.timestamp(tomorrows_datetime))

@pytest.mark.skip(reason="skip untill stderr is properly captured")
def test_list_success_case(capsys):
    test_instance = init_scheduler_set_event(tomorrows_datetime)

    ISOFORMAT = datetime.fromtimestamp(tomorrows_timestamp).isoformat()
    test_instance.list()
    captured = capsys.readouterr()
    expected_stdout = "\n_______________________________________________________\n"
    expected_stdout += ('| {:^5} | {:^20} | {:^20} |\n'.format(*["1", seeds.EVENT_NAME, ISOFORMAT]))
    expected_stdout += "|_______|______________________|______________________|\n"
    assert captured.out == expected_stdout

@pytest.mark.skip(reason="skip untill stderr is properly captured")
def test_list_empty_storage_fail_case(capsys):
    test_instance = Scheduler()

    try:
        test_instance.list()
    except ValueError as error:
        assert str(error) == ERROR_MESSAGES.NO_EVENTS_SCHEDULED.value