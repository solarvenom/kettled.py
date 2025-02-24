from .enums_superclass import GenericEnum
from kettled.constants.enums.icons_enum import ICONS_ENUM

class TERMINAL_PROMPTS_ENUM(GenericEnum):
    ADD_EVENT_NAME = f"{ICONS_ENUM.KETTLE.value} Please enter event name: "
    ADD_EVENT_DATE_TIME = f"{ICONS_ENUM.KETTLE.value} Please enter event scheduled date: "
    ADD_EVENT_RECURRENCY = f"{ICONS_ENUM.KETTLE.value} Please enter event recurrency (Will default to 'not_recurring' if not provided): "
    ADD_EVENT_FALLBACK_DIRECTIVE = f"{ICONS_ENUM.KETTLE.value} Please enter event fallback directive (Will default to 'execute_as_soon_as_possible' if not provided): "
    ADD_EVENT_CALLBACK = f"{ICONS_ENUM.KETTLE.value} Please enter event callback: "
    DELETE_EVENT_NAME = f"{ICONS_ENUM.KETTLE.value} Please enter the name of event to be deleted: "
    UPDATE_EVENT_NAME = f"{ICONS_ENUM.KETTLE.value} Please enter the name of event be modified: "
    UPDATE_NEW_EVENT_NAME = f"{ICONS_ENUM.KETTLE.value} Please enter the new event name or leave blank to keep unchanged: "
    UPDATE_NEW_DATE_TIME = f"{ICONS_ENUM.KETTLE.value} Please enter the new event schdeuled date or leave blank to keep unchanged: "
    UPDATE_NEW_RECURRENCY = f"{ICONS_ENUM.KETTLE.value} Please enter the new event recurrency or leave blank to keep unchanged: "
    UPDATE_NEW_FALLBACK_DIRECTIVE = f"{ICONS_ENUM.KETTLE.value} Please enter the new event fallback directive or leave blank to keep unchanged: "
    UPDATE_NEW_CALLBACK = f"{ICONS_ENUM.KETTLE.value} Please enter the new event callback or leave blank to keep unchanged: "