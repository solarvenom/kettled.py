from sys import exit, argv, stderr
from kettled.constants.enums import COMMANDS, ERROR_MESSAGES, MESSAGES
from kettled.handlers.terminal_handler import TerminalHandler

def main() -> None:
    if len(argv) == 2:
        if COMMANDS.START.value == argv[1]:
            TerminalHandler().init()
        elif COMMANDS.STOP.value == argv[1]:
            TerminalHandler.stop()
        elif COMMANDS.STATUS.value == argv[1]:
            TerminalHandler.status()
        elif COMMANDS.LIST.value == argv[1]:
            TerminalHandler.list()
        elif COMMANDS.ADD.value == argv[1]:
            TerminalHandler.add()
        elif COMMANDS.DELETE.value == argv[1]:
            TerminalHandler.delete()
        elif COMMANDS.UPDATE.value == argv[1]:
            TerminalHandler.update()
        else:
            stderr.write(ERROR_MESSAGES.UNKNOWN_COMMAND.value)
            stderr.write(MESSAGES.USAGE.value)
            exit(2)
    else:
        stderr.write(MESSAGES.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()