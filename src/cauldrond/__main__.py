
from sys import exit, argv, stderr
from time import sleep
from cauldrond.daemon import Daemon
from cauldrond.constants.enums import COMMANDS, ERROR_MESSAGES, MESSAGES
 
class CauldrondDaemon(Daemon):
    def run(self):
        while True:
            sleep(1)
 
def main() -> None:
    daemon = CauldrondDaemon()
    if len(argv) == 2:
        if COMMANDS.START.value == argv[1]:
            daemon.start()
        elif COMMANDS.STOP.value == argv[1]:
            daemon.stop()
        elif COMMANDS.RESTART.value == argv[1]:
            daemon.restart()
        elif COMMANDS.STATUS.value == argv[1]:
            daemon.status()
        elif COMMANDS.LIST.value == argv[1]:
            daemon.list()
        elif COMMANDS.ADD.value == argv[1]:
            event_name = input("Enter event_name: ")
            date_time = input("Enter event date_time: ")
            callback = input("Enter event callback: ")
            daemon.add(
                event_name=event_name,
                date_time=date_time,
                callback=callback)
        else:
            stderr.write(ERROR_MESSAGES.UNKNOWN_COMMAND.value)
            exit(2)
        exit(0)
    else:
        stderr.write(MESSAGES.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()