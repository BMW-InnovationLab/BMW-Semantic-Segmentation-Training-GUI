import os
from typing import List

from application.dataset.models.image_extension import ImageExtension
from domain.exceptions.dataset_exception import DatasetNotValid
from domain.models.datase_information import DatasetInformation
from domain.models.paths import Paths
from domain.services.contracts.abstract_dataset_validator_service import AbstractDatasetValidatorService
from domain.services.contracts.abstract_path_service import AbstractPathService


class DatasetValidatorService(AbstractDatasetValidatorService):
    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def _validate_image_format(self, image_dir: str) -> bool:
        images: List[str] = os.listdir(image_dir)

        # list images and compare them with supported types
        for image in images:
            if image.lower().split('.')[1] not in list(ImageExtension.__members__):
                return False
        return True

    def _validate_folder_structure(self, dataset_path: str) -> bool:
        images_path: str = os.path.join(dataset_path, 'images')
        labels_path: str = os.path.join(dataset_path, 'labels')
        object_classes: str = os.path.join(dataset_path, 'objectclasses.json')

        if os.path.isdir(images_path) and os.path.isdir(labels_path) and os.path.isfile(object_classes):
            return True
        return False

    # todo raise exception with image name and specific error
    def validate_dataset(self, dataset_info: DatasetInformation) -> None:
        dataset_folder: str = os.path.join(self.paths.dataset_folder, dataset_info.dataset_name)
        images_path: str = os.path.join(dataset_folder, 'images')
        labels_path: str = os.path.join(dataset_folder, 'labels')

        if self._validate_folder_structure(dataset_path=dataset_folder):
            if self._validate_image_format(images_path) and self._validate_image_format(labels_path):
                return
            raise DatasetNotValid(dataset_name=dataset_info.dataset_name, additional_message="Image format in dataset not supported")
        raise DatasetNotValid(dataset_name=dataset_info.dataset_name, additional_message="folder structure not valid")
