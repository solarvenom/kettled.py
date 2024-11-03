from sys import stderr
from json import loads
from kettled.constants.env import PIPE_FILE
from kettled.constants.enums import COMMAND_PIPE, COMMANDS, EVENT_PARAMETERS, UPDATE_EVENT_PARAMETERS, ERROR_MESSAGES

def pipe_command(command_json):
        with open(PIPE_FILE, 'w') as pipe:
            pipe.write(command_json + '\n')

def read_pipe(daemon):
        with open(PIPE_FILE, 'r') as pipe:
            command_json = pipe.read().strip()
            parsed_command = loads(command_json)
            if daemon.scheduler is not None:
                if parsed_command[COMMAND_PIPE.COMMAND.value] == COMMANDS.LIST.value:
                    daemon.list()
                elif parsed_command[COMMAND_PIPE.COMMAND.value] == COMMANDS.ADD.value:
                    try:
                        daemon.scheduler.set(
                            event_name=parsed_command[COMMAND_PIPE.DATA.value][EVENT_PARAMETERS.EVENT_NAME.value],
                            date_time=parsed_command[COMMAND_PIPE.DATA.value][EVENT_PARAMETERS.DATE_TIME.value],
                            callback=parsed_command[COMMAND_PIPE.DATA.value][EVENT_PARAMETERS.CALLBACK.value])
                    except ValueError as error:
                        stderr.write(str(error))
                elif parsed_command[COMMAND_PIPE.COMMAND.value] == COMMANDS.DELETE.value:
                    daemon.scheduler.remove(event_name=parsed_command[COMMAND_PIPE.DATA.value][EVENT_PARAMETERS.EVENT_NAME.value])
                elif parsed_command[COMMAND_PIPE.COMMAND.value] == COMMANDS.UPDATE.value:
                    try:
                        fields_to_update = parsed_command[COMMAND_PIPE.DATA.value].keys()
                        daemon.scheduler.update(
                            event_name=parsed_command[COMMAND_PIPE.DATA.value][EVENT_PARAMETERS.EVENT_NAME.value],
                            new_event_name=parsed_command[COMMAND_PIPE.DATA.value][UPDATE_EVENT_PARAMETERS.NEW_EVENT_NAME.value] if UPDATE_EVENT_PARAMETERS.NEW_EVENT_NAME.value in fields_to_update else None,
                            new_date_time=parsed_command[COMMAND_PIPE.DATA.value][UPDATE_EVENT_PARAMETERS.NEW_DATE_TIME.value] if UPDATE_EVENT_PARAMETERS.NEW_DATE_TIME.value in fields_to_update else None,
                            new_callback=parsed_command[COMMAND_PIPE.DATA.value][UPDATE_EVENT_PARAMETERS.NEW_CALLBACK.value] if UPDATE_EVENT_PARAMETERS.NEW_CALLBACK.value in fields_to_update else None)
                    except ValueError as error:
                        stderr.write(str(error))
            else:
                stderr.write(ERROR_MESSAGES.SCHEDULER_NOT_RUNNING.value)