import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 32, 3, padding=1, bias=False)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1, bias=False)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1, bias=False)
        self.conv4 = nn.Conv2d(128, 256, 3, padding=1, bias=False)

        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(p=0.2)
        self.batchnorm1 = nn.BatchNorm2d(32)
        self.batchnorm2 = nn.BatchNorm2d(64)
        self.batchnorm3 = nn.BatchNorm2d(128)
        self.batchnorm4 = nn.BatchNorm2d(256)

        self.fc1 = nn.Linear(256 * 14 * 14, 1024)
        self.fc2 = nn.Linear(1024, 1024)
        self.fc3 = nn.Linear(1024, 136)

    def forward(self, x):
        x = self.pool(F.elu(self.batchnorm1(self.conv1(x))))
        x = self.dropout(x)

        x = self.pool(F.elu(self.batchnorm2(self.conv2(x))))
        x = self.dropout(x)

        x = self.pool(F.elu(self.batchnorm3(self.conv3(x))))
        x = self.dropout(x)

        x = self.pool(F.elu(self.batchnorm4(self.conv4(x))))
        x = self.dropout(x)

        x = x.view(x.size(0), -1)
        x = F.elu(self.fc1(x))
        x = self.dropout(x)

        x = F.elu(self.fc2(x))
        x = self.dropout(x)

        x = self.fc3(x)

        return x
