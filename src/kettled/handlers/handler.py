from sys import stderr
from kettled.daemon import Daemon, get_daemon_pid, DAEMON_STATUSES_ENUM

class Handler:
    def __init__(self, in_memory_only_session=False):
        self.in_memory_only_session = in_memory_only_session

    def init(self):
        try:
            get_daemon_pid()
            stderr.write(DAEMON_STATUSES_ENUM.IS_ALREADY_RUNNING.value)
        except IOError:
            Daemon(in_memory_only_session=self.in_memory_only_session).start()
    
    @staticmethod
    def stop():
        try:
            get_daemon_pid()
            Daemon.stop()
        except IOError:
            stderr.write(DAEMON_STATUSES_ENUM.IS_DOWN.value)