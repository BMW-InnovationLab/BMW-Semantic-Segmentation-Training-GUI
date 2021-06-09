import os
from typing import Dict

from domain.exceptions.dataset_exception import ObjectClassesNotValid
from domain.models.datase_information import DatasetInformation
from domain.models.paths import Paths
from domain.services.contracts.abstract_object_classes_discovery_service import AbstractObjectClassesDiscoveryService
from domain.services.contracts.abstract_path_service import AbstractPathService
from shared.helpers.json_helper import parse_json


class ObjectClassesDiscoveryService(AbstractObjectClassesDiscoveryService):
    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def discover_object_classes(self, dataset_info: DatasetInformation) -> DatasetInformation:
        try:
            object_classes_json_path: str = os.path.join(self.paths.dataset_folder, dataset_info.dataset_name, 'objectclasses.json')
            object_classes_dict: Dict = parse_json(object_classes_json_path)
            return DatasetInformation(dataset_name=dataset_info.dataset_name, num_classes=object_classes_dict["classes"], classes=object_classes_dict["classesname"])
        except Exception as e:
            raise ObjectClassesNotValid(additional_message=e.__str__())