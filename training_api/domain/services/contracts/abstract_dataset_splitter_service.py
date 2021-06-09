from abc import abstractmethod, ABC, ABCMeta


class AbstractDatasetSplitterService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def split_dataset(self, train_ratio: float) -> None: raise NotImplementedError
