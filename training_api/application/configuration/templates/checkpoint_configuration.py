import os
import mxnet as mx
import datetime
from gluoncv.data import VOCSegmentation
from gluoncv.model_zoo.segbase import get_segmentation_model

from domain.models.paths import Paths
from domain.models.dataset_information import DatasetInformation
from domain.models.checkpoint_parameter_information import CheckpointParameterInfo
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_configuration_template import AbstractConfigurationTemplate

from domain.exceptions.configuration_exceptions import ConfigurationError, CheckpointConfigurationInvalid

from shared.helpers.json_helper import parse_json


class CheckpointConfiguration(AbstractConfigurationTemplate):
    def create_network_configuration(self, dataset_info: DatasetInformation, config: HyperParameterInformation, paths: Paths) -> object:
        try:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Creating Configuration From Checkpoint")
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Using The Following Checkpoint: " + str(config.base_model_name)
                  + " With The Following Model: " + str(config.base_weight_name))

            VOCSegmentation.NUM_CLASS = dataset_info.num_classes

            local_weight_path: str = os.path.join(paths.checkpoints_dir, config.base_weight_name,
                                                  config.base_model_name)
            local_weight_configuration_path: str = os.path.join(local_weight_path, 'configuration.json')

            try:
                local_weight_configuration: CheckpointParameterInfo = CheckpointParameterInfo.parse_obj(parse_json(file_path=local_weight_configuration_path))
            except Exception as e:
                raise CheckpointConfigurationInvalid(configuration_path=local_weight_configuration_path, additional_message=e.__str__())

            network = get_segmentation_model(model=local_weight_configuration.network, dataset='pascal_voc', backbone=local_weight_configuration.backbone,
                                             norm_layer=mx.gluon.nn.BatchNorm, norm_kwargs={}, aux=False, crop_size=config.crop_size,
                                             base_size=config.base_size,
                                             pretrained_base=False, pretrained=False)

            network.initialize()
            network.load_parameters(filename=os.path.join(local_weight_path, 'model_best.params'), ignore_extra=True)
            return network
        except CheckpointConfigurationInvalid as  e:
            raise e
        except Exception as e:
            raise ConfigurationError(configuration_name="", additional_message=e.__str__())
