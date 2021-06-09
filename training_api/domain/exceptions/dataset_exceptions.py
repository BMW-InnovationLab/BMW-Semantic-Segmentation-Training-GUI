from domain.exceptions.application_error import ApplicationError


class TrainingTestingPathNotFound(ApplicationError):
    def __init__(self, folder_path: str, additional_message: str = ''):
        super().__init__('Could not create Folder for training/testing data: ', additional_message + ' {}'.format(folder_path))


class PathNotFound(ApplicationError):
    def __init__(self, folder_path: str, additional_message: str = ''):
        super().__init__('Path Not Found: ', additional_message + ' {}'.format(folder_path))


class DatasetAugmentingError(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__('Error While Augmenting Dataset: ', additional_message)


class InvalidJobName(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__('Invalid Job Name for Gluon Dataloader No Dataset Where Found ', additional_message)
