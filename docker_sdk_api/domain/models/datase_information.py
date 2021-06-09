from typing import List

from pydantic import BaseModel


class DatasetInformation(BaseModel):
    dataset_name: str
    num_classes: int = None
    classes: List[str] = None
