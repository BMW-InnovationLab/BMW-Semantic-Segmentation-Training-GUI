from abc import ABC, ABCMeta, abstractmethod
from domain.models.models_info import ModelsInfo
from domain.models.pretrained_models import PretrainedModels


class AbstractModelsArchitectureService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_architectures(self) -> ModelsInfo: raise NotImplementedError

    @abstractmethod
    def get_pretrained_models(self) -> PretrainedModels: raise NotImplementedError
