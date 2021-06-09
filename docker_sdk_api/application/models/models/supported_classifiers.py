from enum import Enum


class SupportedClassifiers(Enum):
    resnet50: str = "resnet50_v1"
    resnet101: str = "resnet101_v1"
    resnet50v1b: str = "resnet50_v1b"
    resnet101v1b: str = "resnet101_v1b"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
