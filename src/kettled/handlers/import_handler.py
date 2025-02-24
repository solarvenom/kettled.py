from sys import stderr
from json import dumps
from datetime import datetime
from typing import Callable, Union
from kettled.daemon.daemon import get_daemon_pid
from kettled.daemon.pipes import pipe_command
from kettled.constants.enums.commands_enum import COMMANDS_ENUM
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM
from kettled.constants.enums.messages_enum import MESSAGES_ENUM
from kettled.constants.enums.update_event_parameters_enum import UPDATE_EVENT_PARAMETERS_ENUM
from kettled.constants.enums.pipe_commands_enum import PIPE_COMMANDS_ENUM
from kettled.constants.enums.event_parameters_enum import EVENT_PARAMETERS_ENUM
from kettled.constants.enums.recurrency_options_enum import RECURRENCY_OPTIONS_ENUM
from kettled.constants.enums.fallback_options_enum import FALLBACK_DIRECTIVES_ENUM
from kettled.constants.enums.relative_datetime_options_enum import RELATIVE_DATETIME_OPTIONS_ENUM
from kettled.utils.relative_datetime_calculator import calculate_relative_datetime
from kettled.handlers.handler import Handler

class ImportHandler(Handler):
    @staticmethod
    def add(
        event_name: str, 
        date_time: Union[str, int], 
        recurrency: Union[str, None],
        fallback_directive: Union[str, None],
        callback: Union[str, Callable]):
        try:
            if event_name == "" or event_name == None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)

            if date_time == "" or date_time == None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_DATETIME.value)
            if date_time in RELATIVE_DATETIME_OPTIONS_ENUM.list():
                now = datetime.now()
                date_time = str(calculate_relative_datetime(now, date_time))

            recurrency_options = RECURRENCY_OPTIONS_ENUM.list()
            if recurrency != "" and recurrency not in recurrency_options:
                raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_RECURRENCY_OPTION.value)
            if recurrency == "" or recurrency == None:
                recurrency = RECURRENCY_OPTIONS_ENUM.NOT_RECURRING.value
            
            fallback_directives = FALLBACK_DIRECTIVES_ENUM.list()
            if fallback_directive != "" and fallback_directive not in fallback_directives:
                raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_FALLBACK_DIRECTIVE.value)
            if fallback_directive == "" or fallback_directive == None:
                fallback_directive = FALLBACK_DIRECTIVES_ENUM.EXECUTE_AS_SOON_AS_POSSIBLE.value
            
            if callback == "" or callback == None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_CALLBACK.value)

            get_daemon_pid()
            pipe_command(dumps({
                PIPE_COMMANDS_ENUM.COMMAND.value: COMMANDS_ENUM.ADD.value,
                PIPE_COMMANDS_ENUM.DATA.value: {
                    EVENT_PARAMETERS_ENUM.EVENT_NAME.value: event_name,
                    EVENT_PARAMETERS_ENUM.DATE_TIME.value: date_time,
                    EVENT_PARAMETERS_ENUM.RECURRENCY.value: recurrency,
                    EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value: fallback_directive,
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
            if event_name == "" or event_name == None:
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
            new_reccurency: Union[str, None],
            new_fallback_directive: Union[str, None],
            new_callback: Union[Callable, None]
        ):
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[PIPE_COMMANDS_ENUM.COMMAND.value] = COMMANDS_ENUM.UPDATE.value

            if event_name == "" or event_name == None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
            data[EVENT_PARAMETERS_ENUM.EVENT_NAME.value] = event_name

            if (new_event_name == "" or new_event_name == None) and (new_date_time == "" or new_date_time == None) and (new_callback == "" or new_callback == None):
                raise ValueError(ERROR_MESSAGES_ENUM.INSUFFICIENT_UPDATE_ARGS.value)

            if new_event_name != "" and new_event_name != None:
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_EVENT_NAME.value] = new_event_name

            if new_date_time != "" and new_date_time != None:
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_DATE_TIME.value] = new_date_time
            if new_date_time in RELATIVE_DATETIME_OPTIONS_ENUM.list():
                now = datetime.now()
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_DATE_TIME.value] = calculate_relative_datetime(now, new_date_time)

            if new_recurrency != "" and new_reccurency != None:
                if new_recurrency not in RECURRENCY_OPTIONS_ENUM.list():
                    raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_RECURRENCY_OPTION.value)
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_RECURRENCY.value] = new_recurrency

            if new_fallback_directive != "" and new_fallback_directive != None:
                if new_fallback_directive not in FALLBACK_DIRECTIVES_ENUM.list():
                    raise ValueError(ERROR_MESSAGES_ENUM.UNSUPPORTED_FALLBACK_DIRECTIVE.value)
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_FALLBACK_DIRECTIVE.value] = new_fallback_directive

            if new_callback != "" and new_callback != None:
                data[UPDATE_EVENT_PARAMETERS_ENUM.NEW_CALLBACK.value] = new_callback

            command[PIPE_COMMANDS_ENUM.DATA.value] = data
            pipe_command(dumps(command))
        except ValueError as error:
            return stderr.write(str(error))
        except IOError:
            return stderr.write(MESSAGES_ENUM.IS_DOWN.value)