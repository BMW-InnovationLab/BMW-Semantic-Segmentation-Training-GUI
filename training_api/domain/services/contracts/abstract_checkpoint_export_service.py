from abc import ABC, ABCMeta, abstractmethod

from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractCheckpointExportService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_checkpoint(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> None: raise NotImplementedError
