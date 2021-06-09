import datetime

from domain.models.gluon_dataset import GluonDataset
from domain.models.gluon_training_parameter import GluonTrainingParameter
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_model_trainer_setup import AbstractModelTrainerSetup
from domain.services.contracts.abstract_data_loader_service import AbstractDataLoaderService
from domain.services.contracts.abstract_model_trainer_service import AbstractModelTrainerService
from domain.services.contracts.abstract_model_train_evaluate_manager import AbstractModelTrainEvaluateManager
from domain.services.contracts.abstract_configuration_storage_service import AbstractConfigurationStorageService

from domain.exceptions.application_error import ApplicationError


class ModelTrainEvaluateManager(AbstractModelTrainEvaluateManager):
    def __init__(self, data_loader_service: AbstractDataLoaderService,
                 configuration_storage_service: AbstractConfigurationStorageService, model_trainer_setup: AbstractModelTrainerSetup,
                 model_trainer_service: AbstractModelTrainerService):
        self.data_loader_service = data_loader_service
        self.configuration_storage_service = configuration_storage_service
        self.model_trainer_setup = model_trainer_setup
        self.model_trainer_service = model_trainer_service

    def __get_dataset(self, model_name: str) -> GluonDataset:
        return self.data_loader_service.get_dataset(model_name=model_name)

    def __get_configuration(self, model_name: str) -> object:
        return self.configuration_storage_service.get_configuration(model_name=model_name)

    def train_eval_continuously(self, config: HyperParameterInformation) -> None:
        try:
            gluon_dataset: GluonDataset = self.__get_dataset(model_name=config.model_name)
            gluon_network: object = self.__get_configuration(model_name=config.model_name)
            gluon_training_params: GluonTrainingParameter = self.model_trainer_setup.setup_training(gluon_dataset=gluon_dataset, config=config,
                                                                                                    gluon_network=gluon_network)
            self.model_trainer_service.training_loop(config=config, gluon_dataset=gluon_dataset, gluon_training_params=gluon_training_params)
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")+"Training Done!")
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")+"Proceeding To Export Model")
        except ApplicationError as e:
            raise e
