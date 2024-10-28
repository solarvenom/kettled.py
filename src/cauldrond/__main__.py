from sys import exit, argv, stderr
from cauldrond.daemon import Daemon, raise_if_daemon_is_up, get_daemon_pid
from cauldrond.constants.enums import COMMANDS, ERROR_MESSAGES, MESSAGES

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
        # elif COMMANDS.LIST.value == argv[1]:
        #     daemon.list()
        else:
            stderr.write(ERROR_MESSAGES.UNKNOWN_COMMAND.value)
            stderr.write(MESSAGES.USAGE.value)
            exit(2)
    else:
        stderr.write(MESSAGES.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()