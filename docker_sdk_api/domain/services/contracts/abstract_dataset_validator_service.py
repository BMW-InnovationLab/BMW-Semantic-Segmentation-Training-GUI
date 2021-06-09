from abc import ABC, ABCMeta, abstractmethod

from domain.models.datase_information import DatasetInformation


class AbstractDatasetValidatorService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate_dataset(self, dataset_info: DatasetInformation) -> None: raise NotImplementedError
