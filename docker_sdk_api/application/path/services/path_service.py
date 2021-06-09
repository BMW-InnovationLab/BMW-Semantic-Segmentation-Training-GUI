import os
from typing import Dict

from domain.models.paths import Paths
from domain.services.contracts.abstract_path_service import AbstractPathService
from shared.helpers.json_helper import parse_json


class PathService(AbstractPathService):

    def __init__(self):
        json_path: str = "./assets/paths.json"
        path_obj: Dict[str, str] = parse_json(json_path)

        path_obj["api_folder"]: str = os.path.join(path_obj["base_dir"], path_obj["api_folder"])
        path_obj["dataset_folder_on_host"]: str = os.path.join(path_obj["base_dir"], path_obj["dataset_folder_on_host"])
        path_obj["checkpoints_folder_on_host"]: str = os.path.join(path_obj["base_dir"], path_obj["checkpoints_folder_on_host"])
        path_obj["inference_api_models_folder"]: str = os.path.join(path_obj["base_dir"], path_obj["inference_api_models_folder"])
        path_obj["servable_folder_on_host"]: str = os.path.join(path_obj["base_dir"], path_obj["servable_folder_on_host"])
        path_obj["classifier_folder_on_host"]: str = os.path.join(path_obj["base_dir"], path_obj["classifier_folder_on_host"])

        self.paths: Paths = Paths.parse_obj(path_obj)

    def get_paths(self) -> Paths:
        return self.paths
