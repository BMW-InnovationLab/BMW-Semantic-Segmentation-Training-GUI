from abc import ABC, ABCMeta, abstractmethod

from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractModelTrainEvaluateManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def train_eval_continuously(self, config: HyperParameterInformation) -> None: raise NotImplementedError
