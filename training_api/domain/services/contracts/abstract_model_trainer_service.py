from abc import ABC, ABCMeta, abstractmethod

from domain.models.gluon_dataset import GluonDataset
from domain.models.gluon_training_parameter import GluonTrainingParameter
from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractModelTrainerService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def training_loop(self, config: HyperParameterInformation, gluon_dataset: GluonDataset,
                      gluon_training_params: GluonTrainingParameter) -> None: raise NotImplementedError
