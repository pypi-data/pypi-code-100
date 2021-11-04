#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written by Mr. HuChang

import torch.nn as _nn
import torch.nn.functional as _F
from .attention import ConvMultiHeadAttention as _CMHA
import matplotlib.pyplot as _plt
import matplotlib_inline as _mat
import numpy as _np
import seaborn as _sns
import sys as _sys
from torchvision.utils import make_grid
import torch as _torch
from IPython import display as _display


_mat.backend_inline.set_matplotlib_formats("svg")


def torch_summary(net, human_style=False):
    total_num = sum(p.numel() for p in net.parameters())
    trainable_num = sum(p.numel() for p in net.parameters() if p.requires_grad)

    return {'Total': num_transform(total_num) if human_style else total_num,
            'Trainable': num_transform(trainable_num) if human_style else trainable_num,
            "Non-Trainable": num_transform(total_num - trainable_num) if human_style else (total_num - trainable_num)}


def num_transform(num):

    if num / 1000 < 1:
        return num

    elif num / 1000000 < 1:
        return str(num // 1000) + "K"

    else:
        return str(num // 1000000) + "M"



class ClassicalBlock(_nn.Module):

    def __init__(self, in_channles, out_channels, kernel_size,
                 stride, padding):
        super().__init__()
        self.backbone = _nn.Sequential(
            _nn.Conv2d(in_channles, out_channels, kernel_size,
                       stride, padding),
            _nn.BatchNorm2d(out_channels),
            _nn.ReLU(),
        )

    def forward(self, x):
        return self.backbone(x)


class BasicBlock(_nn.Module):
    """
    Example:
        >>>m = BasicBlock(3, 12, 2)
        >>>data = torch.randn(5, 3, 32, 32)
        >>>m(data).shape>>>
        >>>torch.Size([5, 12, 16, 16])
    """
    def __init__(self, in_channles, out_channels, stride):
        super().__init__()
        self.features = ClassicalBlock(in_channles, out_channels, 3,
                                       stride, 1)
        self.net = _nn.Sequential(
            _nn.Conv2d(out_channels, out_channels, 3, 1, 1),
            _nn.BatchNorm2d(out_channels)
        )

        self.shortcut = _nn.Conv2d(in_channles, out_channels, kernel_size=3,
                                   padding=1, stride=stride)

    def forward(self, x):
        y = self.features(x)
        y = self.net(y)
        z = self.shortcut(x)
        return _F.relu(y + z)


class TrainProfiler(object):
    """
    Example:
        >>>profiler = hzau.misc.TrainProfiler(len(data_loader), metric=True)
        >>>Epoch = 50
        >>>for i in range(Epoch):
        >>>    for idx, (d, l) in enumerate(data_loader):
        >>>       >>> d = d.to("cuda")
        >>>        l = l.long().to("cuda")
        >>>        out, probs = model(d)
        >>>        loss = criterion(out, l)
        >>>        optimizer.zero_grad()
        >>>        loss.backward()
        >>>        optimizer.step()
        >>>        metric = hzau.misc.cal_acc(probs, l)
        >>>        profiler.log(idx, loss, metric)
        >>>
        >>>    profiler.loss_curve()
        >>>    profiler.mertic_curve()
    """

    def __init__(self, step_length, metric=False):
        self.temp_loss = []
        self.losses = []
        self.trained_epoch = 0
        self.current_step = 0
        self.step_length = step_length
        self.metric = metric
        if metric:
            self.metrics = []
            self.temp_metric = []


    def log(self, step, loss, metric=None,
            log=True, file=_sys.stdout, clear=False):
        self.current_step += 1
        if log and metric == None:
            print("Epoch={:<3} Step[{:>3}/{}] loss={:.5f}".format(
                self.trained_epoch + 1, self.current_step,
                self.step_length, loss.item()), file=file)

        if log and metric != None:
            print("Epoch={:<3} Step[{:>3}/{}] loss={:.5f} metric={:.5f}".format(
                self.trained_epoch + 1,  self.current_step,
                self.step_length, loss.item(), metric), file=file)

        self.temp_loss.append(loss.item())
        if metric != None:
            if isinstance(metric, _torch.Tensor):
                self.temp_metric.append(metric.item())
            else:
                self.temp_metric.append(metric)

        if self.current_step == self.step_length:
            self.current_step = 0
            self.trained_epoch += 1
            self.losses.append(_np.mean(self.temp_loss))
            self.temp_loss = []
            if metric != None:
                self.metrics.append(_np.mean(self.temp_metric))
                self.temp_metric = []
        if clear == True:
            _display.clear_output()

    def loss_curve(self, x_label="x", y_label="y",
                   title="Loss Curve", delta=.00001):

        ax = _sns.lineplot(x=_np.arange(len(self.losses)) + 1, y=self.losses)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        _plt.show()
        _plt.pause(delta)


    def mertic_curve(self, x_label="x", y_label="y",
                   title="Metric Curve", delta=.00001):
        ax = _sns.lineplot(x=_np.arange(len(self.metrics)) + 1, y=self.metrics)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        _plt.show()
        _plt.pause(delta)


def imshow(data):
    images = make_grid(data.detach().cpu(), normalize=True, padding=5, pad_value=1)
    _plt.imshow(images.permute(1, 2, 0))
    _plt.axis("off")
    _plt.grid(False)
    _plt.pause(0.00001)


def cal_acc(out, labels):

    return sum(out.argmax(dim=-1) == labels) / sum(labels.shape)


class ModelProfiler(TrainProfiler):
    """
    Example:
        >>>profiler = hzau.misc.ModelProfiler(len(data_loader), metric=True)
        >>>Epoch = 100
        >>>model = model.train()
        >>>for i in range(Epoch):
        >>>    for idx, (d, l) in enumerate(data_loader):
        >>>        d = d.to(>>>"cuda")
        >>>        l = l.long().to("cuda")
        >>>        out, probs = model(d)
        >>>        loss = criterion(out, l)
        >>>        optimizer.zero_grad()
        >>>        loss.backward()
        >>>        optimizer.step()
        >>>        metric = hzau.misc.cal_acc(probs, l)
        >>>        if profiler.trained_epoch % 20 == 0 and profiler.current_step == 1:
        >>>            profiler.log(idx, loss, metric, clear=True)
        >>>        profiler.log(idx, loss, metric)
        >>>    loss, acc = evaluation(model)
        >>>    profiler.log_eval(loss, acc)
        >>>    model = model.train()
        >>>    scheduler.step()
        >>>    profiler.loss_curve()
        >>>    profiler.mertic_curve()
    """
    def __init__(self, step_length, metric=False):

        super().__init__(step_length, metric)
        self.eval_losses = []
        self.eval_metric = []

    def log_eval(self, loss, metric):
        if isinstance(loss, _torch.Tensor):
            self.eval_losses.append(loss.item())
        else:
            self.eval_losses.append(loss)
        if isinstance(metric, _torch.Tensor):
            self.eval_metric.append(metric.item())
        else:
            self.eval_metric.append(metric)

    def loss_curve(self, x_label="x", y_label="y",
                   title="Loss Curve", delta=.00001):

        ax = _sns.lineplot(x=_np.arange(len(self.losses)) + 1,
                           y=self.losses, label="Train")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.plot(_np.arange(len(self.eval_losses)) + 1,
                self.eval_losses, label="Test")
        ax.legend()
        _plt.show()
        _plt.pause(delta)


    def mertic_curve(self, x_label="x", y_label="y",
                   title="Metric Curve", delta=.00001):
        ax = _sns.lineplot(x=_np.arange(len(self.metrics)) + 1,
                           y=self.metrics, label="Train")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.plot(_np.arange(len(self.eval_metric)) + 1,
                self.eval_metric, label="Test")
        ax.legend()
        _plt.show()
        _plt.pause(delta)
