import os
from typing import List, Dict

from application.models.models.supported_classifiers import SupportedClassifiers
from domain.models.paths import Paths
from domain.services.contracts.abstract_classifier_service import AbstractClassifierService
from domain.services.contracts.abstract_path_service import AbstractPathService

from domain.exceptions.models_exception import PathNotFound
from shared.helpers.json_helper import parse_json


class ClassifierService(AbstractClassifierService):

    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def _get_classifier_backbone(self, config_path: str):
        config_dict: Dict = parse_json(config_path)
        if "network" in config_dict.keys():
            if SupportedClassifiers.has_value(config_dict["network"]):
                return SupportedClassifiers(config_dict["network"]).name
        else:
            return None

    def _validate_classifier(self, classifier_path: str) -> bool:
        if not os.path.exists(classifier_path) or not os.path.isdir(classifier_path):
            return False
        if not os.path.exists(os.path.join(classifier_path, "model_best.params")) and not os.path.isfile(os.path.join(classifier_path, "model_best.params")):
            return False
        if not os.path.exists(os.path.join(classifier_path, "classes.txt")) and not os.path.isfile(os.path.join(classifier_path, "classes.txt")):
            return False
        if not os.path.exists(os.path.join(classifier_path, "config.json")) and not os.path.isfile(os.path.join(classifier_path, "config.json")):
            return False
        return True

    def get_classifiers(self) -> Dict[str, str]:
        available_classifier: Dict[str, str] = {}
        try:
            for classifier in os.listdir(self.paths.classifier_folder):
                if self._validate_classifier(classifier_path=os.path.join(self.paths.classifier_folder, classifier)):
                    classifier_backbone: str = self._get_classifier_backbone(config_path=os.path.join(self.paths.classifier_folder, classifier, "config.json"))
                    if classifier_backbone is not None:
                        available_classifier[classifier] = classifier_backbone
            return available_classifier
        except Exception as e:
            raise PathNotFound(path=self.paths.classifier_folder_on_host)
