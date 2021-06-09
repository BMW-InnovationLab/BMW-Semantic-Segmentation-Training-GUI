from abc import abstractmethod, ABC, ABCMeta

from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.models.paths import Paths


class AbstractConfigurationTemplate(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_network_configuration(self, dataset_info: DatasetInformation, config: HyperParameterInformation, paths: Paths) -> object: raise NotImplementedError
