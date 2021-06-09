import os

from shutil import rmtree
from distutils.dir_util import copy_tree

from domain.models.paths import Paths
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.services.contracts.abstract_inference_model_export_service import AbstractInferenceModelExportService
from domain.services.contracts.abstract_path_service import AbstractPathService

from domain.exceptions.dataset_exceptions import PathNotFound


class InferenceModelExportService(AbstractInferenceModelExportService):
    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def create_inference_model(self, config: HyperParameterInformation) -> None:
        inference_model_path: str = os.path.join(self.paths.inference_model_dir, config.model_name)
        try:
            if os.path.exists(inference_model_path) and os.path.isdir(inference_model_path):
                rmtree(inference_model_path)
            os.makedirs(inference_model_path)

            copy_tree(self.paths.model_dir, inference_model_path)
        except Exception as e:
            raise PathNotFound(folder_path=inference_model_path, additional_message=e.__str__())
