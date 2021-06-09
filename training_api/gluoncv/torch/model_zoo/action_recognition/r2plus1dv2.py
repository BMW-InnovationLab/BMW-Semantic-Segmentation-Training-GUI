# pylint: disable=missing-function-docstring, missing-class-docstring
"""
A Closer Look at Spatiotemporal Convolutions for Action Recognition
CVPR 2018, https://arxiv.org/abs/1711.11248
Large-scale weakly-supervised pre-training for video action recognition
CVPR 2019, https://arxiv.org/abs/1905.00561
"""
import torch
import torch.nn as nn


__all__ = ['ResNet_R2plus1Dv2', 'r2plus1d_v2_resnet152_kinetics400']


eps = 1e-3
bn_mmt = 0.1


class Affine(nn.Module):
    def __init__(self, feature_in):
        super(Affine, self).__init__()
        self.weight = nn.Parameter(torch.randn(feature_in, 1, 1, 1))
        self.bias = nn.Parameter(torch.randn(feature_in, 1, 1, 1))
        self.weight.requires_grad = True
        self.bias.requires_grad = True

    def forward(self, x):
        x = x * self.weight + self.bias
        return x


class Bottleneck_R2plus1Dv2(nn.Module):
    def __init__(self, in_planes, planes, middle_planes, stride=1, temporal_stride=1,
                 down_sample=None, expansion=2, temporal_kernel=3, use_affine=True):
        super(Bottleneck_R2plus1Dv2, self).__init__()
        self.expansion = expansion
        self.conv1 = nn.Conv3d(in_planes, planes, kernel_size=(1, 1, 1),
                               bias=False, stride=(1, 1, 1))

        if use_affine:
            self.bn1 = Affine(planes)
        else:
            self.bn1 = nn.BatchNorm3d(planes, track_running_stats=True,
                                      eps=eps, momentum=bn_mmt)

        self.conv2_middle = nn.Conv3d(
            planes,
            middle_planes,
            kernel_size=(1, 3, 3),
            stride=(1, stride, stride),
            padding=(0, 1, 1),
            groups=1,
            bias=False)
        if use_affine:
            self.bn2_middle = Affine(middle_planes)
        else:
            self.bn2_middle = nn.BatchNorm3d(middle_planes, track_running_stats=True,
                                             eps=eps, momentum=bn_mmt)

        self.conv2 = nn.Conv3d(middle_planes, planes, kernel_size=(temporal_kernel, 1, 1),
                               bias=False, stride=(temporal_stride, 1, 1),
                               padding=((temporal_kernel - 1) // 2, 0, 0))

        if use_affine:
            self.bn2 = Affine(planes)
        else:
            self.bn2 = nn.BatchNorm3d(planes, track_running_stats=True, eps=eps, momentum=bn_mmt)

        self.conv3 = nn.Conv3d(
            planes, planes * self.expansion, kernel_size=1, bias=False)

        if use_affine:
            self.bn3 = Affine(planes * self.expansion)
        else:
            self.bn3 = nn.BatchNorm3d(planes * self.expansion, track_running_stats=True,
                                      eps=eps, momentum=bn_mmt)

        self.relu = nn.ReLU(inplace=True)
        self.down_sample = down_sample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2_middle(out)
        out = self.bn2_middle(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.down_sample is not None:
            residual = self.down_sample(x)

        out += residual
        out = self.relu(out)

        return out


class ResNet_R2plus1Dv2(nn.Module):
    def __init__(self,
                 block,
                 block_nums,
                 num_classes=400,
                 feat_ext=False,
                 use_affine=True):

        self.use_affine = use_affine
        self.in_planes = 64
        self.num_classes = num_classes
        self.feat_ext = feat_ext

        super(ResNet_R2plus1Dv2, self).__init__()
        self.conv1_middle = nn.Conv3d(
            3,
            45,
            kernel_size=(1, 7, 7),
            stride=(1, 2, 2),
            padding=(0, 3, 3),
            bias=False)
        if use_affine:
            self.bn1_middle = Affine(45)
        else:
            self.bn1_middle = nn.BatchNorm3d(45, track_running_stats=True,
                                             eps=eps, momentum=bn_mmt)

        self.conv1 = nn.Conv3d(
            45,
            64,
            kernel_size=(3, 1, 1),
            stride=(1, 1, 1),
            padding=(1, 0, 0),
            bias=False)
        if use_affine:
            self.bn1 = Affine(64)
        else:
            self.bn1 = nn.BatchNorm3d(64, track_running_stats=True, eps=eps, momentum=bn_mmt)

        self.relu = nn.ReLU(inplace=True)

        self.layer1 = self._make_layer(block,
                                       in_planes=64,
                                       planes=64,
                                       middle_planes=144,
                                       blocks=block_nums[0],
                                       stride=1,
                                       expansion=4)

        self.layer2 = self._make_layer(block,
                                       in_planes=256,
                                       planes=128,
                                       middle_planes=288,
                                       blocks=block_nums[1],
                                       stride=2,
                                       temporal_stride=2,
                                       expansion=4)

        self.layer3 = self._make_layer(block,
                                       in_planes=512,
                                       planes=256,
                                       middle_planes=576,
                                       blocks=block_nums[2],
                                       stride=2,
                                       temporal_stride=2,
                                       expansion=4)

        self.layer4 = self._make_layer(block,
                                       in_planes=1024,
                                       planes=512,
                                       middle_planes=1152,
                                       blocks=block_nums[3],
                                       stride=2,
                                       temporal_stride=2,
                                       expansion=4)

        self.avgpool = nn.AdaptiveAvgPool3d(output_size=(1, 1, 1))

        self.out_fc = nn.Linear(in_features=2048, out_features=num_classes, bias=True)

    def _make_layer(self,
                    block,
                    in_planes,
                    planes,
                    middle_planes,
                    blocks,
                    stride=1,
                    temporal_stride=1,
                    expansion=4):

        if self.use_affine:
            down_bn = Affine(planes * expansion)
        else:
            down_bn = nn.BatchNorm3d(planes * expansion, track_running_stats=True,
                                     eps=eps, momentum=bn_mmt)
        down_sample = nn.Sequential(
            nn.Conv3d(
                in_planes,
                planes * expansion,
                kernel_size=1,
                stride=(temporal_stride, stride, stride),
                bias=False), down_bn)
        layers = []
        layers.append(
            block(in_planes, planes, middle_planes, stride, temporal_stride,
                  down_sample, expansion, temporal_kernel=3, use_affine=self.use_affine))
        for _ in range(1, blocks):
            layers.append(block(planes * expansion, planes, middle_planes, expansion=expansion,
                                temporal_kernel=3, use_affine=self.use_affine))

        return nn.Sequential(*layers)

    def forward(self, x):
        bs, _, _, _, _ = x.size()
        x = self.conv1_middle(x)
        x = self.bn1_middle(x)
        x = self.relu(x)

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.view(bs, -1)

        if self.feat_ext:
            return x

        logits = self.out_fc(x)
        return logits


def r2plus1d_v2_resnet152_kinetics400(cfg):
    model = ResNet_R2plus1Dv2(Bottleneck_R2plus1Dv2,
                              num_classes=cfg.CONFIG.DATA.NUM_CLASSES,
                              block_nums=[3, 8, 36, 3],
                              feat_ext=cfg.CONFIG.INFERENCE.FEAT,
                              use_affine=cfg.CONFIG.MODEL.USE_AFFINE)

    if cfg.CONFIG.MODEL.PRETRAINED:
        from ..model_store import get_model_file
        model.load_state_dict(torch.load(get_model_file('r2plus1d_v2_resnet152_kinetics400',
                                                        tag=cfg.CONFIG.MODEL.PRETRAINED)))
    return model
