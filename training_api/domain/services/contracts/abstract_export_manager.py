from abc import ABC, ABCMeta, abstractmethod

from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractExportManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_trained_model(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> None: raise NotImplementedError
