import os

import mxnet as mx
import numpy as np

from tqdm import tqdm
from mxnet import autograd, Context
from mxnet.gluon import Trainer
from typing import List, Any

from gluoncv.utils.metrics import SegmentationMetric
from gluoncv.utils.parallel import DataParallelCriterion, DataParallelModel

from domain.models.paths import Paths
from domain.models.gluon_dataset import GluonDataset
from domain.models.gluon_training_parameter import GluonTrainingParameter
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.services.contracts.abstract_model_trainer_service import AbstractModelTrainerService
from domain.services.contracts.abstract_path_service import AbstractPathService


class ModelTrainerService(AbstractModelTrainerService):

    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()
        self.best_mIoU: int = 0
        self.mIoU: int = 0
        self.gluon_network = None

    def __train_model(self, train_dataset: Any, criterion: DataParallelCriterion, optimizer: Trainer, batch_size: int, epoch: int):
        progress_data_bar = tqdm(train_dataset)
        train_loss: float = 0.0

        for index, (data, target) in enumerate(progress_data_bar):
            with autograd.record(True):
                outputs = self.gluon_network(data.astype('float32', copy=False))
                losses = criterion(outputs, target)
                mx.nd.waitall()
                autograd.backward(losses)
            optimizer.step(batch_size=batch_size)

            for loss in losses:
                train_loss += np.mean(loss.asnumpy()) / len(losses)
            progress_data_bar.set_description('Epoch %d, training loss %.3f' % (epoch, train_loss / (index + 1)))
            mx.nd.waitall()

    def __evaluate_model(self, validation_dataset: Any, metric: SegmentationMetric, evaluator: DataParallelModel, epoch: int, ctx_list: List[Context]):
        metric.reset()
        progress_data_bar = tqdm(validation_dataset)
        for index, (data, target) in enumerate(progress_data_bar):
            outputs = evaluator(data.astype('float32', copy=False))
            outputs = [x[0] for x in outputs]
            targets = mx.gluon.utils.split_and_load(data=target, ctx_list=ctx_list, even_split=False)
            metric.update(targets, outputs)
            pixAcc, self.mIoU = metric.get()
            progress_data_bar.set_description('Epoch %d, validation pixAcc: %.3f, mIoU: %.3f' % (epoch, pixAcc, self.mIoU))
            if self.mIoU >= self.best_mIoU:
                self.best_mIoU = self.mIoU
                self.gluon_network.module.save_parameters(os.path.join(self.paths.model_dir, "model_best.params"))
            print("BEST mIoU IS: " + str(self.best_mIoU), flush=True)
            mx.nd.waitall()

    def training_loop(self, config: HyperParameterInformation, gluon_dataset: GluonDataset,
                      gluon_training_params: GluonTrainingParameter) -> None:
        batch_size_per_context: int = config.batch_size * max(1, len(config.gpus))
        self.gluon_network: object = gluon_training_params.network
        for epoch in range(0, config.epochs):
            self.__train_model(train_dataset=gluon_dataset.train_dataset, criterion=gluon_training_params.criterion, optimizer=gluon_training_params.optimizer,
                               batch_size=batch_size_per_context, epoch=epoch)
            self.__evaluate_model(validation_dataset=gluon_dataset.validation_dataset, metric=gluon_training_params.metric,
                                  evaluator=gluon_training_params.evaluator, epoch=epoch, ctx_list=gluon_training_params.ctx_list)
