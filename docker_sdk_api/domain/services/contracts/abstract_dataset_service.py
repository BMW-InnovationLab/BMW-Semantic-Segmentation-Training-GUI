from abc import ABCMeta, ABC, abstractmethod
from typing import List


class AbstractDatasetService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_datasets(self) -> List[str]: raise NotImplementedError
