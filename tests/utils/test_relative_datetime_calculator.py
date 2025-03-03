import pytest
from datetime import datetime, timedelta
from kettled.constants import RELATIVE_DATETIME_OPTIONS_ENUM, WEEKDAYS_ENUM, ERROR_MESSAGES_ENUM
from kettled.utils import calculate_relative_datetime

@pytest.mark.parametrize("current_datetime, relative_datetime_enumerable, expected", [
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_MINUTE.value, datetime(2025, 2, 19, 10, 1, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWO_MINUTES.value, datetime(2025, 2, 19, 10, 2, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.FIVE_MINUTES.value, datetime(2025, 2, 19, 10, 5, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TEN_MINUTES.value, datetime(2025, 2, 19, 10, 10, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.THIRTY_MINUTES.value, datetime(2025, 2, 19, 10, 30, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_HOUR.value, datetime(2025, 2, 19, 11, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWO_HOURS.value, datetime(2025, 2, 19, 12, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.SIX_HOURS.value, datetime(2025, 2, 19, 16, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWELVE_HOURS.value, datetime(2025, 2, 19, 22, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_DAY.value, datetime(2025, 2, 20, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWO_DAYS.value, datetime(2025, 2, 21, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_WEEK.value, datetime(2025, 2, 26, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWO_WEEKS.value, datetime(2025, 3, 5, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_MONTH.value, datetime(2025, 3, 19, 10, 0, 0)),
])

def test_calculate_relative_datetime(current_datetime, relative_datetime_enumerable, expected):
    if isinstance(current_datetime, str):
        current_datetime = datetime.fromisoformat(current_datetime)
    result = calculate_relative_datetime(current_datetime, relative_datetime_enumerable)
    assert result == expected, f"Expected {expected} but got {result}"

def test_calculate_relative_datetime_invalid_recurrency():
    with pytest.raises(ValueError) as excinfo:
        calculate_relative_datetime(datetime(2025, 2, 19, 10, 0, 0), "INVALID_RELATIVE_DATETIME_ENUMARABLE")
    assert str(excinfo.value) == ERROR_MESSAGES_ENUM.RELATIVE_DATETIME_CALCULATION_ERROR.value
