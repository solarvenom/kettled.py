from sys import stderr, stdout
from typing import Callable
import re
from datetime import datetime
from kettled.constants.date_formats import DATE_FORMATS
from kettled.constants.enums import ERROR_MESSAGES, EVENT_PARAMETERS, REPOSITORY_EVENT_PARAMETERS
from kettled.database.event_repository import EventRepository

class Scheduler:
    def __init__(self, persistent_session=False):
        self.in_memory_storage: dict[int, dict] = {}
        self.index: dict[str, int] = {}
        self.persistent_session: bool = persistent_session
        self.event_repository: EventRepository
        if self.persistent_session:
            self.event_repository = EventRepository()
            scheduled_events = self.event_repository.get_all_events()
            for event in scheduled_events:
                self.set(
                    event_name=event[REPOSITORY_EVENT_PARAMETERS.EVENT_NAME.value],
                    date_time=event[REPOSITORY_EVENT_PARAMETERS.TIMESTAMP.value],
                    callback=event[REPOSITORY_EVENT_PARAMETERS.CALLBACK.value])
    
    @staticmethod
    def get_timestamp(date) -> int:
        # TODO: refactor this
        try:
            date_time = int(date)
            if datetime.timestamp(datetime.now()) > date_time:
                raise ValueError(ERROR_MESSAGES.TIMESTAMP_OUTDATED.value)
            return date_time
        except ValueError:
            matched_format = None
            for pattern in DATE_FORMATS.keys():
                if re.match(pattern, date):
                    matched_format = int(datetime.timestamp(datetime.strptime(date, DATE_FORMATS[pattern])))
                    break
            if matched_format == None:
                raise ValueError(ERROR_MESSAGES.UNSUPPORTED_DATE_FORMAT.value)
            return matched_format

    def get(self, event_name):
        if event_name == None or event_name == "":
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
        timestamp = self.index[event_name]
        if timestamp == None:
            raise ValueError(ERROR_MESSAGES.EVENT_NAME_NOT_FOUND.value)
        callback = self.in_memory_storage[timestamp][event_name]
        return { 
            EVENT_PARAMETERS.EVENT_NAME.value: event_name, 
            EVENT_PARAMETERS.DATE_TIME.value: timestamp, 
            EVENT_PARAMETERS.CALLBACK.value: callback }

    def set(self, event_name, date_time, callback) -> None:
        if event_name == None or event_name == "":
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
        if event_name in self.index.keys():
            raise ValueError(ERROR_MESSAGES.EVENT_NAME_NOT_UNIQUE.value)
        if date_time == None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_DATETIME.value)
        if callback == None:
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value)
        timestamp = self.get_timestamp(date_time)
        current_timestamp = int(datetime.now().timestamp())
        if current_timestamp > timestamp:
            raise ValueError(ERROR_MESSAGES.TIMESTAMP_OUTDATED.value)
        if timestamp not in self.in_memory_storage:
            self.in_memory_storage[timestamp] = {}
        self.in_memory_storage[timestamp][event_name] = lambda: self.wrap_callback(callback)
        self.index[event_name] = timestamp
        if self.persistent_session:
            self.event_repository.insert_event(event_name=event_name, timestamp=timestamp, callback=f"{self.wrap_callback(callback)}")

    def list(self) -> None:
        event_list: list[list] = []
        event_index = 1
        if len(self.index) == 0:
            stderr.write(ERROR_MESSAGES.NO_EVENTS_SCHEDULED.value)
        else:
            for event_name, timestamp in self.index.items():
                event_list.append([event_index, event_name, datetime.fromtimestamp(timestamp).isoformat()])
                event_index += 1
            list_str = "\n_______________________________________________________\n"
            list_str += ('| {:^5} | {:^20} | {:^20} |\n'.format(*["Index", "Event Name", "Scheduled Date"]))
            list_str += "|-----------------------------------------------------|\n"
            for event in event_list:
                list_str += ('| {:^5} | {:^20} | {:^20} |\n'.format(*event))
            list_str += "|_______|______________________|______________________|\n"
            stdout.write(list_str)

    def remove(self, event_name) -> None:
        if event_name not in self.index.keys():
            raise ValueError(ERROR_MESSAGES.EVENT_NAME_NOT_FOUND.value)
        event_timestamp = self.index[event_name]
        if len(self.in_memory_storage[event_timestamp]) > 1:
            self.in_memory_storage[event_timestamp].pop(event_name)
        else:
            self.in_memory_storage.pop(event_timestamp)
        self.index.pop(event_name)
        if self.persistent_session:
            self.event_repository.delete_event_by_name(event_name=event_name)

    def update(self, event_name, new_event_name=None, new_date_time=None, new_callback=None) -> None:
        if event_name == None or event_name == "":
            raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
        if event_name not in self.index.keys():
            raise ValueError(ERROR_MESSAGES.EVENT_NAME_NOT_FOUND.value)
        event_to_update = self.get(event_name)
        if new_event_name != None and new_event_name != "":
            event_to_update[EVENT_PARAMETERS.EVENT_NAME.value] = new_event_name
        if new_date_time != None and new_date_time != "":
            event_to_update[EVENT_PARAMETERS.DATE_TIME.value] = new_date_time
        if new_callback != None and new_callback != "":
            event_to_update[EVENT_PARAMETERS.CALLBACK.value] = new_callback
        self.remove(event_name)
        self.set(
            event_name=event_to_update[EVENT_PARAMETERS.EVENT_NAME.value], 
            date_time=event_to_update[EVENT_PARAMETERS.DATE_TIME.value],
            callback=event_to_update[EVENT_PARAMETERS.CALLBACK.value])
        if self.persistent_session:
            self.event_repository.update_event_by_name(
                event_name=event_name,
                new_event_name=event_to_update[EVENT_PARAMETERS.EVENT_NAME.value],
                new_timestamp=event_to_update[EVENT_PARAMETERS.DATE_TIME.value],
                new_callback=f"{event_to_update[EVENT_PARAMETERS.CALLBACK.value]}")
    
    @staticmethod
    def wrap_callback(event_callback) -> Callable:
        return event_callback