from application.data_preparation.repositories.data_loader_repository import DataLoaderRepository

from domain.models.gluon_dataset import GluonDataset

from domain.services.contracts.abstract_data_loader_service import AbstractDataLoaderService

from domain.exceptions.dataset_exceptions import InvalidJobName


class DataLoaderService(AbstractDataLoaderService):

    def __init__(self, data_loader_repository: DataLoaderRepository):
        self.data_loader_repository = data_loader_repository

    def set_dataset(self, model_name: str, gluon_data: GluonDataset) -> None:
        self.data_loader_repository.store_data_loader(name=model_name, gluon_dataset=gluon_data)

    def get_dataset(self, model_name) -> GluonDataset:

        if self.data_loader_repository.retrieve_data_loader(name=model_name) is not None:
            return self.data_loader_repository.retrieve_data_loader(name=model_name)
        else:
            raise InvalidJobName()
