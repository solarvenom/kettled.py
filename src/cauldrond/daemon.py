from os import fork, chdir, setsid, umask, getpid, remove, kill, path
from sys import exit, stdout, stderr
from time import sleep
from atexit import register
from datetime import datetime
from signal import SIGTERM
from json import loads
from cauldrond.constants.env import DAEMON_NAME, PID_FILE, PIPE_FILE
from cauldrond.constants.enums import ICONS, COMMANDS
from cauldrond.scheduler import Scheduler
from cauldrond.constants.enums import MESSAGES, ERROR_MESSAGES, UPDATE_EVENT_PARAMETERS, COMMAND_MESSAGE, EVENT_PARAMETERS

def get_daemon_pid():
    pf = open(PID_FILE,'r')
    pid = int(pf.read().strip())
    pf.close()
    return pid

class Daemon:
    def __init__(self):
        self.scheduler = None
        self.pipe_updated_at = 0

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
                    remove(PIPE_FILE)
            else:
                stderr.write(err)
                exit(1)

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
    
    @staticmethod
    def pipe_command(command_json):
        with open(PIPE_FILE, 'w') as pipe:
            pipe.write(command_json + '\n')

    def read_pipe(self):
        with open(PIPE_FILE, 'r') as pipe:
            command_json = pipe.read().strip()
            parsed_command = loads(command_json)
            if self.scheduler is not None:
                if parsed_command[COMMAND_MESSAGE.COMMAND.value] == COMMANDS.LIST.value:
                    self.list()
                elif parsed_command[COMMAND_MESSAGE.COMMAND.value] == COMMANDS.ADD.value:
                    try:
                        self.scheduler.set(
                            event_name=parsed_command[COMMAND_MESSAGE.DATA.value][EVENT_PARAMETERS.EVENT_NAME.value],
                            date_time=parsed_command[COMMAND_MESSAGE.DATA.value][EVENT_PARAMETERS.DATE_TIME.value],
                            callback=parsed_command[COMMAND_MESSAGE.DATA.value][EVENT_PARAMETERS.CALLBACK.value])
                    except ValueError as error:
                        stderr.write(str(error))
                elif parsed_command[COMMAND_MESSAGE.COMMAND.value] == COMMANDS.DELETE.value:
                    self.scheduler.remove(event_name=parsed_command[COMMAND_MESSAGE.DATA.value][EVENT_PARAMETERS.EVENT_NAME.value])
                elif parsed_command[COMMAND_MESSAGE.COMMAND.value] == COMMANDS.UPDATE.value:
                    try:
                        fields_to_update = parsed_command[COMMAND_MESSAGE.DATA.value].keys()
                        self.scheduler.update(
                            event_name=parsed_command[COMMAND_MESSAGE.DATA.value][EVENT_PARAMETERS.EVENT_NAME.value],
                            new_event_name=parsed_command[COMMAND_MESSAGE.DATA.value][UPDATE_EVENT_PARAMETERS.NEW_EVENT_NAME.value] if UPDATE_EVENT_PARAMETERS.NEW_EVENT_NAME.value in fields_to_update else None,
                            new_date_time=parsed_command[COMMAND_MESSAGE.DATA.value][UPDATE_EVENT_PARAMETERS.NEW_DATE_TIME.value] if UPDATE_EVENT_PARAMETERS.NEW_DATE_TIME.value in fields_to_update else None,
                            new_callback=parsed_command[COMMAND_MESSAGE.DATA.value][UPDATE_EVENT_PARAMETERS.NEW_CALLBACK.value] if UPDATE_EVENT_PARAMETERS.NEW_CALLBACK.value in fields_to_update else None)
                    except ValueError as error:
                        stderr.write(str(error))
            else:
                stderr.write(ERROR_MESSAGES.SCHEDULER_NOT_RUNNING.value)
            

    def list(self):
        if self.scheduler:
            self.scheduler.list()

    def run(self):
        stdout.write(MESSAGES.IS_STARTED.value)
        self.scheduler = Scheduler()
        while True:
            current_pipe_updated_at = path.getmtime(PIPE_FILE)
            if current_pipe_updated_at > self.pipe_updated_at:
                self.pipe_updated_at = current_pipe_updated_at
                self.read_pipe()
            sleep(0.5)