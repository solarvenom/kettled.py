from enum import Enum
from icons_enum import ICONS_ENUM

class TERMINAL_PROMPTS_ENUM(Enum):
    ADD_EVENT_NAME = f"{ICONS_ENUM.KETTLE.value} Please enter event name: "
    ADD_EVENT_DATE_TIME = f"{ICONS_ENUM.KETTLE.value} Please enter event scheduled date: "
    ADD_EVENT_CALLBACK = f"{ICONS_ENUM.KETTLE.value} Please enter event callback: "
    DELETE_EVENT_NAME = f"{ICONS_ENUM.KETTLE.value} Please enter the name of event to be deleted: "
    UPDATE_EVENT_NAME = f"{ICONS_ENUM.KETTLE.value} Please enter the name of event be modified: "
    UPDATE_NEW_EVENT_NAME = f"{ICONS_ENUM.KETTLE.value} Please enter the new event name or leave blank to leave unchanged: "
    UPDATE_NEW_DATE_TIME = f"{ICONS_ENUM.KETTLE.value} Please enter the new event schdeuled date or leave blank to leave unchanged: "
    UPDATE_NEW_CALLBACK = f"{ICONS_ENUM.KETTLE.value} Please enter the new event callback or leave blank to leave unchanged: "