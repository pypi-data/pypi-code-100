#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written by Mr. HuChang


from __future__ import print_function
import torch.nn as _nn
import torch.nn.functional as _F
import math as _math
import torch as _torch


class SelfAttention(_nn.Module):
    """
    Input shape: B x C x F
    apply self attention in dimension `C`
    Parameters:
        W: dimension of the column of the matrix
        d_k: same size as C
        output_size: the output size of the last dimension
        verbose: print attention matrix dimension
    Example:
        >>>data = torch.randn(5, 625, 3)
        >>>m = SelfAttention(W=3, d_k=100, output_size=100)
        >>>m(data).shape
        >>>torch.Size([5, 625, 100])
        ============================
        >>>data = torch.randn(5, 625, 3)
        >>>m = SelfAttention(W=3, d_k=100)
        >>>m(data).shape
        >>>torch.Size([5, 625, 3])
        ============================
        >>>data = torch.randn(5, 3, 32, 32)
        >>>data = data.view(5, 3, -1)
        >>>data = data.transpose(1, 2)
        >>>m = SelfAttention(W=3, d_k=100)
        >>>m(data).shape
        >>>torch.Size([5, 1024, 3])
        ===========================
        >>>data = torch.randn(5, 3, 32, 32)
        >>>data = data.view(5, 3, -1)
        >>>data = data.transpose(1, 2)
        >>>m = SelfAttention(W=3, d_k=100, output_size=1000, verbose=True)
        >>>the attention matrix shape is torch.Size([5, 1024, 1024])
        >>>torch.Size([5, 1024, 1000])
    """

    def __init__(self, W, d_k=None, output_size=None, dropout=0.,
                 verbose=False):
        super().__init__()
        if output_size == None:
            output_size = W
        if d_k == None:
            d_k = W
        self.Q = _nn.Linear(W, d_k)
        self.K = _nn.Linear(W, d_k)
        self.V = _nn.Linear(W, output_size)
        self.d_k = d_k
        self.dropout = _nn.Dropout(dropout)
        self.verbose = verbose

    def forward(self, x):
        assert len(x.shape) == 3, "x's shape should be B x C x F"
        Q = self.Q(x)
        K = self.K(x)
        V = self.V(x)
        dot_product = _torch.bmm(Q, K.transpose(1, 2)) / _math.sqrt(self.d_k)
        dot_product = _F.softmax(dot_product, dim=-1)
        if self.verbose:
            print(f"the attention matrix shape is {dot_product.shape}")
        out = self.dropout(dot_product)
        out = _torch.bmm(out, V)
        return out


class MultiHeadAttention(_nn.Module):
    """
    Input shape: B x C x F
    apply self attention in dimension `C`
    Parameters:
        W: dimension of the column of the matrix
        num_heads: number of heads
        d_k: same as Self Attention default = W
        output_size: the output size of the last dimension default = W
        verbose: print attention matrix dimension
        V_outsize: Value matrix column size
    Example:
        >>>m = MultiHeadAttention(100, 10, output_size=200, verbose=True)
        >>>data = torch.randn(5, 50, 100)
        >>>m(data).shape
        >>>the attention matrix shape is torch.Size([5, 10, 50, 50])
        >>>torch.Size([5, 50, 200])
        ====================================
        >>>m = MultiHeadAttention(100, 5, verbose=True)
        >>>data = torch.randn(5, 50, 100)
        >>>m(data).shape
        >>>the attention matrix shape is torch.Size([5, 5, 50, 50])
        >>>torch.Size([5, 50, 100])
        ====================================
        >>>m = MultiHeadAttention(100, 3, V_outsize=500, verbose=True)
        >>>data = torch.randn(5, 50, 100)
        >>>m(data).shape
        >>>the attention matrix shape is torch.Size([5, 3, 50, 50])
        >>>torch.Size([5, 50, 100])
    """

    def __init__(self, W, num_heads, output_size=None, d_k=None,
                 V_outsize=None, dropout=0., verbose=False):
        super().__init__()
        self.num_heads = num_heads
        if V_outsize == None:
            V_outsize = W
        if d_k == None:
            d_k = W
        if output_size == None:
            output_size = W
        self.V_outsize = V_outsize
        self.Q = _nn.Linear(W, d_k * num_heads)
        self.K = _nn.Linear(W, d_k * num_heads)
        self.V = _nn.Linear(W, V_outsize * num_heads)
        self.d_k = d_k
        self.dropout = _nn.Dropout(dropout)
        self.verbose = verbose
        self.output_size = output_size
        self.dim_reduction = _nn.Linear(V_outsize * num_heads, output_size)

    def forward(self, x):
        assert len(x.shape) == 3, "x's shape should be B x C x F"
        B, C, f = x.shape
        Q = self.Q(x).view(B, C, -1, self.num_heads).permute(0, 3, 1, 2)
        K = self.K(x).view(B, C, -1, self.num_heads).permute(0, 3, 2, 1)
        V = self.V(x).view(B, C, -1, self.num_heads).permute(0, 3, 1, 2)
        attention = _F.softmax(_torch.matmul(Q, K) / _math.sqrt(self.d_k), -1)
        if self.verbose:
            print(f"the attention matrix shape is {attention.shape}")
        out = _torch.matmul(attention, V).view(B, C,
                                              self.V_outsize * self.num_heads)
        return self.dim_reduction(out)


class ConvSelfAttention(_nn.Module):
    """
    Input: B x C x H x W
    Parameters:
        in_channels: equals to C
        out_channels: same as out_chaneels in Conv2d
        kernel_size: size of convolutional kernel
    Example:
        >>>m = ConvSelfAttention(3, d_k=10, out_channels=12, verbose=True)
        >>>data = torch.randn(5, 3, 32, 32)
        >>>m(data).shape
        >>>the attention matrix shape is torch.Size([5, 1024, 1024])
        >>>torch.Size([5, 12, 32, 32])
    """
    def __init__(self, in_channels, d_k, out_channels, kernel_size=3,
                 verbose=False):
        super().__init__()

        self.d_k = d_k
        self.out_channels = out_channels
        self.verbos = verbose
        self.Q = _nn.Conv2d(in_channels, d_k, kernel_size=kernel_size,
                           padding="same")
        self.K = _nn.Conv2d(in_channels, d_k, kernel_size=kernel_size,
                           padding="same")
        self.V = _nn.Conv2d(in_channels, out_channels, kernel_size,
                           padding="same")

    def forward(self, x):
        assert len(x.shape) == 4, "x's shape should be B x C x H x W"
        B, C, H, W = x.shape
        Q = self.Q(x).view(B, self.d_k, -1)
        K = self.K(x).view(B, self.d_k, -1)
        V = self.V(x).view(B, self.out_channels, -1)

        attention = _F.softmax(_torch.bmm(Q.transpose(1, 2), K) / _math.sqrt(self.d_k),
                              dim=-1)
        if self.verbos:
            print(f"the attention matrix shape is {attention.shape}")
        out = _torch.bmm(V, attention.transpose(1, 2))

        return out.view(B, -1, H, W)


class ConvMultiHeadAttention(_nn.Module):
    """
    Input: B x C x H x W
    Parameters:
        in_channels: equals to C
        out_channels: same as out_chaneels in Conv2d
        kernel_size: size of convolutional kernel
        num_heads: number of self attention
        V_out_channels: Value matrix column size
    Example:
        >>>m = ConvMultiHeadAttention(in_channels=3, d_k=12, V_out_channels=12,
        >>>                          num_heads=5, out_channels=12, verbose=True)
        >>>data = torch.randn(5, 3, 32, 32)
        >>>m(data).shape
        >>>the attention matrix shape is torch.Size([5, 5, 1024, 1024])
        >>>torch.Size([5, 12, 32, 32])
    """

    def __init__(self, in_channels, d_k, V_out_channels, num_heads,
                 out_channels, kernel_size=3, verbose=False,
                 transform_dropout=.0, dropout=.0):
        super().__init__()

        self.d_k = d_k
        self.out_channels = out_channels
        self.V_out_channels = V_out_channels
        self.num_heads = num_heads
        self.verbos = verbose
        self.Q = _nn.Conv2d(in_channels, d_k * num_heads, kernel_size,
                           padding="same")
        self.K = _nn.Conv2d(in_channels, d_k * num_heads, kernel_size,
                           padding="same")
        self.V = _nn.Conv2d(in_channels, V_out_channels * num_heads, kernel_size,
                           padding="same")
        self.channel_transform = _nn.Linear(V_out_channels * num_heads,
                                           out_channels)
        self.dropout = _nn.Dropout(dropout)
        self.Q_dropout = _nn.Dropout(transform_dropout)
        self.K_dropout = _nn.Dropout(transform_dropout)
        self.V_dropout = _nn.Dropout(transform_dropout)

    def forward(self, x):
        assert len(x.shape) == 4, "x's shape should be B x C x H x W"
        B, C, H, W = x.shape
        Q = self.Q(x).view(B, self.d_k, H * W,
                           self.num_heads).permute(0, 3, 1, 2)
        K = self.K(x).view(B, self.d_k, H * W,
                           self.num_heads).permute(0, 3, 2, 1)
        V = self.V(x).view(B, self.V_out_channels, H * W,
                           self.num_heads).permute(0, 3, 1, 2)
        Q = self.Q_dropout(Q)
        V = self.V_dropout(V)
        K = self.V_dropout(K)
        attention = _F.softmax(_torch.matmul(K, Q) / _math.sqrt(self.d_k),
                              dim=-1)
        attention = self.dropout(attention)
        if self.verbos:
            print(f"the attention matrix shape is {attention.shape}")
        out = _torch.matmul(V, attention.transpose(-1, -2))
        out = self.channel_transform(out.view(B, H * W, -1))

        return out.view(B, -1, H, W)

