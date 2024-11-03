from sys import stderr
from json import dumps
from typing import Callable
from kettled.daemon.daemon import get_daemon_pid
from kettled.daemon.pipes import pipe_command
from kettled.constants.enums import (
    COMMANDS, ERROR_MESSAGES, MESSAGES, UPDATE_EVENT_PARAMETERS, 
    COMMAND_PIPE, EVENT_PARAMETERS
)
from kettled.handlers.handler import Handler

class ImportHandler(Handler):
    @staticmethod
    def add(event_name: str, date_time: str | int, callback: str | Callable):
        try:
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
            if date_time == "" or date_time is None:
                raise ValueError(ERROR_MESSAGES.MISSING_EVENT_DATETIME.value)
            if callback == "" or callback is None:
                raise ValueError(ERROR_MESSAGES.MISSING_EVENT_CALLBACK.value)
            get_daemon_pid()
            pipe_command(dumps({
                COMMAND_PIPE.COMMAND.value: COMMANDS.ADD.value,
                COMMAND_PIPE.DATA.value: {
                    EVENT_PARAMETERS.EVENT_NAME.value: event_name,
                    EVENT_PARAMETERS.DATE_TIME.value: date_time,
                    EVENT_PARAMETERS.CALLBACK.value: callback
                }
            }))
        except ValueError as error:
            return stderr.write(str(error))
        except IOError:
            return stderr.write(MESSAGES.IS_DOWN.value)

    @staticmethod
    def delete(event_name: str):
        try:
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
            get_daemon_pid()
            pipe_command(dumps({
                COMMAND_PIPE.COMMAND.value: COMMANDS.DELETE.value,
                COMMAND_PIPE.DATA.value: {
                    EVENT_PARAMETERS.EVENT_NAME.value: event_name
                }
            }))
        except ValueError as error:
            return stderr.write(str(error))
        except IOError as error:
            return stderr.write(str(error))

    @staticmethod
    def update(
            event_name: str | None, 
            new_event_name: str | None,
            new_date_time: str | int | None,
            new_callback: Callable | None
        ):
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[COMMAND_PIPE.COMMAND.value] = COMMANDS.UPDATE.value
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
            data[EVENT_PARAMETERS.EVENT_NAME.value] = event_name
            if (new_event_name == "" or new_event_name is None) and (new_date_time == "" or new_date_time is None) and (new_callback == "" or new_callback is None):
                raise ValueError(ERROR_MESSAGES.INSUFFICIENT_UPDATE_ARGS.value)
            if new_event_name != "" and new_event_name is not None:
                data[UPDATE_EVENT_PARAMETERS.NEW_EVENT_NAME.value] = new_event_name
            if new_date_time != "" and new_date_time is not None:
                data[UPDATE_EVENT_PARAMETERS.NEW_DATE_TIME.value] = new_date_time
            if new_callback != "" and new_callback is not None:
                data[UPDATE_EVENT_PARAMETERS.NEW_CALLBACK.value] = new_callback
            command[COMMAND_PIPE.DATA.value] = data
            pipe_command(dumps(command))
        except ValueError as error:
            return stderr.write(str(error))
        except IOError:
            return stderr.write(MESSAGES.IS_DOWN.value)