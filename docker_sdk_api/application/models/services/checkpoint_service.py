import os
from typing import List, Dict
from domain.models.paths import Paths
from domain.exceptions.models_exception import PathNotFound
from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_checkpoint_service import AbstractCheckpointService


class CheckpointService(AbstractCheckpointService):
    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def _validate_checkpoint(self, checkpoint_path: str) -> bool:
        if not os.path.exists(checkpoint_path):
            return False
        if not os.path.exists(os.path.join(checkpoint_path, "model_best.params")):
            return False
        if not os.path.exists(os.path.join(checkpoint_path, "palette.txt")):
            return False
        if not os.path.exists(os.path.join(checkpoint_path, "configuration.json")):
            return False
        return True

    def get_checkpoints(self) -> Dict[str, str]:
        checkpoints_dict: Dict[str, str] = {}
        try:
            if os.path.isdir(self.paths.checkpoints_folder):
                for root, dirs, files in os.walk(self.paths.checkpoints_folder):
                    for directory in dirs:
                        checkpoint_path: str = os.path.join(root, directory)
                        if self._validate_checkpoint(checkpoint_path):
                            directory_tree_list: List[str] = checkpoint_path.split('/')
                            # ex: /checkpoint/resnet/demo => ["checkpoint","resnet","demo"]
                            # [-2] = "resnet" always network name not dependant on path
                            # [-1] = "demo" model name
                            checkpoints_dict[directory_tree_list[-1]] = directory_tree_list[-2]

            return checkpoints_dict
        except Exception:
            raise PathNotFound(path=self.paths.checkpoints_folder_on_host)
