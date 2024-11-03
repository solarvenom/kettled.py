from os import path
from sys import stderr, stdout
from json import dumps
from datetime import datetime
from kettled.daemon.daemon import Daemon, get_daemon_pid
from kettled.daemon.pipes import pipe_command
from kettled.constants.enums import COMMANDS, MESSAGES, COMMAND_PIPE, ICONS
from kettled.constants.env import DAEMON_NAME, PID_FILE

class GeneralHandler:
    def __init__(self, is_persistent=False):
        self.is_persistent = is_persistent

    def init(self):
        try:
            get_daemon_pid()
            stderr.write(MESSAGES.IS_ALREADY_RUNNING.value)
        except IOError:
            Daemon(self.is_persistent).start()
    
    @staticmethod
    def stop():
        try:
            get_daemon_pid()
            Daemon.stop()
        except IOError:
            stderr.write(MESSAGES.IS_DOWN.value)
    
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
                stdout.write(f"{ICONS.KETTLE.value} {DAEMON_NAME} has been up for {total_seconds} seconds.\n")
            elif total_seconds < 3600:
                stdout.write(f"{ICONS.KETTLE.value} {DAEMON_NAME} has been up for {total_seconds // 60} minutes and {total_seconds % 60} seconds.\n")
            else:
                stdout.write(f"{ICONS.KETTLE.value} {DAEMON_NAME} has been up for {total_seconds // 3600} hours, {total_seconds % 3600 // 60} minutes, and {total_seconds % 3600 % 60} seconds.\n")
        return
    
    @staticmethod
    def list():
        try:
            get_daemon_pid()
            pipe_command(dumps({COMMAND_PIPE.COMMAND.value: COMMANDS.LIST.value}))
        except IOError:
            stderr.write(MESSAGES.IS_DOWN.value)