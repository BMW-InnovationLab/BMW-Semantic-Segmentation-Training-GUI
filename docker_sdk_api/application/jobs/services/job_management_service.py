import os
import time
from typing import Dict, List

from domain.services.contracts.abstract_path_service import AbstractPathService
from shared.helpers.alias_provider_sql import add_alias, delete_alias, get_name_from_alias
from domain.models.container_settings import ContainerSettings
from domain.services.contracts.abstract_job_management_service import AbstractJobManagementService
from domain.models.container_info import ContainerInfo
from shared.helpers.slugified_name_creator import create_slugified_name
from application.docker.services.DockerClientService import DockerClientService
from domain.models.paths import Paths
from domain.exceptions.job_exception import ContainerNotFound
from domain.exceptions.job_exception import JobNotStarted


# noinspection PyCompatibility
class JobManagementService(AbstractJobManagementService):
    def __init__(self, path_service: AbstractPathService, docker_client: DockerClientService):
        self.paths: Paths = path_service.get_paths()
        self.client: DockerClientService = docker_client.client

    def _struct_volumes(self, container_settings: ContainerSettings) -> Dict[str, Dict[str, str]]:
        dataset_path: str = os.path.join(self.paths.dataset_folder_on_host, container_settings.dataset_name)

        volumes: Dict[str, Dict[str, str]] = {
            dataset_path: {'bind': '/dataset', 'mode': 'rw'},
            self.paths.api_folder: {'bind': '/training_api', 'mode': 'rw'},
            self.paths.checkpoints_folder_on_host: {'bind': '/checkpoints', 'mode': 'rw'},
            self.paths.inference_api_models_folder: {'bind': '/inference_api/models', 'mode': 'rw'},
            self.paths.classifier_folder_on_host: {'bind': '/classifiers', 'mode': 'rw'}
        }
        return volumes

    def _struct_ports(self, container_settings: ContainerSettings) -> Dict[str, str]:
        ports: Dict[str, str] = {'5253/tcp': str(container_settings.api_port)}
        return ports

    def _run_command_cpu(self, ports: Dict[str, str], volumes: Dict):
        return self.client.containers.run(self.paths.image_name, remove=True,
                                          ports=ports, volumes=volumes, tty=True,
                                          stdin_open=True, detach=True)

    def _run_command_gpu(self, ports: Dict[str, str], volumes: Dict):
        return self.client.containers.run(self.paths.image_name, remove=True,
                                          runtime='nvidia',
                                          ports=ports, volumes=volumes, tty=True,
                                          stdin_open=True, detach=True)

    def start_container(self, container_settings: ContainerSettings) -> None:

        volumes: Dict[str, Dict[str, str]] = self._struct_volumes(container_settings=container_settings)
        ports: Dict[str, str] = self._struct_ports(container_settings=container_settings)

        string_gpus: List[str] = [str(gpu) for gpu in container_settings.gpus]
        slugified_name: str = create_slugified_name(container_settings.name)

        training_image_architecture: str = self.paths.image_name.split('_')[-1].lower()
        try:

            # in case of CPU docker image
            if string_gpus[0] == "-1" and training_image_architecture == 'cpu':
                container_name: str = "semantic_segmentation_CPU_" + slugified_name
                container = self._run_command_cpu(ports=ports, volumes=volumes)

            # in case of GPU docker image but with CPU training
            elif string_gpus[0] == "-1" and training_image_architecture == 'gpu':
                container_name: str = "semantic_segmentation_CPU_" + slugified_name
                container = self._run_command_gpu(ports=ports, volumes=volumes)

            # in case of GPU image and GPU training
            else:
                container_name: str = "semantic_segmentation_GPU_" + str("_".join(string_gpus)) + "_" + slugified_name
                container = self._run_command_gpu(ports=ports, volumes=volumes)
            #
            #
            # if gpus_string is not None:
            #     container = self._run_command_gpu(ports=ports, volumes=volumes, gpus_string=gpus_string)
            #
            # else:
            #     container = self._run_command_cpu(ports=ports, volumes=volumes)
            container.rename(container_name)
            add_alias(container_name, container_settings.name)
            time.sleep(7)
        except Exception as e:
            raise JobNotStarted(additional_message=e.__str__())

    def stop_container(self, container_info: ContainerInfo) -> None:

        for container in self.client.containers.list():
            if container.name == get_name_from_alias(container_info.name):
                container.kill()
                delete_alias(container_info.name)
                return
        raise ContainerNotFound(additional_message="Job Not Killed ", container_name=container_info.name)
