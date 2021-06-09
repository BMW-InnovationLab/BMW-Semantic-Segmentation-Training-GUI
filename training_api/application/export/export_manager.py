import datetime
from application.configuration.models.configuration_enum import ConfigurationEnum
from application.export.services.inference_model_export_service import InferenceModelExportService

from domain.models.paths import Paths
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.services.contracts.abstract_checkpoint_export_service import AbstractCheckpointExportService
from domain.services.contracts.abstract_export_manager import AbstractExportManager
from domain.services.contracts.abstract_memory_context_managment import AbstractContextManagementService
from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_servable_export_service import AbstractServableExportService

from domain.exceptions.application_error import ApplicationError


class ExportManager(AbstractExportManager):

    def __init__(self, path_service: AbstractPathService, checkpoint_export_service: AbstractCheckpointExportService,
                 inference_model_export_service: InferenceModelExportService,
                 servable_export_service: AbstractServableExportService, context_management_service: AbstractContextManagementService):
        self.paths: Paths = path_service.get_paths()
        self.checkpoint_export_service = checkpoint_export_service
        self.inference_model_export_service = inference_model_export_service
        self.servable_export_service = servable_export_service
        self.context_management_service = context_management_service

    def __adjust_configuration(self, config: HyperParameterInformation):
        if config.weight_type in [ConfigurationEnum.PRETRAINED_OFFLINE.value, ConfigurationEnum.CHECKPOINT.value]:
            configuration_info = config.base_weight_name.split('_')
            config.network, config.backbone = configuration_info[0], configuration_info[1]
        return config

    def save_trained_model(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> None:
        try:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")+"Exporting model")
            config: HyperParameterInformation = self.__adjust_configuration(config=config)
            self.checkpoint_export_service.create_checkpoint(dataset_info=dataset_info, config=config)
            self.inference_model_export_service.create_inference_model(config=config)
            self.servable_export_service.create_servable_model(config=config)
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")+"Exporting Completed!")
            self.context_management_service.clean_context(gpus_list=config.gpus)
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")+"Memory Context Cleared!")
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")+"Training Job Completed Successfully!")

        except ApplicationError as e:
            raise e
