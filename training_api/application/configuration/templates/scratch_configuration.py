import datetime
import mxnet as mx

from gluoncv.data import VOCSegmentation
from gluoncv.model_zoo.segbase import get_segmentation_model

from domain.models.paths import Paths
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_configuration_template import AbstractConfigurationTemplate

from domain.exceptions.configuration_exceptions import ConfigurationError


class ScratchConfiguration(AbstractConfigurationTemplate):
    def create_network_configuration(self, dataset_info: DatasetInformation, config: HyperParameterInformation, paths: Paths) -> object:

        try:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Creating From Scratch Configuration")
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Using The Following Backbone: " + str(config.backbone))
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Using The Following Network: " + str(config.network))

            VOCSegmentation.NUM_CLASS = dataset_info.num_classes
            return get_segmentation_model(model=config.network, backbone=config.backbone, dataset='pascal_voc', norm_layer=mx.gluon.nn.BatchNorm,
                                          crop_size=config.crop_size,
                                          pretrained_base=True, pretrained=False, base_size=config.base_size, aux=False)
        except Exception as e:
            raise ConfigurationError(configuration_name="_".join([config.network, config.backbone]), additional_message=e.__str__())
