from typing import Dict

from domain.models.gluon_dataset import GluonDataset
from domain.repositries.contracts.abstract_data_loader_repository import AbstractDataLoaderRepository


class DataLoaderRepository(AbstractDataLoaderRepository):
    def __init__(self):
        self.data_loader_store: Dict[str, GluonDataset] = dict()

    def store_data_loader(self, name: str, gluon_dataset: GluonDataset) -> None:
        self.data_loader_store[name] = gluon_dataset

    def retrieve_data_loader(self, name) -> GluonDataset:
        try:
            return self.data_loader_store[name]
        except KeyError as e:
            return None
