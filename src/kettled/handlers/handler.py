from sys import stderr
from kettled.daemon.daemon import Daemon, get_daemon_pid
from kettled.constants.enums import MESSAGES

class Handler:
    def __init__(self, persistent_session=False):
        self.persistent_session = persistent_session

    def init(self):
        try:
            get_daemon_pid()
            stderr.write(MESSAGES.IS_ALREADY_RUNNING.value)
        except IOError:
            Daemon(persistent_session=self.persistent_session).start()
    
    @staticmethod
    def stop():
        try:
            get_daemon_pid()
            Daemon.stop()
        except IOError:
            stderr.write(MESSAGES.IS_DOWN.value)