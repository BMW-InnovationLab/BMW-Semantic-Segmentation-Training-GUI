from domain.exceptions.application_error import ApplicationError


class DatasetNotValid(ApplicationError):
    """Raised when the dataset structure or image format is not valid """
    def __init__(self, additional_message: str = '', dataset_name: str = ''):
        super().__init__('Dataset Not Valid ', additional_message + ' {}'.format(dataset_name))


class DatasetPathNotFound(ApplicationError):
    """Raised when the dataset path not found """

    def __init__(self, additional_message: str = ''):
        super().__init__('Dataset Path Not Found ', additional_message)


class ObjectClassesNotValid(ApplicationError):
    """Raised when the dataset path not found """

    def __init__(self, additional_message: str = ''):
        super().__init__('objectclasses.json is not valid ', additional_message)
