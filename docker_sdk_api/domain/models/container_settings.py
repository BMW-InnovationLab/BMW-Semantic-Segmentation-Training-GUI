from pydantic import BaseModel
from typing import List


class ContainerSettings(BaseModel):
    name: str
    dataset_name: str
    gpus: List[int]
    api_port: int
