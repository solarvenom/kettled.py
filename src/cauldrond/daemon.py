import threading 
from time import sleep
import random
from cauldrond.scheduler import Scheduler
from cauldrond.constants.enums import MESSAGES, ICONS
from cauldrond.constants.env import DAEMON_NAME

class Daemon:
    def __init__(self, timeout = 1):
        self.timeout = timeout
        self.thread = self.init_thread()
        self.terminate_daemon = False
        self.scheduler = Scheduler()
        self.thread.start()

    def init_thread(self):
        cauldrond_daemon = self.find_cauldrond_daemon()
        if cauldrond_daemon is not None:
            return cauldrond_daemon
        else:
            inited_thread = threading.Thread(target=self.run, daemon=True, name=DAEMON_NAME)
            inited_thread.start()
            return inited_thread

    def set_timeout(self, timeout):
        self.timeout = timeout

    def find_cauldrond_daemon(self):
        for active_thread in threading.enumerate():
            if active_thread.name == DAEMON_NAME:
                return active_thread
        return None
      
    def run(self):
        print(f'Daemon thread: {self.thread.daemon}')
        while True:
            timeout = random.randint(1, 9)
            self.set_timeout(timeout)
            print(f"Daemong running with interval of {self.timeout} secs")
            for active_thread in threading.enumerate(): 
                print(active_thread.name)
            sleep(self.timeout)
            if self.terminate_daemon is True:
                break
    
    # def stop(self):
    #     self.terminate_daemon = True