import os
from shutil import rmtree
from distutils.dir_util import copy_tree
from gluoncv.utils.viz.segmentation import _getvocpallete

from domain.models.paths import Paths
from domain.models.dataset_information import DatasetInformation
from domain.models.checkpoint_parameter_information import CheckpointParameterInfo
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_checkpoint_export_service import AbstractCheckpointExportService

from domain.exceptions.dataset_exceptions import PathNotFound

from shared.helpers.json_helper import write_json_dict


class CheckpointExportService(AbstractCheckpointExportService):

    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def __create_palette(self, num_classes: int, checkpoint_model_path: str) -> None:
        # todo check  _getvocpalette  num_classes or 256
        palette = _getvocpallete(num_cls=num_classes)
        palette_path: str = os.path.join(checkpoint_model_path, 'palette.txt')
        with open(palette_path, 'w') as palette_writer:
            for i in palette:
                palette_writer.write('%s\n' % i)
            palette_writer.close()

    def __create_json_configuration(self, dataset_info: DatasetInformation, config: HyperParameterInformation, checkpoint_model_path: str) -> None:
        configuration_path: str = os.path.join(checkpoint_model_path, 'configuration.json')
        configuration_info: CheckpointParameterInfo = CheckpointParameterInfo(lr=config.lr, momentum=config.momentum, weight_decay=config.weight_decay,
                                                                              num_workers=config.num_workers,
                                                                              batch_size=config.batch_size,
                                                                              epochs=config.epochs,
                                                                              backbone=config.backbone,
                                                                              network=config.network,
                                                                              checkpoint_name=config.model_name,
                                                                              num_classes=dataset_info.num_classes,
                                                                              classes_names=dataset_info.classes,
                                                                              inference_engine_name="gluonsegmentation",
                                                                              type="semantic")

        write_json_dict(file_path=configuration_path, json_dict=configuration_info.dict())

    def create_checkpoint(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> None:
        network_folder: str = os.path.join(self.paths.checkpoints_dir, "_".join([config.network, config.backbone]))
        checkpoint_path: str = os.path.join(network_folder, config.model_name)

        try:
            if not os.path.exists(network_folder) and not os.path.isdir(network_folder):
                os.makedirs(network_folder)

            if os.path.exists(checkpoint_path) and os.path.isdir(checkpoint_path):
                rmtree(checkpoint_path)

            os.makedirs(checkpoint_path)
            self.__create_palette(num_classes=dataset_info.num_classes, checkpoint_model_path=self.paths.model_dir)
            self.__create_json_configuration(dataset_info=dataset_info, config=config, checkpoint_model_path=self.paths.model_dir)

            copy_tree(self.paths.model_dir, checkpoint_path)
        except Exception as e:
            raise PathNotFound(folder_path=checkpoint_path, additional_message=e.__str__())
