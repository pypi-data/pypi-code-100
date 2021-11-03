# -*-coding:utf-8-*-
import torch
import torch.nn as nn

# loss1
def CrossEntropyLoss():
    return nn.CrossEntropyLoss()

# loss2
class DWVLoss(nn.Module):
    def forward(self, x):
        return torch.sum(torch.mean(torch.std(x, dim=1), dim=1))