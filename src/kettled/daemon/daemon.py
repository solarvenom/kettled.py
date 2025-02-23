from os import fork, chdir, setsid, umask, getpid, remove, kill, path
from sys import exit, stdout, stderr
from time import sleep
from atexit import register
from datetime import datetime
from signal import SIGTERM
from kettled.constants.env import PID_FILE, PIPE_FILE
from kettled.constants.enums.icons_enum import ICONS_ENUM
from kettled.constants.enums.messages_enum import MESSAGES_ENUM
from kettled.constants.enums.event_parameters_enum import EVENT_PARAMETERS_ENUM
from kettled.constants.enums.recurrency_options_enum import RECURRENCY_OPTIONS_ENUM
from kettled.constants.enums.fallback_options_enum import FALLBACK_DIRECTIVES_ENUM
from kettled.utils.next_recurrency_calculator import get_next_datetime
from kettled.daemon.scheduler import Scheduler
from kettled.daemon.pipes import read_pipe

def get_daemon_pid():
    pf = open(PID_FILE,'r')
    pid = int(pf.read().strip())
    pf.close()
    return pid

class Daemon:
    def __init__(self, persistent_session = False):
        self.persistent_session = persistent_session
        self.scheduler = None
        self.pipe_updated_at = 0

    def daemonize(self):
        try:
            pid = fork()
            if pid > 0:
                exit(0)
        except OSError as error:
            stderr.write(f"{ICONS_ENUM.SKULL.value} Fork #1 failed: {error.errno} {error.strerror}\n")
            exit(1)
        chdir("/")
        setsid()
        umask(0)
       
        try:
            pid = fork()
            if pid > 0:
                exit(0)
        except OSError as error:
            stderr.write(f"{ICONS_ENUM.SKULL.value} Fork #2 failed: {error.errno} {error.strerror}\n")
            exit(1)
        
        register(self.del_tmp_files)
        pid = str(getpid())
        open(PID_FILE,'w+').write("%s\n" % pid)
        with open(PIPE_FILE, 'w'):
            pass
        self.pipe_updated_at = path.getmtime(PIPE_FILE)

    @staticmethod
    def del_tmp_files():
        remove(PID_FILE)
        remove(PIPE_FILE)

    def start(self):
        try:
            pid = get_daemon_pid()
        except IOError:
            pid = None

        if pid:
            stderr.write(MESSAGES_ENUM.IS_ALREADY_RUNNING.value)
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
            stderr.write(MESSAGES_ENUM.IS_NOT_RUNNING.value)
            return
        try:
            while 1:
                kill(pid, SIGTERM)
                sleep(0.1)
        except OSError as error:
            error = str(error)
            if error.find("No such process") > 0:
                if path.exists(PID_FILE):
                    remove(PID_FILE)
                    remove(PIPE_FILE)
            else:
                stderr.write(error)
                exit(1)
        finally:
            stdout.write(MESSAGES_ENUM.IS_TERMINATED.value)
    
    def list(self):
        if self.scheduler:
            self.scheduler.list()

    def run(self):
        stdout.write(MESSAGES_ENUM.IS_STARTED.value)
        self.scheduler = Scheduler(persistent_session=self.persistent_session)
        try:
            current_timestamp = int(datetime.now().timestamp())
            outdated_events = [key for key in self.scheduler.in_memory_storage if key < current_timestamp]
            outdated_events_to_execute = []
            print(f"************* self.scheduler.in_memory_storage ****************")
            print(self.scheduler.in_memory_storage)
            print(f"************* self.scheduler.in_memory_storage ****************")
            for outdated_event in outdated_events:
                fallback_directive = outdated_event[EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value]
                print(f"************* outdated_event ****************")
                print(outdated_event)
                print(f"************* outdated_event ****************")
                if fallback_directive != FALLBACK_DIRECTIVES_ENUM.IGNORE:
                    outdated_events_to_execute.append(outdated_event)
                # self.scheduler.in_memory_storage.pop(key)
                # self.scheduler.remove(event_name=outdated_event[key][EVENT_PARAMETERS_ENUM.EVENT_NAME.value])
                
            # for event in outdated_events_to_execute:
            #     if fallback_directive != FALLBACK_DIRECTIVES_ENUM.IGNORE:
            #         if fallback_directive == FALLBACK_DIRECTIVES_ENUM.EXECUTE_AS_SOON_AS_POSSIBLE:
            #             outdated_events_to_execute.append(self.scheduler.in_memory_storage[key])
            #         elif fallback_directive == FALLBACK_DIRECTIVES_ENUM.EXECUTE_ON_NEXT_RECURRENCY:
            #             self.scheduler.set(
            #                 event_name=, date_time, recurrency, fallback_directive, callback
            #             )
        except KeyError:
            pass
        while True:
            current_timestamp = int(datetime.now().timestamp())
            try:
                current_timestamp_events = self.scheduler.in_memory_storage[current_timestamp]
                for event_name, event_details in current_timestamp_events.items():
                    execute_scheduled_events(event_details)
            except KeyError:
                pass
            current_pipe_updated_at = path.getmtime(PIPE_FILE)
            if current_pipe_updated_at > self.pipe_updated_at:
                self.pipe_updated_at = current_pipe_updated_at
                read_pipe(self)
            sleep(0.5)

    def execute_scheduled_events(self, event_details):
        eval(event_details[EVENT_PARAMETERS_ENUM.CALLBACK.value]())

        self.scheduler.remove(event_name=event_name)

        if event_details[EVENT_PARAMETERS_ENUM.RECURRENCY.value] != RECURRENCY_OPTIONS_ENUM.NOT_RECURRING.value:
            next_date_time = get_next_datetime(event_details[EVENT_PARAMETERS_ENUM.DATE_TIME.value], event_details[EVENT_PARAMETERS_ENUM.RECURRENCY.value])
            self.scheduler.set(
                event_name = event_name,
                date_time = next_date_time,
                recurrency = event_details[EVENT_PARAMETERS_ENUM.RECURRENCY.value],
                fallback_directive = event_details[EVENT_PARAMETERS_ENUM.FALLBACK_DIRECTIVE.value],
                callback = event_details[EVENT_PARAMETERS_ENUM.CALLBACK.value]
            )
