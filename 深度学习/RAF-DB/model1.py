# model1.py

import torch.nn as nn
from torchvision.models import resnet34, ResNet34_Weights

class RAFResNet(nn.Module):
    def __init__(self, num_classes=7, dropout_p=0.5):
        super().__init__()
        # 加载 ResNet-34 ImageNet 预训练权重
        weights = ResNet34_Weights.IMAGENET1K_V1
        self.backbone = resnet34(weights=weights)
        # 替换最后的全连接层：Dropout + Linear
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(p=dropout_p),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)
