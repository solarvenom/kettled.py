from sys import stderr
from json import dumps
import logging
from kettled.daemon.daemon import get_daemon_pid
from kettled.daemon.pipes import pipe_command
from kettled.constants.enums import (
    COMMANDS, ERROR_MESSAGES, MESSAGES, UPDATE_EVENT_PARAMETERS, 
    COMMAND_MESSAGE, EVENT_PARAMETERS, TERMINAL_PROMPTS
)
from kettled.handlers.general_handler import GeneralHandler

class TerminalHandler(GeneralHandler):

    @staticmethod
    def add():
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[COMMAND_MESSAGE.COMMAND.value] = COMMANDS.ADD.value
            data[EVENT_PARAMETERS.EVENT_NAME.value] = input(TERMINAL_PROMPTS.ADD_EVENT_NAME.value).strip()
            data[EVENT_PARAMETERS.DATE_TIME.value] = input(TERMINAL_PROMPTS.ADD_EVENT_DATE_TIME.value).strip()
            data[EVENT_PARAMETERS.CALLBACK.value] = input(TERMINAL_PROMPTS.ADD_EVENT_CALLBACK.value).strip()
            command[COMMAND_MESSAGE.DATA.value] = data
            command_json = dumps(command)
            pipe_command(command_json)
        except IOError:
            stderr.write(MESSAGES.IS_DOWN.value)

    @staticmethod
    def delete():
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[COMMAND_MESSAGE.COMMAND.value] = COMMANDS.DELETE.value
            data[EVENT_PARAMETERS.EVENT_NAME.value] = input(TERMINAL_PROMPTS.DELETE_EVENT_NAME.value)
            command[COMMAND_MESSAGE.DATA.value] = data
            command_json = dumps(command)
            pipe_command(command_json)
        except IOError as e:
            logging.exception(e)

    @staticmethod
    def update():
        try:
            get_daemon_pid()
            command, data = {}, {}
            command[COMMAND_MESSAGE.COMMAND.value] = COMMANDS.UPDATE.value
            event_name = input(TERMINAL_PROMPTS.UPDATE_EVENT_NAME.value)
            if event_name == "":
                stderr.write(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
                return
            data[EVENT_PARAMETERS.EVENT_NAME.value] = event_name
            new_event_name = input(TERMINAL_PROMPTS.UPDATE_NEW_EVENT_NAME.value)
            new_date_time = input(TERMINAL_PROMPTS.UPDATE_NEW_DATE_TIME.value)
            new_callback = input(TERMINAL_PROMPTS.UPDATE_NEW_CALLBACK.value)
            if new_event_name == "" and new_date_time == "" and new_callback == "":
                stderr.write(ERROR_MESSAGES.INSUFFICIENT_UPDATE_ARGS.value)
                return
            if new_event_name != "":
                data[UPDATE_EVENT_PARAMETERS.NEW_EVENT_NAME.value] = new_event_name
            if new_date_time != "":
                data[UPDATE_EVENT_PARAMETERS.NEW_DATE_TIME.value] = new_date_time
            if new_callback != "":
                data[UPDATE_EVENT_PARAMETERS.NEW_CALLBACK.value] = new_callback
            command[COMMAND_MESSAGE.DATA.value] = data
            command_json = dumps(command)
            pipe_command(command_json)
        except ValueError as error:
            stderr.write(str(error))
        except IOError:
            stderr.write(MESSAGES.IS_DOWN.value)