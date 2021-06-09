from abc import abstractmethod, ABC, ABCMeta

from domain.models.gluon_dataset import GluonDataset


class AbstractDataLoaderService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_dataset(self, model_name: str, gluon_data: GluonDataset) -> None: raise NotImplementedError

    @abstractmethod
    def get_dataset(self, model_name: str) -> GluonDataset: raise NotImplementedError
