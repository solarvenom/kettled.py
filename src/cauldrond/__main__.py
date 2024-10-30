from sys import exit, argv, stderr
from json import dumps
from cauldrond.daemon import Daemon, raise_if_daemon_is_up, get_daemon_pid
from cauldrond.constants.enums import COMMANDS, ERROR_MESSAGES, MESSAGES, ICONS
import inspect
import logging

def main() -> None:
    if len(argv) == 2:
        if COMMANDS.START.value == argv[1]:
            try:
                raise_if_daemon_is_up()
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
                command["command"] = COMMANDS.LIST.value
                command_json = dumps(command)
                Daemon.pipe_command(command_json)
            except IOError:
                stderr.write(MESSAGES.IS_DOWN.value)
        elif COMMANDS.ADD.value == argv[1]:
            try:
                get_daemon_pid()
                command, data = {}, {}
                command["command"] = COMMANDS.ADD.value
                # data["date_time"] = "2024-10-17 09:57:28"
                # data["event_name"] = "test event"
                # def callback():
                #     return print("test_cb_value")
                data["event_name"] = input(f"{ICONS.CRYSTALL_BALL.value} Please enter event name: ")
                data["date_time"] = input(f"{ICONS.CRYSTALL_BALL.value} Please enter event scheduled date: ")
                event_callback = input(f"{ICONS.CRYSTALL_BALL.value} Please enter event callback: ")
                def callback():
                    return event_callback
                data["callback"] = inspect.getsource(callback)
                command["data"] = data
                command_json = dumps(command)
                Daemon.pipe_command(command_json)
            except IOError:
                stderr.write(MESSAGES.IS_DOWN.value)
        elif COMMANDS.DELETE.value == argv[1]:
            try:
                get_daemon_pid()
                command, data = {}, {}
                command["command"] = COMMANDS.DELETE.value
                data["event_name"] = input(f"{ICONS.CRYSTALL_BALL.value} Please enter the name of event to be deleted: ")
                command["data"] = data
                command_json = dumps(command)
                Daemon.pipe_command(command_json)
            except IOError as e:
                logging.exception(e)
        elif COMMANDS.UPDATE.value == argv[1]:
            try:
                get_daemon_pid()
                command, data = {}, {}
                command["command"] = COMMANDS.UPDATE.value
                event_name = input(f"{ICONS.CRYSTALL_BALL.value} Please enter the name of event be modified: ")
                if event_name == "":
                    stderr.write(ERROR_MESSAGES.MISSING_EVENT_NAME.value)
                    return
                data["event_name"] = event_name
                new_event_name = input(f"{ICONS.CRYSTALL_BALL.value} Please enter the new event name or leave blank to leave unchanged: ")
                new_date_time = input(f"{ICONS.CRYSTALL_BALL.value} Please enter the new event schdeuled date or leave blank to leave unchanged: ")
                new_callback = input(f"{ICONS.CRYSTALL_BALL.value} Please enter the new event callback or leave blank to leave unchanged: ")
                if new_event_name == "" and new_date_time == "" and new_callback == "":
                    stderr.write(ERROR_MESSAGES.INSUFFICIENT_UPDATE_ARGS.value)
                    return
                if new_event_name != "":
                    data["new_event_name"] = new_date_time
                if new_date_time != "":
                    data["new_date_time"] = new_date_time
                if new_callback != "":
                    data["new_callback"] = new_callback
                command["data"] = data
                command_json = dumps(command)
                Daemon.pipe_command(command_json)
                print("UPDATE PIPE PIPED")
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