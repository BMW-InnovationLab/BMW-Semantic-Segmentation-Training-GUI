import os

import mxnet as mx
import datetime
from gluoncv.data import VOCSegmentation
from gluoncv.model_zoo.segbase import get_segmentation_model

from domain.models.paths import Paths
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.models.checkpoint_parameter_information import CheckpointParameterInfo

from domain.services.contracts.abstract_configuration_template import AbstractConfigurationTemplate

from domain.exceptions.configuration_exceptions import ConfigurationError, CheckpointConfigurationInvalid

from shared.helpers.json_helper import parse_json


class LocalWeightsConfiguration(AbstractConfigurationTemplate):
    def create_network_configuration(self, dataset_info: DatasetInformation, config: HyperParameterInformation, paths: Paths) -> object:
        try:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Transfer Learning From Local Weights")

            local_weight_path: str = os.path.join(paths.checkpoints_dir, config.base_weight_name,
                                                  config.base_model_name)
            local_weight_configuration_path: str = os.path.join(local_weight_path, 'configuration.json')
            try:
                local_weight_configuration: CheckpointParameterInfo = CheckpointParameterInfo.parse_obj(parse_json(file_path=local_weight_configuration_path))
            except Exception as e:
                raise CheckpointConfigurationInvalid(configuration_path=local_weight_configuration_path, additional_message=e.__str__())

            VOCSegmentation.NUM_CLASS = local_weight_configuration.num_classes
            network = get_segmentation_model(model=local_weight_configuration.network, dataset='pascal_voc', backbone=local_weight_configuration.backbone,
                                             norm_layer=mx.gluon.nn.BatchNorm, norm_kwargs={}, aux=False, crop_size=config.crop_size,
                                             base_size=config.base_size,
                                             pretrained_base=False, pretrained=False)
            network.initialize()
            network.load_parameters(filename=os.path.join(local_weight_path, 'model_best.params'), ignore_extra=True)
            with network.name_scope():
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Using The Following Network: " + str(local_weight_configuration.network))
                if local_weight_configuration.network == "deeplab":
                    network.head.block[4].__init__(channels=dataset_info.num_classes, kernel_size=1, in_channels=256)
                elif local_weight_configuration.network in ["fcn", "psp"]:
                    network.head.block[4].__init__(channels=dataset_info.num_classes, kernel_size=1, in_channels=512)
                network.head.block[4].initialize()
            return network
        except CheckpointConfigurationInvalid as  e:
            raise e
        except Exception as e:
            raise ConfigurationError(configuration_name="", additional_message=e.__str__())
