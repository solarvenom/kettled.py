
from sys import exit, argv, stderr
from time import sleep
from cauldrond.daemon import Daemon
from cauldrond.constants.enums import COMMANDS, ERROR_MESSAGES, MESSAGES
 
class NuthatchDaemon(Daemon):
    def run(self):
        while True:
            sleep(1)
 
def main() -> None:
    daemon = NuthatchDaemon()
    if len(argv) == 2:
        if COMMANDS.START.value == argv[1]:
            daemon.start()
        elif COMMANDS.STOP.value == argv[1]:
            daemon.stop()
        elif COMMANDS.RESTART.value == argv[1]:
            daemon.restart()
        elif COMMANDS.STATUS.value == argv[1]:
            daemon.status()
        else:
            stderr.write(ERROR_MESSAGES.UNKNOWN_COMMAND.value)
            exit(2)
        exit(0)
    else:
        stderr.write(MESSAGES.USAGE.value)
        exit(2)

if __name__ == "__main__":
    main()