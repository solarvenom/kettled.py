from sys import stderr
from json import loads
from kettled.constants.env import PIPE_FILE
from kettled.constants.enums.pipe_commands_enum import PIPE_COMMANDS_ENUM
from kettled.constants.enums.commands_enum import COMMANDS_ENUM
from kettled.constants.enums.event_parameters_enum import EVENT_PARAMETERS_ENUM
from kettled.constants.enums.update_event_parameters_enum import UPDATE_EVENT_PARAMETERS_ENUM
from kettled.constants.enums.error_messages_enum import ERROR_MESSAGES_ENUM

def pipe_command(command_json):
        with open(PIPE_FILE, 'w') as pipe:
            pipe.write(command_json + '\n')

def read_pipe(daemon):
        with open(PIPE_FILE, 'r') as pipe:
            command_json = pipe.read().strip()
            parsed_command = loads(command_json)
            if daemon.scheduler is not None:
                if parsed_command[PIPE_COMMANDS_ENUM.COMMAND.value] == COMMANDS_ENUM.LIST.value:
                    daemon.list()
                elif parsed_command[PIPE_COMMANDS_ENUM.COMMAND.value] == COMMANDS_ENUM.ADD.value:
                    try:
                        daemon.scheduler.set(
                            event_name=parsed_command[PIPE_COMMANDS_ENUM.DATA.value][EVENT_PARAMETERS_ENUM.EVENT_NAME.value],
                            date_time=parsed_command[PIPE_COMMANDS_ENUM.DATA.value][EVENT_PARAMETERS_ENUM.DATE_TIME.value],
                            callback=parsed_command[PIPE_COMMANDS_ENUM.DATA.value][EVENT_PARAMETERS_ENUM.CALLBACK.value])
                    except ValueError as error:
                        stderr.write(str(error))
                elif parsed_command[PIPE_COMMANDS_ENUM.COMMAND.value] == COMMANDS_ENUM.DELETE.value:
                    daemon.scheduler.remove(event_name=parsed_command[PIPE_COMMANDS_ENUM.DATA.value][EVENT_PARAMETERS_ENUM.EVENT_NAME.value])
                elif parsed_command[PIPE_COMMANDS_ENUM.COMMAND.value] == COMMANDS_ENUM.UPDATE.value:
                    try:
                        fields_to_update = parsed_command[PIPE_COMMANDS_ENUM.DATA.value].keys()
                        daemon.scheduler.update(
                            event_name=parsed_command[PIPE_COMMANDS_ENUM.DATA.value][EVENT_PARAMETERS_ENUM.EVENT_NAME.value],
                            new_event_name=parsed_command[PIPE_COMMANDS_ENUM.DATA.value][UPDATE_EVENT_PARAMETERS_ENUM.NEW_EVENT_NAME.value] if UPDATE_EVENT_PARAMETERS_ENUM.NEW_EVENT_NAME.value in fields_to_update else None,
                            new_date_time=parsed_command[PIPE_COMMANDS_ENUM.DATA.value][UPDATE_EVENT_PARAMETERS_ENUM.NEW_DATE_TIME.value] if UPDATE_EVENT_PARAMETERS_ENUM.NEW_DATE_TIME.value in fields_to_update else None,
                            new_callback=parsed_command[PIPE_COMMANDS_ENUM.DATA.value][UPDATE_EVENT_PARAMETERS_ENUM.NEW_CALLBACK.value] if UPDATE_EVENT_PARAMETERS_ENUM.NEW_CALLBACK.value in fields_to_update else None)
                    except ValueError as error:
                        stderr.write(str(error))
            else:
                stderr.write(ERROR_MESSAGES_ENUM.SCHEDULER_NOT_RUNNING.value)