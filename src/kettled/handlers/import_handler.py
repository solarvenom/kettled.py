from sys import stderr
from json import dumps
from typing import Callable, Union
from kettled.daemon.daemon import get_daemon_pid
from kettled.daemon.pipes import pipe_command
from kettled.constants.enums.commands_enum import COMMANDS_ENUM
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM
from kettled.constants.enums.messages_enum import MESSAGES_ENUM
from kettled.constants.enums.update_event_parameters_enum import UPDATE_EVENT_PARAMETERS_ENUM
from kettled.constants.enums.pipe_commands_enum import PIPE_COMMANDS_ENUM
from kettled.constants.enums.event_parameters_enum import EVENT_PARAMETERS_ENUM
from kettled.handlers.handler import Handler

class ImportHandler(Handler):
    @staticmethod
    def add(event_name: str, date_time: Union[str, int], callback: Union[str, Callable]):
        try:
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
            if date_time == "" or date_time is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_DATETIME.value)
            if callback == "" or callback is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_CALLBACK.value)
            get_daemon_pid()
            pipe_command(dumps({
                PIPE_COMMANDS_ENUM.COMMAND.value: COMMANDS_ENUM.ADD.value,
                PIPE_COMMANDS_ENUM.DATA.value: {
                    EVENT_PARAMETERS_ENUM.EVENT_NAME.value: event_name,
                    EVENT_PARAMETERS_ENUM.DATE_TIME.value: date_time,
                    EVENT_PARAMETERS_ENUM.CALLBACK.value: callback
                }
            }))
        except ValueError as error:
            return stderr.write(str(error))
        except IOError:
            return stderr.write(MESSAGES_ENUM.IS_DOWN.value)

    @staticmethod
    def delete(event_name: str):
        try:
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
            get_daemon_pid()
            pipe_command(dumps({
                PIPE_COMMANDS_ENUM.COMMAND.value: COMMANDS_ENUM.DELETE.value,
                PIPE_COMMANDS_ENUM.DATA.value: {
                    EVENT_PARAMETERS_ENUM.EVENT_NAME.value: event_name
                }
            }))
        except ValueError as error:
            return stderr.write(str(error))
        except IOError as error:
            return stderr.write(str(error))

    @staticmethod
    def update(
            event_name: Union[str, None], 
            new_event_name: Union[str, None],
            new_date_time: Union[str, int, None],
            new_callback: Union[Callable, None]
        ):
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[PIPE_COMMANDS_ENUM.COMMAND.value] = COMMANDS_ENUM.UPDATE.value
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
            data[EVENT_PARAMETERS_ENUM.EVENT_NAME.value] = event_name
            if (new_event_name == "" or new_event_name is None) and (new_date_time == "" or new_date_time is None) and (new_callback == "" or new_callback is None):
                raise ValueError(ERROR_MESSAGES_ENUM.INSUFFICIENT_UPDATE_ARGS.value)
            if new_event_name != "" and new_event_name is not None:
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_EVENT_NAME.value] = new_event_name
            if new_date_time != "" and new_date_time is not None:
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_DATE_TIME.value] = new_date_time
            if new_callback != "" and new_callback is not None:
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_CALLBACK.value] = new_callback
            command[PIPE_COMMANDS_ENUM.DATA.value] = data
            pipe_command(dumps(command))
        except ValueError as error:
            return stderr.write(str(error))
        except IOError:
            return stderr.write(MESSAGES_ENUM.IS_DOWN.value)