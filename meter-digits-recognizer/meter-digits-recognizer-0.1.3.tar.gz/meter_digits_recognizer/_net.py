import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

__all__ = ["Net"]


class Net(nn.Module):
    test_transform = transforms.Compose([
        transforms.ToTensor()
    ]) 

    train_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.ColorJitter(brightness=0.1),
        transforms.RandomAffine(5.0,  translate=(0.1, 0.1), scale=(1.0, 1.2),
            interpolation=transforms.InterpolationMode.BILINEAR),
    ])

    def __init__(self):
        nn.Module.__init__(self)
        self.n_filters1 = 32
        self.n_filters2 = 64
        self.n_filters3 = 64
        self.input_size = (20, 32)
      
        self.batchnorm = nn.BatchNorm2d(3)
        self.conv1 = nn.Conv2d(3, self.n_filters1, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(self.n_filters1, self.n_filters2, 3, padding=1)
        self.conv3 = nn.Conv2d(self.n_filters2, self.n_filters3, 3, padding=1)
        self.fc1 = nn.Linear(4 * 2 * self.n_filters3, 512)
        self.fc2 = nn.Linear(512, 11)

    def forward(self, x):
        x = self.batchnorm(x)
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 4 * 2 * self.n_filters3)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
