from typing import Dict

from domain.exceptions.models_exception import PathNotFound
from domain.models.models_info import ModelsInfo
from domain.models.paths import Paths
from domain.models.pretrained_models import PretrainedModels
from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_models_architecture_service import AbstractModelsArchitectureService
from shared.helpers.json_helper import parse_json


class ModelsArchitectureService(AbstractModelsArchitectureService):

    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def get_architectures(self) -> ModelsInfo:
        try:
            networks_dict: Dict = parse_json(self.paths.networks_path)
            return ModelsInfo.parse_obj(networks_dict)
        except Exception as e:
            raise PathNotFound(additional_message=e.__str__(), path=self.paths.networks_path)

    def get_pretrained_models(self) -> PretrainedModels:
        try:
            networks_dict: Dict = parse_json(self.paths.networks_path)
            return PretrainedModels.parse_obj(networks_dict)
        except Exception as e:
            raise PathNotFound(additional_message=e.__str__(), path=self.paths.networks_path)
