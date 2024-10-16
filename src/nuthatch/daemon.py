from os import fork, chdir, setsid, umask, dup2, getpid, remove, kill, path
from sys import exit, stdin, stdout, stderr
from time import sleep
from atexit import register
from datetime import datetime
from signal import SIGTERM
import env
 
class Daemon:
    def __init__(self, pidfile=env.PID_FILE, stdin=env.STD_IN, stdout=env.STD_OUT, stderr=env.STD_ERR):
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
            stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            exit(1)
       
        chdir("/")
        setsid()
        umask(0)
       
        try:
            pid = fork()
            if pid > 0:
                exit(0)
        except OSError as e:
            stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
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
        open(self.pidfile,'w+').write("%s\n" % pid)
       
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
                message = "pidfile %s already exist. Nuthatch already running?\n"
                stderr.write(message % self.pidfile)
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
            message = "pidfile %s does not exist. Nuthatch not running?\n"
            stderr.write(message % self.pidfile)
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
        stderr.write("Nuthatch started\n")

    def status(self):
        try:
            c_time = path.getctime(self.pidfile) 
        except IOError:
            c_time = None
    
        if not c_time:
            message = "Nuthatch is down\n"
        else:
            total_seconds = int((datetime.now() - datetime.fromtimestamp(c_time)).total_seconds())
            if total_seconds < 60:
                message = f"Nuthatch has been running for {total_seconds} seconds.\n"
            elif total_seconds < 3600:
                message = f"Nuthatch has been running for {total_seconds // 60} minutes and {total_seconds % 60} seconds.\n"
            else:
                message = f"Nuthatch has been running for {total_seconds // 3600} hours, {total_seconds % 3600 // 60} minutes, and {total_seconds % 3600 % 60} seconds.\n"
            
        stderr.write(message)
        return