import datetime
from typing import Dict

from application.configuration.models.configuration_enum import ConfigurationEnum
from application.configuration.templates.scratch_configuration import ScratchConfiguration
from application.configuration.templates.checkpoint_configuration import CheckpointConfiguration
from application.configuration.templates.pre_trained_configuration import PreTrainedConfiguration
from application.configuration.templates.local_weights_configuration import LocalWeightsConfiguration
from application.configuration.templates.local_classifier_configuration import LocalClassifierConfiguration

from domain.models.paths import Paths
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_configuration_factory import AbstractConfigurationFactory
from domain.services.contracts.abstract_configuration_storage_service import AbstractConfigurationStorageService
from domain.services.contracts.abstract_configuration_template import AbstractConfigurationTemplate
from domain.services.contracts.abstract_path_service import AbstractPathService

from domain.exceptions.configuration_exceptions import ConfigurationTypeNotFound, CheckpointConfigurationInvalid, ConfigurationError


class ConfigurationFactory(AbstractConfigurationFactory):

    def __init__(self, path_service: AbstractPathService, configuration_storage_service: AbstractConfigurationStorageService):
        self.paths: Paths = path_service.get_paths()
        self.configuration_storage_service = configuration_storage_service
        self.configuration_instances: Dict[str, AbstractConfigurationTemplate] = {}
        self.configuration_mappings: Dict[str, AbstractConfigurationTemplate] = {}
        self.__initialize_mappings__()

    def __initialize_mappings__(self) -> None:
        self.configuration_mappings = {
            ConfigurationEnum.SCRATCH.value: ScratchConfiguration,
            ConfigurationEnum.PRETRAINED_ONLINE.value: PreTrainedConfiguration,
            ConfigurationEnum.PRETRAINED_OFFLINE.value: LocalWeightsConfiguration,
            ConfigurationEnum.CHECKPOINT.value: CheckpointConfiguration,
            ConfigurationEnum.PRETRAINED_CLASSIFIER.value: LocalClassifierConfiguration
        }

    def create_configuration(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> None:
        configuration_type: str = config.weight_type.lower()

        try:
            if AbstractConfigurationTemplate in self.configuration_instances:
                return self.configuration_mappings.get(configuration_type.lower())

            else:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Creating Configuration With The Following Parameters:")
                print(config.json(indent=4))
                configuration: AbstractConfigurationTemplate = self.configuration_mappings.get(configuration_type)()
                self.configuration_instances[configuration_type] = configuration
                configuration: object = configuration.create_network_configuration(dataset_info=dataset_info, config=config, paths=self.paths)
                print(configuration)
                self.configuration_storage_service.set_configuration(model_name=config.model_name, configuration_obj=configuration)
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Configuration Created Successfully!")
        except CheckpointConfigurationInvalid as e:
            raise e
        except ConfigurationError as e:
            raise e
        except Exception as e:
            raise ConfigurationTypeNotFound(additional_message=e.__str__(), configuration_type=configuration_type)
