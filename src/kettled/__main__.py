from sys import exit, argv, stderr
from kettled.constants import ERROR_MESSAGES_ENUM, MESSAGES_ENUM, SESSION_OPTIONS_ENUM
from kettled.daemon import DAEMON_COMMANDS_ENUM
from kettled.handlers import TerminalHandler

def main() -> None:
    if DAEMON_COMMANDS_ENUM.START.value == argv[1]:
        try:
            in_memory_only_session = True if argv[2] == SESSION_OPTIONS_ENUM.IN_MEMORY_ONLY.value else False
            TerminalHandler(in_memory_only_session=in_memory_only_session).init()
        except IndexError:
            TerminalHandler().init()
    elif DAEMON_COMMANDS_ENUM.STOP.value == argv[1]:
        TerminalHandler.stop()
    elif DAEMON_COMMANDS_ENUM.STATUS.value == argv[1]:
        TerminalHandler.status()
    elif DAEMON_COMMANDS_ENUM.LIST.value == argv[1]:
        TerminalHandler.list()
    elif DAEMON_COMMANDS_ENUM.ADD.value == argv[1]:
        TerminalHandler.add()
    elif DAEMON_COMMANDS_ENUM.DELETE.value == argv[1]:
        TerminalHandler.delete()
    elif DAEMON_COMMANDS_ENUM.UPDATE.value == argv[1]:
        TerminalHandler.update()
    else:
        stderr.write(ERROR_MESSAGES_ENUM.UNKNOWN_COMMAND.value)
        stderr.write(MESSAGES_ENUM.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()