import os
import mxnet as mx
import datetime
from gluoncv.data import VOCSegmentation
from gluoncv.model_zoo.segbase import get_segmentation_model

from domain.models.paths import Paths
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_configuration_template import AbstractConfigurationTemplate

from domain.exceptions.configuration_exceptions import ConfigurationError

from shared.helpers.classes_helper import get_num_classes


class LocalClassifierConfiguration(AbstractConfigurationTemplate):

    def create_network_configuration(self, dataset_info: DatasetInformation, config: HyperParameterInformation, paths: Paths) -> object:
        try:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Using Local Classifier Backbone Configuration")
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Using The Following Network: "+str(config.network))

            VOCSegmentation.NUM_CLASS = dataset_info.num_classes

            num_classes: int = get_num_classes(classes_path=os.path.join(paths.classifier_dir,  config.base_model_name, 'classes.txt'))
            network = get_segmentation_model(model=config.network, dataset='pascal_voc', backbone=config.backbone,
                                             norm_layer=mx.gluon.nn.BatchNorm, norm_kwargs={}, aux=False, base_size=config.base_size,
                                             crop_size=config.crop_size, pretrained=False, pretrained_base=True, classes=num_classes,
                                             pretrained_base_name=os.path.join(paths.classifier_dir, config.base_model_name,
                                                                               'model_best.params'))
            network.initialize()
            return network
        except Exception as e:
            raise ConfigurationError(
                configuration_name=os.path.join(paths.classifier_dir,  config.base_model_name, 'model_best.params'),
                additional_message=e.__str__())
