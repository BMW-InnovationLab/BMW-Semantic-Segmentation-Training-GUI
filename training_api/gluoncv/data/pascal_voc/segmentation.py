"""Pascal VOC Semantic Segmentation Dataset."""
import os
import numpy as np
from PIL import Image
from mxnet import cpu
import mxnet.ndarray as F
from ..segbase import SegmentationDataset


class VOCSegmentation(SegmentationDataset):
    """Pascal VOC Semantic Segmentation Dataset.

    Parameters
    ----------
    root : string
        Path to VOCdevkit folder. Default is '$(HOME)/mxnet/datasets/voc'
    split: string
        'train', 'val' or 'test'
    transform : callable, optional
        A function that transforms the image

    Examples
    --------
    >>> from mxnet.gluon.data.vision import transforms
    >>> # Transforms for Normalization
    >>> input_transform = transforms.Compose([
    >>>     transforms.ToTensor(),
    >>>     transforms.Normalize([.485, .456, .406], [.229, .224, .225]),
    >>> ])
    >>> # Create Dataset
    >>> trainset = gluoncv.data.VOCSegmentation(split='train', transform=input_transform)
    >>> # Create Training Loader
    >>> train_data = gluon.data.DataLoader(
    >>>     trainset, 4, shuffle=True, last_batch='rollover',
    >>>     num_workers=4)
    """
    BASE_DIR = 'VOC2012'
    NUM_CLASS = 0

    def __init__(self, num_classes=0, featurespath=None, labelspath=None, root=os.path.expanduser('~/.mxnet/datasets/voc'),
                 split='train', mode=None, transform=None, augment_data=True, **kwargs):
        super(VOCSegmentation, self).__init__(root, split, mode, transform, **kwargs)
        # _voc_root = os.path.join(root, self.BASE_DIR)
        # _mask_dir = os.path.join(_voc_root, 'SegmentationClass')
        # _image_dir = os.path.join(_voc_root, 'JPEGImages')
        # # train/val/test splits are pre-cut
        # _splits_dir = os.path.join(_voc_root, 'ImageSets/Segmentation')
        # if split == 'train':
        #     _split_f = os.path.join(_splits_dir, 'trainval.txt')
        # elif split == 'val':
        #     _split_f = os.path.join(_splits_dir, 'val.txt')
        # elif split == 'test':
        #     _split_f = os.path.join(_splits_dir, 'test.txt')
        # else:
        #     raise RuntimeError('Unknown dataset split.')
        #
        # self.images = []
        # self.masks = []
        # with open(os.path.join(_split_f), "r") as lines:
        #     for line in lines:
        #         _image = os.path.join(_image_dir, line.rstrip('\n') + ".jpg")
        #         assert os.path.isfile(_image)
        #         self.images.append(_image)
        #         if split != 'test':
        #             _mask = os.path.join(_mask_dir, line.rstrip('\n') + ".png")
        #             assert os.path.isfile(_mask)
        #             self.masks.append(_mask)
        #
        # if split != 'test':
        #     assert (len(self.images) == len(self.masks))

        """modified block to enable data augmenting"""
        self.augment_data = augment_data
        entries = os.listdir(featurespath)
        entries = sorted(entries)
        self.images = []
        VOCSegmentation.NUM_CLASS = num_classes
        for entry in entries:
            self.images.append(featurespath + '/' + entry)

        entries = os.listdir(labelspath)
        entries = sorted(entries)
        self.masks = []
        for entry in entries:
            self.masks.append(labelspath + '/' + entry)

    def __getitem__(self, index):
        img = Image.open(self.images[index]).convert('RGB')
        if self.mode == 'test':
            img = self._img_transform(img)
            if self.transform is not None:
                img = self.transform(img)
            return img, os.path.basename(self.images[index])
        mask = Image.open(self.masks[index])
        # synchronized transform
        if self.mode == 'train':
            """modified block to enable data augmenting"""
            img, mask = self._sync_transform(img, mask, augment_data=self.augment_data)
        elif self.mode == 'val':
            img, mask = self._val_sync_transform(img, mask)
        else:
            assert self.mode == 'testval'
            img, mask = self._img_transform(img), self._mask_transform(mask)
        # general resize, normalize and toTensor
        if self.transform is not None:
            img = self.transform(img)

        return img, mask

    def __len__(self):
        return len(self.images)

    def _mask_transform(self, mask):
        target = np.array(mask).astype('int32')
        return F.array(target, cpu(0))

    @property
    def classes(self):
        """Category names."""
        return type(self).CLASSES
