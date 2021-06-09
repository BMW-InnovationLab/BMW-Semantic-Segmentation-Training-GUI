from abc import ABC, ABCMeta, abstractmethod
from typing import List


class AbstractContextManagementService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def clean_context(self, gpus_list: List[int]) -> None: raise NotImplementedError
