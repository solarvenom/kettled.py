
from sys import exit, argv, stderr
import cauldrond.daemon 
from cauldrond.constants.enums import COMMANDS, ERROR_MESSAGES, MESSAGES

def main() -> None:
    daemon = cauldrond.daemon.Daemon()
    if len(argv) == 2:
        if COMMANDS.START.value == argv[1]:
            daemon.run()
        # elif COMMANDS.STOP.value == argv[1]:
        #     daemon.stop()
        # elif COMMANDS.RESTART.value == argv[1]:
        #     daemon.restart()
        # elif COMMANDS.STATUS.value == argv[1]:
        #     daemon.status()
        # elif COMMANDS.LIST.value == argv[1]:
        #     daemon.list()
        # elif COMMANDS.ADD.value == argv[1]:
        #     event_name = input("Enter event_name: ")
        #     date_time = input("Enter event date_time: ")
        #     callback = input("Enter event callback: ")
        #     daemon.add(
        #         event_name=event_name,
        #         date_time=date_time,
        #         callback=callback)
        else:
            stderr.write(ERROR_MESSAGES.UNKNOWN_COMMAND.value)
            exit(2)
    else:
        stderr.write(MESSAGES.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()