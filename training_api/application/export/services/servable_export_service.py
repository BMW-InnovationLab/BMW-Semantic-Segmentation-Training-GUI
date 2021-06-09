import os
from shutil import make_archive

from domain.models.paths import Paths
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_servable_export_service import AbstractServableExportService

from domain.exceptions.dataset_exceptions import PathNotFound


class ServableExportService(AbstractServableExportService):
    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def create_servable_model(self, config: HyperParameterInformation) -> None:
        zip_dir: str = os.path.join(self.paths.servable_dir, "_".join([config.network, config.backbone]))
        zip_file: str = os.path.join(zip_dir, config.model_name)

        if not os.path.exists(zip_dir) and not os.path.isdir(zip_dir):
            os.makedirs(zip_dir, exist_ok=True)

        try:
            make_archive(zip_file, 'zip', self.paths.model_dir)
        except Exception as e:
            raise PathNotFound(folder_path=zip_file, additional_message=e.__str__(), )
