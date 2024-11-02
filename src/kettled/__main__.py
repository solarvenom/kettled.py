from sys import exit, argv, stderr
from json import dumps
from inspect import getsource
import logging
from kettled.daemon import Daemon, get_daemon_pid
from kettled.constants.enums import COMMANDS, ERROR_MESSAGES, MESSAGES, UPDATE_EVENT_PARAMETERS, COMMAND_MESSAGE, EVENT_PARAMETERS, TERMINAL_PROMPTS
from kettled.pipes import pipe_command

def main() -> None:
    if len(argv) == 2:
        if COMMANDS.START.value == argv[1]:
            try:
                get_daemon_pid()
                stderr.write(MESSAGES.IS_ALREADY_RUNNING.value)
            except IOError:
                daemon = Daemon()
                daemon.start()
        elif COMMANDS.STOP.value == argv[1]:
            try:
                get_daemon_pid()
                Daemon.stop()
            except IOError:
                stderr.write(MESSAGES.IS_DOWN.value)
        elif COMMANDS.STATUS.value == argv[1]:
            Daemon.status()
        elif COMMANDS.LIST.value == argv[1]:
            try:
                get_daemon_pid()
                command = {}
                command[COMMAND_MESSAGE.COMMAND.value] = COMMANDS.LIST.value
                command_json = dumps(command)
                pipe_command(command_json)
            except IOError:
                stderr.write(MESSAGES.IS_DOWN.value)
        elif COMMANDS.ADD.value == argv[1]:
            try:
                get_daemon_pid()
                command, data = {}, {}
                command[COMMAND_MESSAGE.COMMAND.value] = COMMANDS.ADD.value
                # data["date_time"] = "2286-11-20 15:28:45"
                # data["event_name"] = "test event"
                # def callback():
                #     return print("test_cb_value")
                data[EVENT_PARAMETERS.EVENT_NAME.value] = input(TERMINAL_PROMPTS.ADD_EVENT_NAME.value)
                data[EVENT_PARAMETERS.DATE_TIME.value] = input(TERMINAL_PROMPTS.ADD_EVENT_DATE_TIME.value)
                event_callback = input(TERMINAL_PROMPTS.ADD_EVENT_CALLBACK.value)
                def callback():
                    return event_callback
                data[EVENT_PARAMETERS.CALLBACK.value] = getsource(callback)
                command[COMMAND_MESSAGE.DATA.value] = data
                command_json = dumps(command)
                pipe_command(command_json)
            except IOError:
                stderr.write(MESSAGES.IS_DOWN.value)
        elif COMMANDS.DELETE.value == argv[1]:
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
        elif COMMANDS.UPDATE.value == argv[1]:
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
                logging.exception(error)
            except IOError:
                stderr.write(MESSAGES.IS_DOWN.value)
        else:
            stderr.write(ERROR_MESSAGES.UNKNOWN_COMMAND.value)
            stderr.write(MESSAGES.USAGE.value)
            exit(2)
    else:
        stderr.write(MESSAGES.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()