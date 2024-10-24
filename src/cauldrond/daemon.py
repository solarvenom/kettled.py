from os import fork, chdir, setsid, umask, dup2, getpid, remove, kill, path
from sys import exit, stdin, stdout, stderr
from time import sleep
from atexit import register
from datetime import datetime
from signal import SIGTERM
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
       
    def daemonize(self):
        try:
            pid = fork()
            if pid > 0:
                exit(0)
        except OSError as e:
            stderr.write(f"{ICONS.CRYSTALL_BALL.value} fork #1 failed: {e.errno} {e.strerror}\n")
            exit(1)
       
        chdir("/")
        setsid()
        umask(0)
       
        try:
            pid = fork()
            if pid > 0:
                exit(0)
        except OSError as e:
            stderr.write(f"{ICONS.CRYSTALL_BALL.value} fork #2 failed: {e.errno} {e.strerror}\n")
            exit(1)
       
        stdout.flush()
        stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        dup2(si.fileno(), stdin.fileno())
        dup2(so.fileno(), stdout.fileno())
        dup2(se.fileno(), stderr.fileno())
       
        register(self.delpid)
        pid = str(getpid())
        open(self.pidfile,'w+').write(f"{pid}\n")
       
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
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
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
        scheduler = Scheduler()

        # scheduler.add(timestamp=1, event=StorageEventInput(name="test event", date_time="2024-10-17 09:57:28", callback=print("kekekekeke")))

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