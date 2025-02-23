from datetime import datetime, timedelta
from kettled.constants.enums.relative_datetime_options_enum import RELATIVE_DATETIME_OPTIONS_ENUM
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM
from kettled.utils.next_recurrency_calculator import get_next_datetime
from kettled.constants.enums.recurrency_options_enum import RECURRENCY_OPTIONS_ENUM

def calculate_relative_datetime(current_datetime, relative_datetime_enumerable):
    if relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.ONE_MINUTE:
        return current_datetime + timedelta(minutes=1)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.TWO_MINUTES:
        return current_datetime + timedelta(minutes=2)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.FIVE_MINUTES:
        return current_datetime + timedelta(minutes=5)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.TEN_MINUTES:
        return current_datetime + timedelta(minutes=10)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.THIRTY_MINUTES:
        return current_datetime + timedelta(minutes=30)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.ONE_HOUR:
        return current_datetime + timedelta(hours=1)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.TWO_HOURS:
        return current_datetime + timedelta(hours=2)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.SIX_HOURS:
        return current_datetime + timedelta(hours=6)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.TWELVE_HOURS:
        return current_datetime + timedelta(hours=12)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.ONE_DAY:
        return current_datetime + timedelta(days=1)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.TWO_DAYS:
        return current_datetime + timedelta(days=2)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.ONE_WEEK:
        return current_datetime + timedelta(weeks=1)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.TWO_WEEKS:
        return current_datetime + timedelta(weeks=2)
    elif relative_datetime_enumerable == RELATIVE_DATETIME_OPTIONS_ENUM.ONE_MONTH:
        return get_next_datetime(current_datetime, RECURRENCY_OPTIONS_ENUM.MONTHLY)
    else:
        raise ValueError(ERROR_MESSAGES_ENUM.RELATIVE_DATETIME_CALCULATION_ERROR.value)