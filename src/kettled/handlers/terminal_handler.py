from os import path
from sys import stderr, stdout
from json import dumps
from datetime import datetime
from kettled.constants.env import DAEMON_NAME, PID_FILE
from kettled.daemon.daemon import get_daemon_pid
from kettled.daemon.pipes import pipe_command
from kettled.constants.enums.commands_enum import COMMANDS_ENUM
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM
from kettled.constants.enums.messages_enum import MESSAGES_ENUM
from kettled.constants.enums.update_event_parameters_enum import UPDATE_EVENT_PARAMETERS_ENUM
from kettled.constants.enums.pipe_commands_enum import PIPE_COMMANDS_ENUM
from kettled.constants.enums.event_parameters_enum import EVENT_PARAMETERS_ENUM
from kettled.constants.enum.terminal_propmpts_enum import TERMINAL_PROPMPTS_ENUM
from kettled.constants.enum.icons_enum import ICONS_ENUM
from kettled.handlers.handler import Handler

class TerminalHandler(Handler):
    @staticmethod
    def add():
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[PIPE_COMMANDS_ENUM.COMMAND.value] = COMMANDS_ENUM.ADD.value
            event_name = input(TERMINAL_PROPMPTS_ENUM.ADD_EVENT_NAME.value).strip()
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
            data[EVENT_PARAMETERS_ENUM.EVENT_NAME.value] = event_name
            date_time = input(TERMINAL_PROPMPTS_ENUM.ADD_EVENT_DATE_TIME.value).strip()
            if date_time == "" or date_time is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_DATETIME.value)
            data[EVENT_PARAMETERS_ENUM.DATE_TIME.value] = date_time
            callback = input(TERMINAL_PROPMPTS_ENUM.ADD_EVENT_CALLBACK.value).strip()
            if callback == "" or callback is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_CALLBACK.value)
            data[EVENT_PARAMETERS_ENUM.CALLBACK.value] = callback
            command[PIPE_COMMANDS_ENUM.DATA.value] = data
            pipe_command(dumps(command))
        except ValueError as error:
            stderr.write(str(error))
        except IOError:
            stderr.write(MESSAGES_ENUM.IS_DOWN.value)

    @staticmethod
    def delete():
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[PIPE_COMMANDS_ENUM.COMMAND.value] = COMMANDS_ENUM.DELETE.value
            event_name = input(TERMINAL_PROPMPTS_ENUM.DELETE_EVENT_NAME.value).strip()
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
            data[EVENT_PARAMETERS_ENUM.EVENT_NAME.value] = event_name
            command[PIPE_COMMANDS_ENUM.DATA.value] = data
            pipe_command(dumps(command))
        except ValueError as error:
            stderr.write(str(error))
        except IOError as error:
            stderr.write(str(error))

    @staticmethod
    def update():
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[PIPE_COMMANDS_ENUM.COMMAND.value] = COMMANDS_ENUM.UPDATE.value
            event_name = input(TERMINAL_PROPMPTS_ENUM.UPDATE_EVENT_NAME.value).strip()
            if event_name == "" or event_name is None:
                raise ValueError(ERROR_MESSAGES_ENUM.MISSING_EVENT_NAME.value)
            data[EVENT_PARAMETERS_ENUM.EVENT_NAME.value] = event_name
            new_event_name = input(TERMINAL_PROPMPTS_ENUM.UPDATE_NEW_EVENT_NAME.value).strip()
            new_date_time = input(TERMINAL_PROPMPTS_ENUM.UPDATE_NEW_DATE_TIME.value).strip()
            new_callback = input(TERMINAL_PROPMPTS_ENUM.UPDATE_NEW_CALLBACK.value).strip()
            if (new_event_name == "" or new_event_name is None) and (new_date_time == "" or new_date_time is None) and (new_callback == "" or new_callback is None):
                raise ValueError(ERROR_MESSAGES_ENUM.INSUFFICIENT_UPDATE_ARGS.value)
            if new_event_name != "" and new_event_name is not None:
                data[UPDATE_EVENT_PARAMETERS.NEW_EVENT_NAME.value] = new_event_name
            if new_date_time != "" and new_date_time is not None:
                data[UPDATE_EVENT_PARAMETERS.NEW_DATE_TIME.value] = new_date_time
            if new_callback != "" and new_callback is not None:
                data[UPDATE_EVENT_PARAMETERS.NEW_CALLBACK.value] = new_callback
            command[PIPE_COMMANDS_ENUM.DATA.value] = data
            pipe_command(dumps(command))
        except ValueError as error:
            stderr.write(str(error))
        except IOError:
            stderr.write(MESSAGES_ENUM.IS_DOWN.value)

    @staticmethod
    def status():
        try:
            c_time = path.getctime(PID_FILE)
        except IOError:
            c_time = None
    
        if not c_time:
            stdout.write(MESSAGES_ENUM.IS_DOWN.value)
        else:
            total_seconds = int((datetime.now() - datetime.fromtimestamp(c_time)).total_seconds())
            if total_seconds < 60:
                stdout.write(f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} has been up for {total_seconds} seconds.\n")
            elif total_seconds < 3600:
                stdout.write(f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} has been up for {total_seconds // 60} minutes and {total_seconds % 60} seconds.\n")
            else:
                stdout.write(f"{ICONS_ENUM.KETTLE.value} {DAEMON_NAME} has been up for {total_seconds // 3600} hours, {total_seconds % 3600 // 60} minutes, and {total_seconds % 3600 % 60} seconds.\n")
        return

    @staticmethod
    def list():
        try:
            get_daemon_pid()
            pipe_command(dumps({PIPE_COMMANDS_ENUM.COMMAND.value: COMMANDS_ENUM.LIST.value}))
        except IOError:
            stderr.write(MESSAGES_ENUM.IS_DOWN.value)