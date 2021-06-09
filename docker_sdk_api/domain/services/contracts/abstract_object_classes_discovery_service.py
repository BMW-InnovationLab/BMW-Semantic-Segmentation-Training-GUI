from abc import ABC, ABCMeta, abstractmethod

from domain.models.datase_information import DatasetInformation


class AbstractObjectClassesDiscoveryService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def discover_object_classes(self, dataset_info: DatasetInformation) -> DatasetInformation: raise NotImplementedError
