from datetime import datetime
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F


def conv3x3(in_ch, out_ch, stride=1):
    return nn.Conv2d(in_ch, out_ch, 3, stride=stride, padding=1, bias=False)


def _add_stage(block, in_ch, out_ch, stride, repeat_time):
    assert repeat_time > 0 and isinstance(repeat_time, int)
    layers = [block(in_ch, out_ch, stride)]
    for _ in range(repeat_time - 1):
        layers.append(block(out_ch, out_ch, 1))
    return nn.Sequential(*layers)


class BasicBlock(nn.Module):

    def __init__(self, in_ch, out_ch, stride, expansion=1):
        assert out_ch % expansion == 0
        mid_ch = int(out_ch / expansion)
        super().__init__()
        self.do_downsample = not (in_ch == out_ch and stride == 1)
        self.conv1 = conv3x3(in_ch, mid_ch, stride=stride)
        self.bn1 = nn.BatchNorm2d(mid_ch)
        self.conv2 = conv3x3(mid_ch, out_ch, stride=1)
        self.bn2 = nn.BatchNorm2d(out_ch)
        self.relu = nn.ReLU(inplace=True)

        if self.do_downsample:
            self.residual = nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 1, stride, bias=False),
                nn.BatchNorm2d(out_ch),
            )

    def forward(self, x):
        residual = x
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)

        if self.do_downsample:
            residual = self.residual(residual)
        x += residual

        return self.relu(x)


class ModernUpConv(nn.Module):

    def __init__(self, in_ch, out_ch, scale_factor=2):
        super(ModernUpConv, self).__init__()
        self.scale_factor = scale_factor
        self.interpolate_conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        x = F.interpolate(x,
                          scale_factor=self.scale_factor,
                          mode='bilinear',
                          align_corners=True)
        return self.interpolate_conv(x)


class ModernUpBlock(nn.Module):

    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.up_conv = ModernUpConv(in_ch, out_ch)
        self.up_block = BasicBlock(out_ch * 2, out_ch, 1)

    def forward(self, encoded, x):
        x = self.up_conv(x)
        x = torch.cat((encoded, x), dim=1)
        return self.up_block(x)


class ResNet34(nn.Module):

    def __init__(self):
        super().__init__()
        self.channels = [64, 64, 128, 256, 512]
        self.stage0 = nn.Sequential(
            nn.Conv2d(3, self.channels[0], 7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(self.channels[0]),
            nn.ReLU(inplace=True),
        )
        self.stage1 = nn.Sequential(nn.MaxPool2d(3, stride=2, padding=1))
        for layer in _add_stage(BasicBlock, self.channels[0], self.channels[1],
                                1, 3):
            self.stage1.add_module(str(len(self.stage1)), layer)
        self.stage2 = _add_stage(BasicBlock, self.channels[1], self.channels[2],
                                 2, 4)
        self.stage3 = _add_stage(BasicBlock, self.channels[2], self.channels[3],
                                 2, 6)
        self.stage4 = _add_stage(BasicBlock, self.channels[3], self.channels[4],
                                 2, 3)

    def forward(self, x):
        x = self.stage0(x)  # 64, 1/2
        x = self.stage1(x)  # 64, 1/4
        x = self.stage2(x)  # 128, 1/8
        x = self.stage3(x)  # 256, 1/16
        x = self.stage4(x)  # 512, 1/32
        return x


class ModernUNet(nn.Module):

    def __init__(self, num_classes=1):
        super().__init__()
        self.device = 'cpu'
        self.backbone = ResNet34()
        self.up_block4 = ModernUpBlock(self.backbone.channels[4],
                                       self.backbone.channels[3])
        self.up_block3 = ModernUpBlock(self.backbone.channels[3],
                                       self.backbone.channels[2])
        self.up_block2 = ModernUpBlock(self.backbone.channels[2],
                                       self.backbone.channels[1])
        self.up_block1 = ModernUpBlock(self.backbone.channels[1],
                                       self.backbone.channels[0])
        self.outputs = nn.Sequential(
            ModernUpConv(self.backbone.channels[0], self.backbone.channels[0]),
            nn.Conv2d(self.backbone.channels[0], num_classes, 1, bias=False),
        )

    def forward(self, x):
        e1 = self.backbone.stage0(x)
        e2 = self.backbone.stage1(e1)
        e3 = self.backbone.stage2(e2)
        e4 = self.backbone.stage3(e3)
        e5 = self.backbone.stage4(e4)
        d4 = self.up_block4(e4, e5)
        d3 = self.up_block3(e3, d4)
        d2 = self.up_block2(e2, d3)
        d1 = self.up_block1(e1, d2)
        return self.outputs(d1)

    def init(self, device='cuda', params=None):
        print(f'{datetime.now().ctime()} - Start initialization...')
        self.change_device(device=device)
        if params:
            self.load_params(params)
        print(f'{datetime.now().ctime()} - Finish initialization')

    def change_device(self, device):
        assert device in ['cpu', 'cuda'], 'device should be \'cpu\' or \'cuda\''
        self.device = device
        self.to(device=self.device)
        print(f'{datetime.now().ctime()} - Change device to {self.device}')

    def load_params(self, params):
        print(f'{datetime.now().ctime()} - Start loading params...')
        missing_keys, unexpected_keys = self.load_state_dict(
            torch.load(params, map_location=self.device))
        if len(missing_keys) == 0 and len(unexpected_keys) == 0:
            print(f'{datetime.now().ctime()} - Finish loading params')
        else:
            print(f'{missing_keys}')
            print(f'{unexpected_keys}')

    def predict(self, image, threshold=0.5):
        self.eval()
        image = self._normalize(image)
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, 0)
        image = torch.Tensor(image)
        image = image.to(device=self.device)
        with torch.no_grad():
            mask = self.forward(image)
            mask = torch.sigmoid(mask)
            mask = mask > threshold
        mask = mask.cpu().numpy()
        mask = np.squeeze(mask)
        return mask

    def _normalize(self,
                   img,
                   mean=(0.485, 0.456, 0.406),
                   std=(0.229, 0.224, 0.225),
                   max_pixel_value=255.0):
        mean = np.array(mean, dtype=np.float32)
        mean *= max_pixel_value
        std = np.array(std, dtype=np.float32)
        std *= max_pixel_value
        denominator = np.reciprocal(std, dtype=np.float32)
        img = img.astype(np.float32)
        img -= mean
        img *= denominator
        return img
