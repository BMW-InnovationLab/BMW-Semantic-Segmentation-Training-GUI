from abc import ABCMeta, ABC, abstractmethod
from typing import  List


class AbstractClassifierService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_classifiers(self) -> List[str]: raise NotImplementedError
