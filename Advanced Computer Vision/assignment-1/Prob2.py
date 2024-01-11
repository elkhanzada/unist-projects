import torch.nn as nn
import torchvision


class TimePredictor(nn.Module):
    """
    TimePredictor model consists of Resnet18 and two extra hour, minute layers.
    """

    def __init__(self):
        super(TimePredictor, self).__init__()
        self.model = torchvision.models.resnet18(pretrained=True)
        self.hour = nn.Linear(self.model.fc.out_features, 1)
        self.minute = nn.Linear(self.model.fc.out_features, 1)

    def forward(self, x):
        x = self.model(x)
        x_hour = self.hour(x)
        x_minute = self.minute(x)
        return x_hour, x_minute
