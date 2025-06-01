import torch.nn as nn
from torchvision.models import resnet34, ResNet34_Weights

class RAFResNet(nn.Module):
    def __init__(self, num_classes=7):
        super().__init__()
        weights = ResNet34_Weights.IMAGENET1K_V1
        self.backbone = resnet34(weights=weights)
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, num_classes)

    def forward(self, x):
        return self.backbone(x)
