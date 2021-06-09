from abc import abstractmethod, ABC, ABCMeta

from domain.models.gluon_dataset import GluonDataset


class AbstractDataLoaderRepository(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_data_loader(self, name: str, gluon_dataset: GluonDataset) -> None: raise NotImplementedError

    @abstractmethod
    def retrieve_data_loader(self, name) -> GluonDataset: raise NotImplementedError
