from abc import ABC, ABCMeta, abstractmethod

from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractInferenceModelExportService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_inference_model(self, config: HyperParameterInformation) -> None: raise NotImplementedError

