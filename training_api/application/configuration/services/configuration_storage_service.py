from domain.exceptions.dataset_exceptions import InvalidJobName

from domain.services.contracts.abstract_configuration_storage_service import AbstractConfigurationStorageService
from domain.repositries.contracts.abstract_configuration_storage_repository import AbstractConfigurationStorageRepository


class ConfigurationStorageService(AbstractConfigurationStorageService):

    def __init__(self, configuration_storage_repository: AbstractConfigurationStorageRepository):
        self.configuration_repository = configuration_storage_repository

    def set_configuration(self, model_name: str, configuration_obj: object) -> None:
        self.configuration_repository.store_configuration(name=model_name, configuration_obj=configuration_obj)

    def get_configuration(self, model_name: str) -> object:

        if self.configuration_repository.retrieve_configuration(name=model_name) is not None:
            return self.configuration_repository.retrieve_configuration(name=model_name)
        else:
            raise InvalidJobName()
