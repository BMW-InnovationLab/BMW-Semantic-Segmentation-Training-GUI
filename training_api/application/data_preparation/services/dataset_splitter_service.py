import os
import random

from typing import List
from shutil import rmtree, copy2

from domain.models.paths import Paths

from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_dataset_splitter_service import AbstractDatasetSplitterService

from domain.exceptions.dataset_exceptions import TrainingTestingPathNotFound, PathNotFound


class DatasetSplitterService(AbstractDatasetSplitterService):

    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def __clean_folder_content(self, folder_dir: str) -> None:
        for folder in os.listdir(folder_dir):
            folder_path: str = os.path.join(folder_dir, folder)
            if os.path.isdir(folder_path):
                rmtree(folder_path, ignore_errors=True)

    def __shuffle_dataset(self, list_a: List[str], list_b: List[str]):
        list_a.sort()
        list_b.sort()
        images_labels_zip = list(zip(list_a, list_b))
        random.shuffle(images_labels_zip)
        list_a, list_b = zip(*images_labels_zip)
        return list(list_a), list(list_b)

    def __create_folder_structure(self) -> None:
        try:

            training_images: str = os.path.join(self.paths.training_dir, 'training_images')
            training_labels: str = os.path.join(self.paths.training_dir, 'training_labels')
            testing_images: str = os.path.join(self.paths.training_dir, 'validation_images')
            testing_labels: str = os.path.join(self.paths.training_dir, 'validation_labels')

            self.__clean_folder_content(folder_dir=self.paths.training_dir)
            self.__clean_folder_content(folder_dir=self.paths.model_dir)
            os.makedirs(training_images, exist_ok=True)
            os.makedirs(training_labels, exist_ok=True)
            os.makedirs(testing_images, exist_ok=True)
            os.makedirs(testing_labels, exist_ok=True)
        except Exception as e:
            raise TrainingTestingPathNotFound(folder_path=self.paths.training_dir, additional_message=e.__str__())

    def split_dataset(self, train_ratio: float) -> None:
        images: List[str] = os.listdir(self.paths.images_dir)
        labels: List[str] = os.listdir(self.paths.labels_dir)
        # shuffle images
        images, labels = self.__shuffle_dataset(list_a=images, list_b=labels)

        train_len: int = int(train_ratio * len(images))

        self.__create_folder_structure()

        for index, image_name in enumerate(images):
            if index <= train_len:
                dst_img: str = os.path.join(self.paths.training_dir, 'training_images')
                dst_label: str = os.path.join(self.paths.training_dir, 'training_labels')
            else:
                dst_img: str = os.path.join(self.paths.training_dir, 'validation_images')
                dst_label: str = os.path.join(self.paths.training_dir, 'validation_labels')
            try:
                copy2(os.path.join(self.paths.images_dir, image_name), dst_img)
            except Exception as e:
                PathNotFound(folder_path=os.path.join(self.paths.training_dir, 'training_images'), additional_message=e.__str__())
            try:
                copy2(os.path.join(self.paths.labels_dir, labels[index]), dst_label)
            except Exception as e:
                PathNotFound(folder_path=os.path.join(self.paths.training_dir, 'training_labels'), additional_message=e.__str__())
