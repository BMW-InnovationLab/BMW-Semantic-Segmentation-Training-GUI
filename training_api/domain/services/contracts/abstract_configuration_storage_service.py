from abc import ABC, abstractmethod, ABCMeta


class AbstractConfigurationStorageService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_configuration(self, model_name: str, configuration_obj: object) -> None: raise NotImplementedError

    @abstractmethod
    def get_configuration(self, model_name: str) -> object: raise NotImplementedError
