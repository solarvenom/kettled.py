from sys import stderr, stdout
from json import dumps
from datetime import datetime
from typing import Callable, Union
from kettled.daemon import get_daemon_pid, pipe_command
from kettled.constants import (
    COMMANDS_ENUM, ERROR_MESSAGES_ENUM, MESSAGES_ENUM,
    UPDATE_EVENT_PARAMETERS_ENUM, PIPE_COMMANDS_ENUM,
    EVENT_PARAMETERS_ENUM, RECURRENCY_OPTIONS_ENUM,
    FALLBACK_DIRECTIVES_ENUM, RELATIVE_DATETIME_OPTIONS_ENUM,
    ICONS_ENUM
)
from kettled.utils import calculate_relative_datetime
from kettled.handlers import Handler

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
    
    @staticmethod
    def status():
        try:
            c_time = get_daemon_pid()
        except IOError:
            c_time = None
    
        if not c_time:
            return MESSAGES_ENUM.IS_DOWN.value
        else:
            total_seconds = int((datetime.now() - datetime.fromtimestamp(c_time)).total_seconds())
            if total_seconds < 60:
                return f"{ICONS_ENUM.KETTLE.value} kettled has been up for {total_seconds} seconds."
            elif total_seconds < 3600:
                return f"{ICONS_ENUM.KETTLE.value} kettled has been up for {total_seconds // 60} minutes and {total_seconds % 60} seconds."
            else:
                return f"{ICONS_ENUM.KETTLE.value} kettled has been up for {total_seconds // 3600} hours, {total_seconds % 3600 // 60} minutes, and {total_seconds % 3600 % 60} seconds."
        return