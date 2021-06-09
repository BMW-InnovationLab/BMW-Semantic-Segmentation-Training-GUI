from dependency_injector import containers, providers

from application.path.services.path_service import PathService

from application.data_preparation.services.data_loader_service import DataLoaderService
from application.data_preparation.dataset_preparation_manager import DatasetPreparationManager
from application.data_preparation.services.dataset_splitter_service import DatasetSplitterService
from application.data_preparation.repositories.data_loader_repository import DataLoaderRepository
from application.data_preparation.services.dataset_augmentation_service import DatasetAugmentationService

from application.configuration.services.configuration_factory import ConfigurationFactory
from application.configuration.services.configuration_storage_service import ConfigurationStorageService
from application.configuration.repositories.configuration_storage_repository import ConfigurationStorageRepository

from application.training_module.services.model_trainer_setup import ModelTrainerSetup
from application.training_module.services.model_trainer_service import ModelTrainerService
from application.training_module.model_train_evaluate_manager import ModelTrainEvaluateManager

from application.export.export_manager import ExportManager
from application.export.services.servable_export_service import ServableExportService
from application.export.services.checkpoint_export_service import CheckpointExportService
from application.export.services.context_managment_service import ContextManagementService
from application.export.services.inference_model_export_service import InferenceModelExportService

from domain.repositries.contracts.abstract_data_loader_repository import AbstractDataLoaderRepository
from domain.services.contracts.abstract_checkpoint_export_service import AbstractCheckpointExportService
from domain.repositries.contracts.abstract_configuration_storage_repository import AbstractConfigurationStorageRepository

from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_export_manager import AbstractExportManager
from domain.services.contracts.abstract_data_loader_service import AbstractDataLoaderService
from domain.services.contracts.abstract_model_trainer_setup import AbstractModelTrainerSetup
from domain.services.contracts.abstract_model_trainer_service import AbstractModelTrainerService
from domain.services.contracts.abstract_configuration_factory import AbstractConfigurationFactory
from domain.services.contracts.abstract_servable_export_service import AbstractServableExportService
from domain.services.contracts.abstract_dataset_splitter_service import AbstractDatasetSplitterService
from domain.services.contracts.abstract_memory_context_managment import AbstractContextManagementService
from domain.services.contracts.abstract_dataset_preparation_service import AbstractDatasetPreparationManager
from domain.services.contracts.abstract_model_train_evaluate_manager import AbstractModelTrainEvaluateManager
from domain.services.contracts.abstract_dataset_augmentation_service import AbstractDatasetAugmentationService
from domain.services.contracts.abstract_configuration_storage_service import AbstractConfigurationStorageService
from domain.services.contracts.abstract_inference_model_export_service import AbstractInferenceModelExportService


class Repositories(containers.DeclarativeContainer):
    data_loader_repository = providers.Singleton(AbstractDataLoaderRepository.register(DataLoaderRepository))
    configuration_storage_repository = providers.Singleton(AbstractConfigurationStorageRepository.register(ConfigurationStorageRepository))


class Services(containers.DeclarativeContainer):
    path_provider = providers.Singleton(AbstractPathService.register(PathService))

    dataset_splitter_service = providers.Factory(AbstractDatasetSplitterService.register(DatasetSplitterService), path_service=path_provider)
    dataset_augmentation_service = providers.Factory(AbstractDatasetAugmentationService.register(DatasetAugmentationService), path_service=path_provider)
    data_loader_service = providers.Factory(AbstractDataLoaderService.register(DataLoaderService), data_loader_repository=Repositories.data_loader_repository)

    configuration_storage_service = providers.Factory(AbstractConfigurationStorageService.register(ConfigurationStorageService),
                                                      configuration_storage_repository=Repositories.configuration_storage_repository)

    model_trainer_setup = providers.Factory(AbstractModelTrainerSetup.register(ModelTrainerSetup))
    model_trainer_service = providers.Factory(AbstractModelTrainerService.register(ModelTrainerService), path_service=path_provider)

    checkpoint_export_service = providers.Factory(AbstractCheckpointExportService.register(CheckpointExportService), path_service=path_provider)
    inference_model_export_service = providers.Factory(AbstractInferenceModelExportService.register(InferenceModelExportService), path_service=path_provider)
    servable_export_service = providers.Factory(AbstractServableExportService.register(ServableExportService), path_service=path_provider)
    context_management_service = providers.Factory(AbstractContextManagementService.register(ContextManagementService))


class Managers(containers.DeclarativeContainer):
    dataset_preparation_manager = providers.Factory(AbstractDatasetPreparationManager.register(DatasetPreparationManager),
                                                    dataset_splitter_service=Services.dataset_splitter_service,
                                                    dataset_augmentation_service=Services.dataset_augmentation_service,
                                                    data_loader_service=Services.data_loader_service)

    configuration_factory = providers.Factory(AbstractConfigurationFactory.register(ConfigurationFactory), path_service=Services.path_provider,
                                              configuration_storage_service=Services.configuration_storage_service)

    model_train_evaluate_manager = providers.Factory(AbstractModelTrainEvaluateManager.register(ModelTrainEvaluateManager),
                                                     data_loader_service=Services.data_loader_service,
                                                     configuration_storage_service=Services.configuration_storage_service,
                                                     model_trainer_setup=Services.model_trainer_setup,
                                                     model_trainer_service=Services.model_trainer_service)

    export_manager = providers.Factory(AbstractExportManager.register(ExportManager), path_service=Services.path_provider,
                                       checkpoint_export_service=Services.checkpoint_export_service,
                                       inference_model_export_service=Services.inference_model_export_service,
                                       servable_export_service=Services.servable_export_service,
                                       context_management_service=Services.context_management_service)
