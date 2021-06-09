from domain.exceptions.application_error import ApplicationError


class ConfigurationError(ApplicationError):
    def __init__(self, configuration_name: str, additional_message: str = ''):
        super().__init__('Could not create Configuration: ', additional_message + ' {}'.format(configuration_name))


class ConfigurationTypeNotFound(ApplicationError):
    def __init__(self, configuration_type: str, additional_message: str = ''):
        super().__init__('Configuration Type Not Found: ', additional_message + ' {}'.format(configuration_type))


class CheckpointConfigurationInvalid(ApplicationError):
    def __init__(self, configuration_path: str, additional_message: str = ''):
        super().__init__('JSON configuration is not valid: ', additional_message + ' {}'.format(configuration_path))
