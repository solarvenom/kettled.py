import pytest
from datetime import datetime, timedelta
from kettled.constants.enums.relative_datetime_options_enum import RELATIVE_DATETIME_OPTIONS_ENUM
from kettled.constants.enums.weekdays_enum import WEEKDAYS_ENUM
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM
from kettled.utils.relative_datetime_calculator import calculate_relative_datetime

@pytest.mark.parametrize("current_datetime, relative_datetime_enumerable, expected", [
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_MINUTE, datetime(2025, 2, 19, 10, 1, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWO_MINUTES, datetime(2025, 2, 19, 10, 2, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.FIVE_MINUTES, datetime(2025, 2, 19, 10, 5, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TEN_MINUTES, datetime(2025, 2, 19, 10, 10, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.THIRTY_MINUTES, datetime(2025, 2, 19, 10, 30, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_HOUR, datetime(2025, 2, 19, 11, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWO_HOURS, datetime(2025, 2, 19, 12, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.SIX_HOURS, datetime(2025, 2, 19, 16, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWELVE_HOURS, datetime(2025, 2, 19, 22, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_DAY, datetime(2025, 2, 20, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWO_DAYS, datetime(2025, 2, 21, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_WEEK, datetime(2025, 2, 26, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.TWO_WEEKS, datetime(2025, 3, 5, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RELATIVE_DATETIME_OPTIONS_ENUM.ONE_MONTH, datetime(2025, 3, 19, 10, 0, 0)),
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
