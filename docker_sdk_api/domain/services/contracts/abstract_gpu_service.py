from typing import Dict
from abc import ABC, abstractmethod, ABCMeta


class AbstractGpuService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_gpu_info(self) -> Dict[str, str]: raise NotImplementedError
