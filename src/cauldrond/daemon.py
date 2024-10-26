from os import fork, chdir, setsid, umask, dup2, getpid, remove, kill, path
from sys import exit, stdin, stdout, stderr, executable
from time import sleep
from atexit import register
from datetime import datetime
from signal import SIGTERM
import subprocess
from cauldrond.constants.env import PID_FILE, STD_IN, STD_OUT, STD_ERR, DAEMON_NAME
from cauldrond.constants.enums import ICONS
from cauldrond.scheduler import Scheduler
from cauldrond.constants.enums import MESSAGES

class Daemon:
    def __init__(self, pidfile=PID_FILE, stdin=STD_IN, stdout=STD_OUT, stderr=STD_ERR):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.scheduler = None

    def get_daemon_pid(self):
        pf = open(self.pidfile,'r')
        pid = int(pf.read().strip())
        pf.close()
        return pid

    def daemonize(self):
        try:
            process = subprocess.Popen([executable, "-m", DAEMON_NAME])
            pid = process.pid
            open(self.pidfile,'w+').write(f"{pid}\n")
            
            # self.scheduler = Scheduler()
        except IOError:
            stderr.write("Daemonizing went wrong...")

    def delpid(self):
        remove(self.pidfile)

    def start(self):
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            stderr.write(MESSAGES.IS_ALREADY_RUNNING.value)
            exit(1)
        self.daemonize()
        self.run()
 
    def stop(self):
        try:
            pid = self.get_daemon_pid()
        except IOError:
            pid = None
       
        if not pid:
            stderr.write(f"{ICONS.CRYSTALL_BALL.value} pidfile {self.pidfile} does not exist. {DAEMON_NAME} not running?\n")
            return

        try:
            while 1:
                kill(pid, SIGTERM)
                sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if path.exists(self.pidfile):
                    remove(self.pidfile)
            else:
                print(err)
                exit(1)
 
    def restart(self):
        self.stop()
        self.start()
 
    def run(self):
        stdout.write(MESSAGES.IS_STARTED.value)
        # scheduler = Scheduler()

    def status(self):
        try:
            c_time = path.getctime(self.pidfile) 
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
        print(f"self.scheduler exists: {self.scheduler is not None}")
        if self.scheduler:
            self.scheduler.list()
        # self.scheduler.list()
    
    def raise_if_daemon_is_up(self):
        return self.get_daemon_pid()