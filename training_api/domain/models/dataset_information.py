from typing import List

from pydantic import BaseModel


class DatasetInformation(BaseModel):
    num_classes: int
    classes: List[str]
    train_ratio: float
