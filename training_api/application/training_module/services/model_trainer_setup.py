import mxnet as mx

from mxnet.gluon import Trainer
from typing import List, Dict

from gluoncv.utils import LRScheduler
from gluoncv.utils.parallel import DataParallelModel, DataParallelCriterion
from gluoncv.utils.metrics import SegmentationMetric
from gluoncv.model_zoo.segbase import SegEvalModel
from gluoncv.loss import MixSoftmaxCrossEntropyLoss
from gluoncv.data.pascal_voc.segmentation import VOCSegmentation

from domain.models.gluon_training_parameter import GluonTrainingParameter
from domain.models.gluon_dataset import GluonDataset
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_model_trainer_setup import AbstractModelTrainerSetup


class ModelTrainerSetup(AbstractModelTrainerSetup):

    def __set_ctx(self, gpus_list: List[int]) -> List:
        gpu_count: int = mx.util.get_gpu_count()
        if gpu_count > 0:
            ctx = [mx.gpu(gpu) for gpu in gpus_list] if gpus_list[0] != -1 else [mx.cpu(0)]
        else:
            ctx = [mx.cpu(0)]
        return ctx

    def setup_training(self, config: HyperParameterInformation, gluon_dataset: GluonDataset,
                       gluon_network: object) -> GluonTrainingParameter:
        ctx_list: List[mx.context.Context] = self.__set_ctx(gpus_list=config.gpus)

        gluon_network.collect_params().reset_ctx(ctx_list)
        gluon_network.cast('float32')
        network: DataParallelModel = DataParallelModel(module=gluon_network, ctx_list=ctx_list, sync=False)
        evaluator: DataParallelModel = DataParallelModel(module=SegEvalModel(gluon_network), ctx_list=ctx_list)
        criterion_loss: MixSoftmaxCrossEntropyLoss = MixSoftmaxCrossEntropyLoss(aux=False, aux_weight=0.5)
        criterion: DataParallelCriterion = DataParallelCriterion(module=criterion_loss, ctx_list=ctx_list, sync=False)
        lr_scheduler: LRScheduler = LRScheduler(mode='poly', base_lr=config.lr, nepochs=config.epochs, iters_per_epoch=len(gluon_dataset.train_dataset),
                                                power=0.9)
        kv = mx.kv.create('device')
        optimizer_params: Dict = {'lr_scheduler': lr_scheduler,
                                  'wd': config.weight_decay,
                                  'momentum': config.momentum,
                                  'learning_rate': config.lr,
                                  'clip_gradient': 5
                                  }
        optimizer: Trainer = Trainer(network.module.collect_params(), 'sgd',
                                     optimizer_params, kvstore=kv)
        metric: SegmentationMetric = SegmentationMetric(VOCSegmentation.NUM_CLASS)

        return GluonTrainingParameter(network=network, metric=metric, criterion=criterion, evaluator=evaluator, optimizer=optimizer, ctx_list=ctx_list)
