
from sys import exit, argv
from time import sleep
from nuthatch.daemon import Daemon
from env import ICON
 
class NuthatchDaemon(Daemon):
    def run(self):
        while True:
            sleep(1)
 
def main() -> None:
    daemon = NuthatchDaemon()
    if len(argv) == 2:
        if 'start' == argv[1]:
            daemon.start()
        elif 'stop' == argv[1]:
            daemon.stop()
        elif 'restart' == argv[1]:
            daemon.restart()
        elif 'status' == argv[1]:
            daemon.status()
        else:
            print(f"{ICON} Unknown command")
            exit(2)
        exit(0)
    else:
        print(f"{ICON} usage: [{argv[0]}] : start | stop | restart | status")
        exit(2)

if __name__ == "__main__":
    main()