from abc import abstractmethod, ABC, ABCMeta


class AbstractConfigurationStorageRepository(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_configuration(self, name: str, configuration_obj: object) -> None: raise NotImplementedError

    @abstractmethod
    def retrieve_configuration(self, name) -> object: raise NotImplementedError
