"""ResNet18 adapted to 6 input channels (B, G, R, RedEdge, NIR, NDVI)."""

import torch
import torch.nn as nn
from torchvision import models

NUM_CHANNELS = 6
NUM_CLASSES = 2  # 0 = non-wheat (soybean in training), 1 = wheat


def build_model(num_channels: int = NUM_CHANNELS, num_classes: int = NUM_CLASSES,
                pretrained: bool = False) -> nn.Module:
    """Build the network.

    With `pretrained=True` the ImageNet weights are loaded and the first conv
    is widened to 6 channels: RGB filters are copied as-is, the 3 extra
    channels get the mean RGB filter (this is how the released model was
    initialised before fine-tuning).
    """
    weights = models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
    model = models.resnet18(weights=weights)

    old_conv = model.conv1
    model.conv1 = nn.Conv2d(
        num_channels, old_conv.out_channels,
        kernel_size=old_conv.kernel_size, stride=old_conv.stride,
        padding=old_conv.padding, bias=False,
    )
    if pretrained:
        with torch.no_grad():
            model.conv1.weight[:, :3] = old_conv.weight
            mean_w = old_conv.weight.mean(dim=1, keepdim=True)
            model.conv1.weight[:, 3:] = mean_w.repeat(1, num_channels - 3, 1, 1)

    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


def load_model(weights_path: str, device: str | torch.device = "cpu") -> nn.Module:
    """Load models/best_model.pth (a plain state_dict) in eval mode."""
    model = build_model()
    state = torch.load(weights_path, map_location=device, weights_only=True)
    model.load_state_dict(state)
    return model.to(device).eval()
