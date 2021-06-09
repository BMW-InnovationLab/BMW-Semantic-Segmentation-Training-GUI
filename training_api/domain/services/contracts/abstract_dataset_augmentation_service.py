from abc import abstractmethod, ABC, ABCMeta

from domain.models.dataset_information import DatasetInformation
from domain.models.gluon_dataset import GluonDataset
from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractDatasetAugmentationService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def augment_dataset(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> GluonDataset: raise NotImplementedError
