from sys import exit, argv, stderr
from kettled.constants.enums.commands_enum import COMMANDS_ENUM
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM
from kettled.constants.enums.messages_enum import MESSAGES_ENUM
from kettled.constants.enums.session_options_enum import SESSION_OPTIONS_ENUM
from kettled.handlers.terminal_handler import TerminalHandler

def main() -> None:
    if COMMANDS_ENUM.START.value == argv[1]:
        try:
            in_memory_only_session = True if argv[2] == SESSION_OPTIONS_ENUM.IN_MEMORY_ONLY.value else False
            TerminalHandler(in_memory_only_session=in_memory_only_session).init()
        except IndexError:
            TerminalHandler().init()
    elif COMMANDS_ENUM.STOP.value == argv[1]:
        TerminalHandler.stop()
    elif COMMANDS_ENUM.STATUS.value == argv[1]:
        TerminalHandler.status()
    elif COMMANDS_ENUM.LIST.value == argv[1]:
        TerminalHandler.list()
    elif COMMANDS_ENUM.ADD.value == argv[1]:
        TerminalHandler.add()
    elif COMMANDS_ENUM.DELETE.value == argv[1]:
        TerminalHandler.delete()
    elif COMMANDS_ENUM.UPDATE.value == argv[1]:
        TerminalHandler.update()
    else:
        stderr.write(ERROR_MESSAGES_ENUM.UNKNOWN_COMMAND.value)
        stderr.write(MESSAGES_ENUM.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()