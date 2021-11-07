import torch
import torch.nn.functional as F
from . import metric
from . import utils

__all__ = ['MSSIM']


class SSIM(object):
    def __init__(self) -> None:
        super().__init__()


class MSSIM(metric.Metric):
    def __init__(self,
                 window_size=None,
                 K1=0.01,
                 K2=0.03,
                 sigma=1.5,
                 L=1.0,
                 downsample=True) -> None:
        super().__init__()
        self.downsample = downsample
        truncate = 3.5

        if window_size == None:
            r = round(truncate * sigma)
            window_size = 2 * r + 1
        else:
            window_size = window_size

        self.gauss_filter = utils.filter.GaussianFilter(window_size, sigma)
        NP = window_size**2
        self.conv_norm = NP / (NP - 1)
        self.C1 = (K1 * L)**2
        self.C2 = (K2 * L)**2

    def calc(self, img_a: torch.Tensor, img_b: torch.Tensor):
        C, H, W = img_a.size()
        f = max(1, round(min(H, W) / 256))

        if f > 1 and self.downsample == True:
            img_a = F.avg_pool2d(img_a.unsqueeze(0), kernel_size=f).squeeze()
            img_b = F.avg_pool2d(img_b.unsqueeze(0), kernel_size=f).squeeze()

        if C == 1:
            mu_a = self.gauss_filter(img_a)
            mu_b = self.gauss_filter(img_b)
            mu_aa, mu_bb, mu_ab = mu_a**2, mu_b**2, mu_a * mu_b
            sigma_aa = self.gauss_filter(img_a**2) - mu_aa
            sigma_bb = self.gauss_filter(img_b**2) - mu_bb
            sigma_ab = self.gauss_filter(img_a * img_b) - mu_ab
            A1 = 2.0 * mu_ab + self.C1
            A2 = 2.0 * sigma_ab + self.C2
            B1 = (mu_aa + mu_bb + self.C1)
            B2 = (sigma_aa + sigma_bb + self.C2)
            mssim = torch.mean((A1 * A2) / (B1 * B2))
            return mssim
        else:
            total_value = 0
            split_channels_img_a = torch.chunk(img_a, C)
            split_channels_img_b = torch.chunk(img_b, C)

            for channel in range(C):
                total_value += self.calc(split_channels_img_a[channel],
                                         split_channels_img_b[channel])

            return total_value / C
