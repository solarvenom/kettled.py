from enum import Enum

class GenericEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))