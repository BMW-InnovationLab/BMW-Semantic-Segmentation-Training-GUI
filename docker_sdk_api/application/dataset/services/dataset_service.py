import os
from typing import List

from domain.exceptions.dataset_exception import DatasetPathNotFound
from domain.models.paths import Paths
from domain.services.contracts.abstract_dataset_service import AbstractDatasetService
from domain.services.contracts.abstract_path_service import AbstractPathService


class DatasetService(AbstractDatasetService):
    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def get_datasets(self) -> List[str]:
        try:
            return os.listdir(self.paths.dataset_folder)
        except Exception as e:
            raise DatasetPathNotFound(additional_message=e.__str__())
