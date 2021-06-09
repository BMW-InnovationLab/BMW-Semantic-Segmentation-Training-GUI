from typing import List

from pydantic import BaseModel, Field


class HyperParameterInformation(BaseModel):
    lr: float = Field(default=0.001, example=0.001)
    momentum: float = Field(default=0.9, example=0.9)
    weight_decay: float = Field(default=0.0001, example=0.0001)
    num_workers: int = Field(default=1, example=1)
    batch_size: int = Field(default=1, example=1)
    validation_batch_size: int = Field(default=1, example=1)
    epochs: int = Field(default=15, example=15)
    augment_data: bool = Field(default=True, example=True)

    gpus: List[int] = Field(default=[0], example=[0])

    weight_type: str = Field(default="pre_trained", example="pre_trained")  # checkpoint , pretrained_offline etc
    backbone: str = Field(default="resnet101", example="resnet101")
    network: str = Field(default="deeplab", example="deeplab")
    base_weight_name: str = Field(default="deeplab_resnet101", example="deeplab_resnet101")
    # ex: psp_resnet_50 in case of checkpoint and transfer learning from local weights

    crop_size: int = Field(default=480, example=480)
    base_size: int = Field(default=520, example=520)

    pretrained_dataset: str = Field(default="voc", example="voc")  # pretrained dataset voc etc .
    model_name: str = Field(default="sample_model", example="sample_model")  # model name of the training
    base_model_name: str = Field(default="checkpoint_model", example="checkpoint_model")  # in case of pretrained_offline or checkpoint
