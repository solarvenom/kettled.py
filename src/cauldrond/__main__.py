from sys import exit, argv, stderr
from json import dumps
from cauldrond.daemon import Daemon, raise_if_daemon_is_up, get_daemon_pid
from cauldrond.constants.enums import COMMANDS, ERROR_MESSAGES, MESSAGES
import inspect

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
            command = {}
            command["command"] = COMMANDS.LIST.value
            command_json = dumps(command)
            Daemon.pipe_command(command_json)
        elif COMMANDS.ADD.value == argv[1]:
            command, data = {}, {}
            command["command"] = COMMANDS.ADD.value
            data["date_time"] = "2024-10-17 09:57:28"
            data["name"] = "test event"
            def callback():
                return print("test_cb_value")
            data["callback"] = inspect.getsource(callback)
            command["data"] = data
            command_json = dumps(command)
            Daemon.pipe_command(command_json)
        else:
            stderr.write(ERROR_MESSAGES.UNKNOWN_COMMAND.value)
            stderr.write(MESSAGES.USAGE.value)
            exit(2)
    else:
        stderr.write(MESSAGES.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()