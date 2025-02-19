from datetime import datetime, timedelta
from kettled.constants.enums.recurrency_options_enum import RECURRENCY_OPTIONS_ENUM
from kettled.constants.enums.weekdays_num import WEEKDAYS_ENUM

def get_next_datetime(current_datetime, recurrency):
    if isinstance(current_datetime, str):
        current_datetime = datetime.fromisoformat(current_datetime)

    if recurrency == RECURRENCY_OPTIONS_ENUM.HOURLY:
        return current_datetime + timedelta(hours=1)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.DAILY:
        return current_datetime + timedelta(days=1)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.EVERY_MONDAY:
        return get_next_weekday(current_datetime, WEEKDAYS_ENUM.MONDAY)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.EVERY_TUESDAY:
        return get_next_weekday(current_datetime, WEEKDAYS_ENUM.TUESDAY)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.EVERY_WEDNESDAY:
        return get_next_weekday(current_datetime, WEEKDAYS_ENUM.WEDNESDAY)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.EVERY_THURSDAY:
        return get_next_weekday(current_datetime, WEEKDAYS_ENUM.THURSDAY)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.EVERY_FRIDAY:
        return get_next_weekday(current_datetime, WEEKDAYS_ENUM.FRIDAY)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.EVERY_SATURDAY:
        return get_next_weekday(current_datetime, WEEKDAYS_ENUM.SATURDAY)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.EVERY_SUNDAY:
        return get_next_weekday(current_datetime, WEEKDAYS_ENUM.SUNDAY)
    
    if recurrency == RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_MONDAY:
        fortnight_week = current_datetime + timedelta(weeks=2)
        return get_next_weekday(fortnight_week, WEEKDAYS_ENUM.MONDAY)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_TUESDAY:
        fortnight_week = current_datetime + timedelta(weeks=2)
        return get_next_weekday(fortnight_week, WEEKDAYS_ENUM.TUESDAY)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_WEDNESDAY:
        fortnight_week = current_datetime + timedelta(weeks=2)
        return get_next_weekday(fortnight_week, WEEKDAYS_ENUM.WEDNESDAY)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_THURSDAY:
        fortnight_week = current_datetime + timedelta(weeks=2)
        return get_next_weekday(fortnight_week, WEEKDAYS_ENUM.THURSDAY)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_FRIDAY:
        fortnight_week = current_datetime + timedelta(weeks=2)
        return get_next_weekday(fortnight_week, WEEKDAYS_ENUM.FRIDAY)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_SATURDAY:
        fortnight_week = current_datetime + timedelta(weeks=2)
        return get_next_weekday(fortnight_week, WEEKDAYS_ENUM.SATURDAY)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.FORTNIGHTLY_SUNDAY:
        fortnight_week = current_datetime + timedelta(weeks=2)
        return get_next_weekday(fortnight_week, WEEKDAYS_ENUM.SUNDAY)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.FIRST_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 1)
    
    elif recurrency == RECURRENCY_OPTIONS_ENUM.SECOND_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 2)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.THIRD_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 3)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.FOURTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 4)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.FIFTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 5)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.SIXTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 6)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.SEVENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 7)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.EIGHTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 8)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.NINTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 9)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 10)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.ELEVENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 11)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWELFTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 12)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.THIRTEENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 13)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.FOURTEENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 14)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.FIFTEENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 15)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.SIXTEENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 16)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.SEVENTEENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 17)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.EIGHTEENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 18)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.NINETEENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 19)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTIETH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 20)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_FIRST_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 21)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_SECOND_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 22)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_THIRD_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 23)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_FOURTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 24)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_FIFTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 25)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_SIXTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 26)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_SEVENTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 27)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_EIGHTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 28)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.TWENTY_NINTH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 29)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.THIRTIETH_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 30)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.THIRTY_FIRST_DAY_OF_THE_MONTH:
        return get_next_specific_day_of_the_month(current_datetime, 31)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.LAST_DAY_OF_THE_MONTH:
        return get_last_day_of_the_month(current_datetime.year, current_datetime.month)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.SECOND_TO_LAST_DAY_OF_THE_MONTH:
        return get_nth_to_last_day_of_the_month(current_datetime, 2)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.THIRD_TO_LAST_DAY_OF_THE_MONTH:
        return get_nth_to_last_day_of_the_month(current_datetime, 3)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.FORTH_TO_LAST_DAY_OF_THE_MONTH:
        return get_nth_to_last_day_of_the_month(current_datetime, 4)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.FIFTH_TO_LAST_DAY_OF_THE_MONTH:
        return get_nth_to_last_day_of_the_month(current_datetime, 5)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.SIXTH_TO_LAST_DAY_OF_THE_MONTH:
        return get_nth_to_last_day_of_the_month(current_datetime, 6)

    elif recurrency == RECURRENCY_OPTIONS_ENUM.SEVENTH_TO_LAST_DAY_OF_THE_MONTH:
        return get_nth_to_last_day_of_the_month(current_datetime, 7)

    else:
        raise ValueError(f"Unsupported recurrency: {recurrency}")

def get_next_specific_day_of_the_month(current_datetime, day_of_month):
    year = current_datetime.year
    month = current_datetime.month
    
    if day_of_month > 28:
        last_day_of_current_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day
        if day_of_month > last_day_of_current_month:
            month += 1
            if month > 12:
                month = 1
                year += 1
    
    next_occurrence = datetime(year, month, day_of_month)
    
    if next_occurrence <= current_datetime:
        month += 1
        if month > 12:
            month = 1
            year += 1
        next_occurrence = datetime(year, month, day_of_month)
    
    return next_occurrence

def get_next_weekday(current_datetime, weekday):
    days_ahead = weekday - current_datetime.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return current_datetime + timedelta(days=days_ahead)

def get_last_day_of_the_month(current_datetime):
    year = current_datetime.year
    month = current_datetime.month

    next_month = month + 1 if month < 12 else 1
    year_for_next_month = year if month < 12 else year + 1
    last_day_of_current_month = (datetime(year_for_next_month, next_month, 1) - timedelta(days=1))

    if current_datetime.date() == last_day_of_current_month.date():
        return (datetime(year_for_next_month, next_month + 1 if next_month < 12 else 1, 1) - timedelta(days=1))
    
    return last_day_of_current_month

def get_nth_to_last_day_of_the_month(current_datetime, n):
    last_day = get_last_day_of_the_month(current_datetime)
    nth_to_last_day = last_day - timedelta(days=(n - 1))
    
    if current_datetime > nth_to_last_day:
        next_month = current_datetime.month + 1 if current_datetime.month < 12 else 1
        year_for_next_month = current_datetime.year if current_datetime.month < 12 else current_datetime.year + 1
        last_day_of_next_month = (datetime(year_for_next_month, next_month + 1 if next_month < 12 else 1, 1) - timedelta(days=1))
        nth_to_last_day = last_day_of_next_month - timedelta(days=(n - 1))
    
    return nth_to_last_day