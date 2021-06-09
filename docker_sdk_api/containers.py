from dependency_injector import containers, providers

from application.dataset.services.dataset_service import DatasetService
from application.dataset.services.dataset_validator_service import DatasetValidatorService
from application.dataset.services.object_classes_discovery_service import ObjectClassesDiscoveryService
from application.docker.services.DockerClientService import DockerClientService
from application.infrastructure.services.gpu_service import GpuService
from application.infrastructure.services.port_scanner_service import PortScannerService
from application.jobs.services.job_management_service import JobManagementService
from application.jobs.services.job_utility_service import JobUtilityService
from application.path.services.path_service import PathService
from application.models.services.checkpoint_service import CheckpointService
from application.models.services.download_models_service import DownloadModelsService
from application.models.services.models_architecture_service import ModelsArchitectureService
from application.models.services.classifier_service import ClassifierService
from domain.services.contracts.abstract_classifier_service import AbstractClassifierService
from domain.services.contracts.abstract_checkpoint_service import AbstractCheckpointService
from domain.services.contracts.abstract_dataset_service import AbstractDatasetService
from domain.services.contracts.abstract_dataset_validator_service import AbstractDatasetValidatorService
from domain.services.contracts.abstract_download_models_service import AbstractDownloadModelsService
from domain.services.contracts.abstract_gpu_service import AbstractGpuService
from domain.services.contracts.abstract_job_management_service import AbstractJobManagementService
from domain.services.contracts.abstract_job_utility_service import AbstractJobUtilityService
from domain.services.contracts.abstract_models_architecture_service import AbstractModelsArchitectureService
from domain.services.contracts.abstract_object_classes_discovery_service import AbstractObjectClassesDiscoveryService
from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_port_scanner_service import AbstractPortScannerService


class Services(containers.DeclarativeContainer):
    path_provider = providers.Singleton(AbstractPathService.register(PathService))
    docker_client = providers.Singleton(DockerClientService)

    # dataset
    dataset_service = providers.Factory(AbstractDatasetService.register(DatasetService), path_service=path_provider)
    dataset_validator_service = providers.Factory(AbstractDatasetValidatorService.register(DatasetValidatorService), path_service=path_provider)
    object_classes_discovery_service = providers.Factory(AbstractObjectClassesDiscoveryService.register(ObjectClassesDiscoveryService), path_service=path_provider)

    # infrastructure
    gpu_service = providers.Factory(AbstractGpuService.register(GpuService))
    port_scanner_service = providers.Factory(AbstractPortScannerService.register(PortScannerService))

    # jobs
    job_utility_service = providers.Factory(AbstractJobUtilityService.register(JobUtilityService), path_service=path_provider, docker_client=docker_client)
    job_management_service = providers.Factory(AbstractJobManagementService.register(JobManagementService), path_service=path_provider, docker_client=docker_client)

    # models
    checkpoint_service = providers.Factory(AbstractCheckpointService.register(CheckpointService), path_service=path_provider)
    classifier_service = providers.Factory(AbstractClassifierService.register(ClassifierService), path_service=path_provider)
    download_models_service = providers.Factory(AbstractDownloadModelsService.register(DownloadModelsService), path_service=path_provider)
    models_architecture_service = providers.Factory(AbstractModelsArchitectureService.register(ModelsArchitectureService), path_service=path_provider)
