import pytest
from datetime import datetime, timedelta
from kettled.constants.enums.recurrency_options_enum import RECURRENCY_OPTIONS_ENUM
from kettled.constants.enums.weekdays_enum import WEEKDAYS_ENUM
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM
from kettled.utils.next_recurrency_calculator import get_next_datetime

@pytest.mark.parametrize("current_datetime, recurrency, expected", [
    ("2025-02-19T10:00:00", RECURRENCY_OPTIONS_ENUM.HOURLY.value, datetime(2025, 2, 19, 11, 0, 0)),
    ("2025-02-19T10:00:00", RECURRENCY_OPTIONS_ENUM.DAILY.value, datetime(2025, 2, 20, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EVERY_MONDAY.value, datetime(2025, 2, 24, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EVERY_TUESDAY.value, datetime(2025, 2, 25, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EVERY_WEDNESDAY.value, datetime(2025, 2, 26, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EVERY_THURSDAY.value, datetime(2025, 2, 20, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EVERY_FRIDAY.value, datetime(2025, 2, 21, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EVERY_SATURDAY.value, datetime(2025, 2, 22, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EVERY_SUNDAY.value, datetime(2025, 2, 23, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_MONDAY.value, datetime(2025, 3, 3, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_TUESDAY.value, datetime(2025, 3, 4, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_WEDNESDAY.value, datetime(2025, 3, 5, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_THURSDAY.value, datetime(2025, 3, 6, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_FRIDAY.value, datetime(2025, 3, 7, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_SATURDAY.value, datetime(2025, 3, 8, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_SUNDAY.value, datetime(2025, 3, 9, 10, 0, 0)),
    ("2025-02-19T10:00:00", RECURRENCY_OPTIONS_ENUM.MONTHLY.value, datetime(2025, 3, 19, 10, 0, 0)),
    (datetime(2025, 1, 31, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.MONTHLY.value, datetime(2025, 3, 31, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FIRST_DAY_OF_THE_MONTH.value, datetime(2025, 3, 1, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.SECOND_DAY_OF_THE_MONTH.value, datetime(2025, 3, 2, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.THIRD_DAY_OF_THE_MONTH.value, datetime(2025, 3, 3, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FOURTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 4, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FIFTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 5, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.SIXTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 6, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.SEVENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 7, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EIGHTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 8, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.NINTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 9, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 10, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.ELEVENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 11, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWELFTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 12, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.THIRTEENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 13, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FOURTEENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 14, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FIFTEENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 15, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.SIXTEENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 16, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.SEVENTEENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 17, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.EIGHTEENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 18, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.NINETEENTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 19, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTIETH_DAY_OF_THE_MONTH.value, datetime(2025, 2, 20, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_FIRST_DAY_OF_THE_MONTH.value, datetime(2025, 2, 21, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_SECOND_DAY_OF_THE_MONTH.value, datetime(2025, 2, 22, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_SECOND_DAY_OF_THE_MONTH.value, datetime(2025, 2, 22, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_THIRD_DAY_OF_THE_MONTH.value, datetime(2025, 2, 23, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_FOURTH_DAY_OF_THE_MONTH.value, datetime(2025, 2, 24, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_FIFTH_DAY_OF_THE_MONTH.value, datetime(2025, 2, 25, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_SIXTH_DAY_OF_THE_MONTH.value, datetime(2025, 2, 26, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_SEVENTH_DAY_OF_THE_MONTH.value, datetime(2025, 2, 27, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_EIGHTH_DAY_OF_THE_MONTH.value, datetime(2025, 2, 28, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.TWENTY_NINTH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 29, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.THIRTIETH_DAY_OF_THE_MONTH.value, datetime(2025, 3, 30, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.THIRTY_FIRST_DAY_OF_THE_MONTH.value, datetime(2025, 3, 31, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FIRST_DAY_OF_THE_MONTH.value, datetime(2025, 3, 1, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.LAST_DAY_OF_THE_MONTH.value, datetime(2025, 2, 28, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.SECOND_TO_LAST_DAY_OF_THE_MONTH.value, datetime(2025, 2, 27, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.THIRD_TO_LAST_DAY_OF_THE_MONTH.value, datetime(2025, 2, 26, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FORTH_TO_LAST_DAY_OF_THE_MONTH.value, datetime(2025, 2, 25, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.FIFTH_TO_LAST_DAY_OF_THE_MONTH.value, datetime(2025, 2, 24, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.SIXTH_TO_LAST_DAY_OF_THE_MONTH.value, datetime(2025, 2, 23, 10, 0, 0)),
    (datetime(2025, 2, 19, 10, 0, 0), RECURRENCY_OPTIONS_ENUM.SEVENTH_TO_LAST_DAY_OF_THE_MONTH.value, datetime(2025, 2, 22, 10, 0, 0)),
])

def test_get_next_datetime(current_datetime, recurrency, expected):
    if isinstance(current_datetime, str):
        current_datetime = datetime.fromisoformat(current_datetime)
    result = get_next_datetime(current_datetime, recurrency)
    assert result == expected, f"Expected {expected} but got {result}"

def test_get_next_datetime_invalid_recurrency():
    with pytest.raises(ValueError) as excinfo:
        get_next_datetime(datetime(2025, 2, 19, 10, 0, 0), "INVALID_RECURRING_ENUMERABLE")
    assert str(excinfo.value) == ERROR_MESSAGES_ENUM.NEXT_RECURRENCY_CALCULATION_ERROR.value
