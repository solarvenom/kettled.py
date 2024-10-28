from os import fork, chdir, setsid, umask, dup2, getpid, remove, kill, path
from sys import exit, stdin, stdout, stderr, executable
from time import sleep
from atexit import register
from datetime import datetime
from signal import SIGTERM
from cauldrond.constants.env import PID_FILE, STD_IN, STD_OUT, STD_ERR, DAEMON_NAME
from cauldrond.constants.enums import ICONS
from cauldrond.scheduler import Scheduler
from cauldrond.constants.enums import MESSAGES

def get_daemon_pid():
    pf = open(PID_FILE,'r')
    pid = int(pf.read().strip())
    pf.close()
    return pid

def raise_if_daemon_is_up():
    return get_daemon_pid()

class Daemon:
    def __init__(self, stdin=STD_IN, stdout=STD_OUT, stderr=STD_ERR):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.scheduler = None

    def daemonize(self):
        try:
            pid = fork()
            if pid > 0:
                exit(0)
        except OSError as e:
            stderr.write(f"{ICONS.SKULL.value} Fork #1 failed: {e.errno} {e.strerror}\n")
            exit(1)
       
        chdir("/")
        setsid()
        umask(0)
       
        try:
            pid = fork()
            if pid > 0:
                exit(0)
        except OSError as e:
            stderr.write(f"{ICONS.SKULL.value} Fork #2 failed: {e.errno} {e.strerror}\n")
            exit(1)
        
        register(self.delpid)
        pid = str(getpid())
        open(PID_FILE,'w+').write("%s\n" % pid)

    @staticmethod
    def delpid():
        remove(PID_FILE)

    def start(self):
        try:
            pid = get_daemon_pid()
        except IOError:
            pid = None

        if pid:
            stderr.write(MESSAGES.IS_ALREADY_RUNNING.value)
            exit(1)
        self.daemonize()
        self.run()

    @staticmethod
    def stop():
        try:
            pid = get_daemon_pid()
        except IOError:
            pid = None
        
        if not pid:
            stderr.write(f"{ICONS.CRYSTALL_BALL.value} pidfile {PID_FILE} does not exist. {DAEMON_NAME} not running?\n")
            return

        try:
            while 1:
                kill(pid, SIGTERM)
                sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if path.exists(PID_FILE):
                    remove(PID_FILE)
            else:
                stderr.write(err)
                exit(1)

    def run(self):
        stdout.write(MESSAGES.IS_STARTED.value)
        self.scheduler = Scheduler()
        while True:
            sleep(1)
        # scheduler = Scheduler()

    @staticmethod
    def status():
        try:
            c_time = path.getctime(PID_FILE)
        except IOError:
            c_time = None
    
        if not c_time:
            stdout.write(MESSAGES.IS_DOWN.value)
        else:
            total_seconds = int((datetime.now() - datetime.fromtimestamp(c_time)).total_seconds())
            if total_seconds < 60:
                stdout.write(f"{ICONS.CRYSTALL_BALL.value} {DAEMON_NAME} has been up for {total_seconds} seconds.\n")
            elif total_seconds < 3600:
                stdout.write(f"{ICONS.CRYSTALL_BALL.value} {DAEMON_NAME} has been up for {total_seconds // 60} minutes and {total_seconds % 60} seconds.\n")
            else:
                stdout.write(f"{ICONS.CRYSTALL_BALL.value} {DAEMON_NAME} has been up for {total_seconds // 3600} hours, {total_seconds % 3600 // 60} minutes, and {total_seconds % 3600 % 60} seconds.\n")
        return
    
    def list(self):
        if self.scheduler:
            self.scheduler.list()
    