from typing import List

from pydantic import BaseModel


class PretrainedModels(BaseModel):
    pretrained_networks: List[str]
