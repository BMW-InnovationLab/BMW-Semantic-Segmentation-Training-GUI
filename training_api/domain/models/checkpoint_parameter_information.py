from typing import List

from pydantic import BaseModel


class CheckpointParameterInfo(BaseModel):
    lr: float
    momentum: float
    weight_decay: float
    num_workers: int
    batch_size: int
    epochs: int

    backbone: str
    network: str

    checkpoint_name: str  # model name of the training

    num_classes: int
    classes_names: List[str]

    inference_engine_name: str
    type: str
