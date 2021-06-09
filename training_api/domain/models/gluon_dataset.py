from typing import Any

from pydantic import BaseModel


class GluonDataset(BaseModel):
    train_dataset: Any
    validation_dataset: Any
