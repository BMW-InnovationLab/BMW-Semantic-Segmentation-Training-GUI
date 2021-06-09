import datetime
from textwrap import indent

from domain.exceptions.application_error import ApplicationError
from domain.models.gluon_dataset import GluonDataset
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_data_loader_service import AbstractDataLoaderService
from domain.services.contracts.abstract_dataset_augmentation_service import AbstractDatasetAugmentationService
from domain.services.contracts.abstract_dataset_preparation_service import AbstractDatasetPreparationManager
from domain.services.contracts.abstract_dataset_splitter_service import AbstractDatasetSplitterService


class DatasetPreparationManager(AbstractDatasetPreparationManager):

    def __init__(self, dataset_augmentation_service: AbstractDatasetAugmentationService, dataset_splitter_service: AbstractDatasetSplitterService,
                 data_loader_service: AbstractDataLoaderService):
        self.dataset_augmentation_service = dataset_augmentation_service
        self.dataset_splitter_service = dataset_splitter_service
        self.data_loader_service = data_loader_service

    def prepare_dataset(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> None:
        try:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Processing Dataset With The Following Parameters:")
            print(dataset_info.json(indent=4))

            self.dataset_splitter_service.split_dataset(train_ratio=dataset_info.train_ratio)
            gluon_data: GluonDataset = self.dataset_augmentation_service.augment_dataset(dataset_info=dataset_info, config=config)
            self.data_loader_service.set_dataset(model_name=config.model_name, gluon_data=gluon_data)
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + "Dataset Preparation Successful Proceeding")
        except ApplicationError as e:
            raise e
