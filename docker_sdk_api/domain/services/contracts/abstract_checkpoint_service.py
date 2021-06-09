from abc import ABCMeta, ABC, abstractmethod
from typing import Dict


class AbstractCheckpointService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_checkpoints(self) -> Dict[str, str]: raise NotImplementedError
