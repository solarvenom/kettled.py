from enum import Enum

class EnumSuperclass(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))