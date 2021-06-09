import datetime
from gluoncv.data import VOCSegmentation
from gluoncv.model_zoo import get_model

from domain.models.paths import Paths
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_configuration_template import AbstractConfigurationTemplate

from domain.exceptions.configuration_exceptions import ConfigurationError


class PreTrainedConfiguration(AbstractConfigurationTemplate):
    def create_network_configuration(self, dataset_info: DatasetInformation, config: HyperParameterInformation, paths: Paths) -> object:
        try:
            model_zoo_name: str = "_".join([config.network, config.backbone, config.pretrained_dataset])
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Creating Configuration From PreTrained Model")
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Using The Following PreTrained Model: " + str(model_zoo_name))

            VOCSegmentation.NUM_CLASS = 21

            network = get_model(name=model_zoo_name, pretrained=True, aux=False, crop_size=config.crop_size, base_size=config.base_size, pretrained_base=False)
            if config.network == "deeplab":
                network.head.block[4].__init__(channels=dataset_info.num_classes, kernel_size=1, in_channels=256)
            else:
                network.head.block[4].__init__(channels=dataset_info.num_classes, kernel_size=1, in_channels=512)
            network.head.block[4].initialize()
            return network
        except Exception as e:
            raise ConfigurationError(configuration_name="_".join([config.network, config.backbone]), additional_message=e.__str__())
