from sys import stderr, stdout
from typing import Callable
import re
from datetime import datetime
from kettled.constants.date_formats import DATE_FORMATS
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM
from kettled.constants.enums.event_parameters_enum import EVENT_PARAMETERS_ENUM
from kettled.constants.enums.repository_event_parameters_enum import REPOSITORY_EVENT_PARAMETERS_ENUM
from kettled.constants.enums.recurrency_options_enum import RECURRENCY_OPTIONS_ENUM
from kettled.constants.enums.fallback_options_enum import FALLBACK_DIRECTIVES_ENUM
from kettled.database.event_repository import EventRepository
from kettled.utils.next_recurrency_calculator import calculate_next_recurrency

class Scheduler:
    def __init__(self, in_memory_only_session=False):
        self.in_memory_storage: dict[int, dict[str, dict]] = {}
        self.index: dict[str, int] = {}
        self.in_memory_only_session: bool = in_memory_only_session
        self.event_repository: EventRepository
        if self.in_memory_only_session != True:
            self.event_repository = EventRepository()
            stored_events = self.event_repository.get_all_events()

            now = datetime.now().timestamp()
            outdated_events = [event for event in stored_events if event[REPOSITORY_EVENT_PARAMETERS_ENUM.TIMESTAMP.value] < now and event[REPOSITORY_EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value] != FALLBACK_DIRECTIVES_ENUM.IGNORE.value]
            events_to_schedule = [event for event in stored_events if event[REPOSITORY_EVENT_PARAMETERS_ENUM.TIMESTAMP.value] >= now]

            try:
                for outdated_event in outdated_events:
                    fallback_directive = outdated_event[REPOSITORY_EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value]
                    if fallback_directive == FALLBACK_DIRECTIVES_ENUM.EXECUTE_AS_SOON_AS_POSSIBLE.value:
                        self.execute_event(outdated_event, remove_after_execution=False)
                    elif fallback_directive == FALLBACK_DIRECTIVES_ENUM.EXECUTE_ON_NEXT_RECURRENCY.value:
                        next_recurrency = calculate_next_recurrency(now, outdated_event[REPOSITORY_EVENT_PARAMETERS_ENUM.RECURRENCY.value])
                        self.set(
                            event_name=outdated_event[REPOSITORY_EVENT_PARAMETERS_ENUM.EVENT_NAME.value],
                            date_time=next_recurrency,
                            recurrency=outdated_event[REPOSITORY_EVENT_PARAMETERS_ENUM.RECURRENCY.value],
                            fallback_directive=outdated_event[REPOSITORY_EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value],
                            callback=outdated_event[REPOSITORY_EVENT_PARAMETERS_ENUM.CALLBACK.value],
                        )
                for event_to_schedule in events_to_schedule:
                    self.set(
                        event_name=event[REPOSITORY_EVENT_PARAMETERS_ENUM.EVENT_NAME.value],
                        date_time=event[REPOSITORY_EVENT_PARAMETERS_ENUM.TIMESTAMP.value],
                        recurrency=event[REPOSITORY_EVENT_PARAMETERS_ENUM.RECURRENCY.value],
                        fallback_directive=event[REPOSITORY_EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value],
                        callback=event[REPOSITORY_EVENT_PARAMETERS_ENUM.CALLBACK.value],
                        store_in_db=False)
            except KeyError:
                pass
    
    @staticmethod
    def get_timestamp(date) -> int:
        # TODO: refactor this
        try:
            date_time = int(date)
            if datetime.timestamp(datetime.now()) > date_time:
                raise ValueError(ERROR_MESSAGES_ENUM.TIMESTAMP_OUTDATED.value)
            return date_time
        except ValueError:
            matched_format = None
            for pattern in DATE_FORMATS.keys():
                if re.match(pattern, date):
                    matched_format = int(datetime.timestamp(datetime.strptime(date, DATE_FORMATS[pattern])))
                    break
            if matched_format == None:
                raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_DATE_FORMAT.value)
            return matched_format

    def get(self, event_name):
        if event_name == None or event_name == "":
            raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
        timestamp = self.index[event_name]
        if timestamp == None:
            raise ValueError(ERROR_MESSAGES_ENUM.EVENT_NAME_NOT_FOUND.value)
        event = self.in_memory_storage[timestamp][event_name]
        recurrency = event[EVENT_PARAMETERS_ENUM.RECURRENCY.value]
        fallback_directive = event[EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value]
        callback = event[EVENT_PARAMETERS_ENUM.CALLBACK.value]
        return { 
            EVENT_PARAMETERS_ENUM.EVENT_NAME.value: event_name, 
            EVENT_PARAMETERS_ENUM.DATE_TIME.value: timestamp,
            EVENT_PARAMETERS_ENUM.RECURRENCY.value: recurrency,
            EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value: fallback_directive,
            EVENT_PARAMETERS_ENUM.CALLBACK.value: callback }

    def set(
        self,
        event_name, 
        date_time, 
        recurrency, 
        fallback_directive, 
        callback,
        store_in_db=True) -> None:
        if event_name == None or event_name == "":
            raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
        if event_name in self.index.keys():
            raise ValueError(ERROR_MESSAGES_ENUM.EVENT_NAME_NOT_UNIQUE.value)

        if date_time == None or date_time == "":
            raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_DATETIME.value)

        if recurrency == None or recurrency == "":
            recurrency = RECURRENCY_OPTIONS_ENUM.NOT_RECURRING.value

        if fallback_directive == None or fallback_directive == "":
            fallback_directive = FALLBACK_DIRECTIVES_ENUM.EXECUTE_AS_SOON_AS_POSSIBLE.value

        if callback == None:
            raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_CALLBACK.value)

        timestamp = self.get_timestamp(date_time)
        current_timestamp = int(datetime.now().timestamp())
        if current_timestamp > timestamp:
            raise ValueError(ERROR_MESSAGES_ENUM.TIMESTAMP_OUTDATED.value)
        if timestamp not in self.in_memory_storage:
            self.in_memory_storage[timestamp] = {}
        self.in_memory_storage[timestamp][event_name] = {}
        self.in_memory_storage[timestamp][event_name][EVENT_PARAMETERS_ENUM.RECURRENCY.value] = recurrency
        self.in_memory_storage[timestamp][event_name][EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value] = fallback_directive
        self.in_memory_storage[timestamp][event_name][EVENT_PARAMETERS_ENUM.CALLBACK.value] = lambda: self.wrap_callback(callback)
        self.index[event_name] = timestamp
        if self.in_memory_only_session != True and store_in_db == True:
            self.event_repository.insert_event(
                event_name=event_name,
                timestamp=timestamp,
                recurrency=recurrency,
                fallback_directive=fallback_directive,
                callback=f"{self.wrap_callback(callback)}")

    def list(self) -> None:
        event_list: list[list] = []
        event_index = 1
        if len(self.index) == 0:
            stderr.write(ERROR_MESSAGES_ENUM.NO_EVENTS_SCHEDULED.value)
        else:
            for event_name, timestamp in self.index.items():
                event_list.append([
                    event_index, 
                    event_name, 
                    datetime.fromtimestamp(timestamp).isoformat(),
                    self.in_memory_storage[timestamp][event_name][EVENT_PARAMETERS_ENUM.RECURRENCY.value],
                    self.in_memory_storage[timestamp][event_name][EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value]])
                event_index += 1
            list_str = "\n_______________________________________________________________________________________________________________________\n"
            list_str += ('| {:^5} | {:^30} | {:^22} | {:^20} | {:^27} |\n'.format(*[
                "Index", 
                "Event Name", 
                "Scheduled Date & Time", 
                "Recurrency",
                "Fallback Directive"]))
            list_str += "|----------------------------------------------------------------------------------------------------------------------|\n"
            for event in event_list:
                list_str += ('| {:^5} | {:^30} | {:^22} | {:^20} | {:^25} |\n'.format(*event))
            list_str += "|_______|________________________________|________________________|______________________|_____________________________|\n"
            list_str += "\n"
            stdout.write(list_str)

    def remove(self, event_name) -> None:
        if event_name not in self.index.keys():
            raise ValueError(ERROR_MESSAGES_ENUM.EVENT_NAME_NOT_FOUND.value)
        event_timestamp = self.index[event_name]
        if len(self.in_memory_storage[event_timestamp]) > 1:
            self.in_memory_storage[event_timestamp].pop(event_name)
        else:
            self.in_memory_storage.pop(event_timestamp)
        self.index.pop(event_name)
        if self.in_memory_only_session != True:
            self.event_repository.delete_event_by_name(event_name=event_name)

    def update(
        self,
        event_name,
        new_event_name=None,
        new_date_time=None,
        new_recurrency=None,
        new_fallback_directive=None,
        new_callback=None
        ) -> None:
        if event_name == None or event_name == "":
            raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
        if event_name not in self.index.keys():
            raise ValueError(ERROR_MESSAGES_ENUM.EVENT_NAME_NOT_FOUND.value)
        event_to_update = self.get(event_name)

        if new_event_name != None and new_event_name != "":
            event_to_update[EVENT_PARAMETERS_ENUM.EVENT_NAME.value] = new_event_name

        if new_date_time != None and new_date_time != "":
            event_to_update[EVENT_PARAMETERS_ENUM.DATE_TIME.value] = new_date_time

        if new_recurrency != None and new_recurrency != "":
            if new_recurrency not in RECURRENCY_OPTIONS_ENUM.list():
                raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_RECURRENCY_OPTION.value)
            event_to_update[EVENT_PARAMETERS_ENUM.RECURRENCY.value] = new_recurrency

        if new_fallback_directive != None and new_fallback_directive != "":
            if new_fallback_directive not in FALLBACK_DIRECTIVES_ENUM.list():
                raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_FALLBACK_DIRECTIVE.value)
            event_to_update[EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value] = new_fallback_directive

        if new_callback != None and new_callback != "":
            event_to_update[EVENT_PARAMETERS_ENUM.CALLBACK.value] = new_callback

        self.remove(event_name)
        self.set(
            event_name=event_to_update[EVENT_PARAMETERS_ENUM.EVENT_NAME.value], 
            date_time=event_to_update[EVENT_PARAMETERS_ENUM.DATE_TIME.value],
            recurrency=event_to_update[EVENT_PARAMETERS_ENUM.RECURRENCY.value],
            fallback_directive=event_to_update[EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value],
            callback=event_to_update[EVENT_PARAMETERS_ENUM.CALLBACK.value])
        if self.in_memory_only_session != True:
            self.event_repository.update_event_by_name(
                event_name=event_name,
                new_event_name=event_to_update[EVENT_PARAMETERS_ENUM.EVENT_NAME.value],
                new_timestamp=event_to_update[EVENT_PARAMETERS_ENUM.DATE_TIME.value],
                new_recurrency=event_to_update[EVENT_PARAMETERS_ENUM.RECURRENCY.value],
                new_fallback_directive=event_to_update[EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value],
                new_callback=f"{event_to_update[EVENT_PARAMETERS_ENUM.CALLBACK.value]}")
    
    @staticmethod
    def wrap_callback(event_callback) -> Callable:
        return event_callback

    def execute_event(self, event, remove_after_execution=True):
        eval(event[EVENT_PARAMETERS_ENUM.CALLBACK.value])

        if remove_after_execution:
            self.remove(event_name=event[EVENT_PARAMETERS_ENUM.EVENT_NAME.value])

        if event[EVENT_PARAMETERS_ENUM.RECURRENCY.value] != RECURRENCY_OPTIONS_ENUM.NOT_RECURRING.value:
            next_date_time = calculate_next_recurrency(event[EVENT_PARAMETERS_ENUM.DATE_TIME.value], event[EVENT_PARAMETERS_ENUM.RECURRENCY.value])
            self.set(
                event_name = event[EVENT_PARAMETERS_ENUM.EVENT_NAME.value],
                date_time = next_date_time,
                recurrency = event[EVENT_PARAMETERS_ENUM.RECURRENCY.value],
                fallback_directive = event[EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value],
                callback = event[EVENT_PARAMETERS_ENUM.CALLBACK.value]
            )