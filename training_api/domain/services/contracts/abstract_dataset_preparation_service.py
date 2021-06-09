from abc import abstractmethod, ABC, ABCMeta

from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractDatasetPreparationManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def prepare_dataset(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> None: raise NotImplementedError
