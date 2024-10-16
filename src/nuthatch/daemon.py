
import sys, os, time, atexit
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
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
       
        os.chdir("/")
        os.setsid()
        os.umask(0)
       
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
       
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
       
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("%s\n" % pid)
       
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
       
            if pid:
                message = "pidfile %s already exist. Nuthatch already running?\n"
                sys.stderr.write(message % self.pidfile)
                sys.exit(1)
               
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
            sys.stderr.write(message % self.pidfile)
            return
 
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(err)
                sys.exit(1)
 
    def restart(self):
        self.stop()
        self.start()
 
    def run(self):
        print("Nuthatch started")

    def status(self):
        try:
            c_time = os.path.getctime(self.pidfile) 
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
            
        sys.stderr.write(message)
        return