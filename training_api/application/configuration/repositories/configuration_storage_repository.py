from typing import Dict

from domain.repositries.contracts.abstract_configuration_storage_repository import AbstractConfigurationStorageRepository


class ConfigurationStorageRepository(AbstractConfigurationStorageRepository):
    def __init__(self):
        self.configuration_storage_store: Dict[str, object] = dict()

    def store_configuration(self, name: str, configuration_obj: object) -> None:
        self.configuration_storage_store[name] = configuration_obj

    def retrieve_configuration(self, name) -> object:
        try:
            return self.configuration_storage_store[name]
        except KeyError as e:
            return None
