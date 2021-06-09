from typing import List

from pydantic import BaseModel


class ModelsInfo(BaseModel):
    networks: List[str]
    backbones: List[str]