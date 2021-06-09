from typing import Dict
from abc import ABC, abstractmethod, ABCMeta


class AbstractDownloadModelsService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_downloadable_models(self) -> Dict[str, str]: raise NotImplementedError
