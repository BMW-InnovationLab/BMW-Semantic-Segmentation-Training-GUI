import os

from mxnet import gluon
from mxnet.gluon.data.vision import transforms

from gluoncv.data import get_segmentation_dataset
from gluoncv.data.pascal_voc.segmentation import VOCSegmentation

from domain.models.paths import Paths
from domain.models.gluon_dataset import GluonDataset
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation

from domain.services.contracts.abstract_path_service import AbstractPathService
from domain.services.contracts.abstract_dataset_augmentation_service import AbstractDatasetAugmentationService

from domain.exceptions.dataset_exceptions import DatasetAugmentingError


class DatasetAugmentationService(AbstractDatasetAugmentationService):
    def __init__(self, path_service: AbstractPathService):
        self.paths: Paths = path_service.get_paths()

    def augment_dataset(self, dataset_info: DatasetInformation, config: HyperParameterInformation) -> GluonDataset:
        try:
            batch_size: int = config.batch_size * max(len(config.gpus), 1)
            validation_batch_size: int = config.validation_batch_size * max(len(config.gpus), 1)

            input_transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize([.485, .456, .406], [.229, .224, .225]),
            ])

            VOCSegmentation.NUM_CLASS = dataset_info.num_classes

            training_set = VOCSegmentation(num_classes=dataset_info.num_classes,
                                           featurespath=os.path.join(self.paths.training_dir, "training_images"),
                                           labelspath=os.path.join(self.paths.training_dir, "training_labels"),
                                           mode='train',
                                           transform=input_transform,
                                           crop_size=config.crop_size,
                                           augment_data=config.augment_data)

            validation_set = VOCSegmentation(num_classes=dataset_info.num_classes,
                                             featurespath=os.path.join(self.paths.training_dir, 'validation_images'),
                                             labelspath=os.path.join(self.paths.training_dir, 'validation_labels'),
                                             mode='val',
                                             transform=input_transform,
                                             crop_size=config.crop_size,
                                             augment_data=config.augment_data)

            return GluonDataset(
                train_dataset=gluon.data.DataLoader(training_set, batch_size, shuffle=True, last_batch='rollover', num_workers=config.num_workers),
                validation_dataset=gluon.data.DataLoader(validation_set, validation_batch_size, last_batch='rollover', num_workers=config.num_workers))
        except Exception as e:
            raise DatasetAugmentingError(additional_message=e.__str__())
