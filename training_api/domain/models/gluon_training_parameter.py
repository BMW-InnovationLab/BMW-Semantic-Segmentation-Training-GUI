from pydantic import BaseModel
from typing import List
from mxnet.gluon import Trainer

from gluoncv.utils.metrics import SegmentationMetric
from gluoncv.utils.parallel import DataParallelModel, DataParallelCriterion
from mxnet.context import Context


class GluonTrainingParameter(BaseModel):
    network: DataParallelModel
    metric: SegmentationMetric
    criterion: DataParallelCriterion
    evaluator: DataParallelModel
    optimizer: Trainer
    ctx_list: List[Context]

    class Config:
        arbitrary_types_allowed = True
