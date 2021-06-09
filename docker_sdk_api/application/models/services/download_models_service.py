import os
from typing import Dict

from domain.models.paths import Paths

from domain.exceptions.models_exception import PathNotFound

from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_download_models_service import AbstractDownloadModelsService

from shared.helpers.get_model_zip import get_downloadable_zip


class DownloadModelsService(AbstractDownloadModelsService):

    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def get_downloadable_models(self) -> Dict[str, str]:
        if not os.path.isdir(self.paths.servable_folder):
            os.makedirs(self.paths.servable_folder)
        try:
            response: Dict[str, str] = get_downloadable_zip(folder_path=self.paths.servable_folder)
            return response
        except Exception:
            raise PathNotFound(path=self.paths.servable_folder_on_host)
