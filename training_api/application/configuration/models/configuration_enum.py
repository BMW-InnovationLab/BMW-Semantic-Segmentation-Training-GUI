from enum import Enum


class ConfigurationEnum(Enum):
    PRETRAINED_ONLINE = "pre_trained"
    PRETRAINED_CLASSIFIER = "pre_trained_classifier"
    PRETRAINED_OFFLINE = "pre_trained_offline"
    SCRATCH = "from_scratch"
    CHECKPOINT = "from_checkpoint"
