# -*-coding:utf-8-*-
import os
import random
import numpy as np
from PIL import Image
from PIL import ImageFilter

import torch
from torchvision import transforms
from torch.utils.data import sampler, Dataset


class BDFC_Dataset(Dataset):
    def __init__(self,root,aug_times,batch_size,transforms=None):
        self.root = root
        self.imgs = self.get_img_paths(root)
        self.transforms = transforms
        self.iter = aug_times
        self.batch_size = batch_size

    def __getitem__(self, index):
        path = self.imgs[index]
        with open(path, 'rb') as f:
            with Image.open(f) as origin_img:
                origin_img = origin_img.convert('RGB')

        if self.transforms is not None:
            transformed_img_list = []
            target_list = []
            for i in range(self.iter):
                origin_transformed_img = self.transforms(origin_img)
                transformed_img_list.append(origin_transformed_img.numpy())
                target_list.append(index % self.batch_size)

            return torch.tensor(transformed_img_list),torch.tensor(target_list)

    def __len__(self):
        return len(self.imgs)

    def get_img_paths(self,root):
        imgs = []
        for subset in os.listdir(root):
            subset_path = os.path.join(root,subset)
            for img_name in os.listdir(subset_path):
                imgs.append(os.path.join(subset_path, img_name))
        random.shuffle(imgs)
        return imgs

class GaussianNoise(object):
    """Gaussian Noise Augmentation for tensor"""

    def __init__(self, sigma=0.1):
        self.sigma = sigma

    def __call__(self, img):
        noise = torch.randn(1,img.shape[1],img.shape[2])
        noise = torch.cat([noise,noise,noise],dim=0)
        return torch.clamp(img + self.sigma * noise,0.0,1.0)

class GaussianBlur(object):
    """Gaussian blur augmentation in SimCLR https://arxiv.org/abs/2002.05709"""

    def __init__(self, sigma=[.4, 2.]):
        self.sigma = sigma

    def __call__(self, x):
        sigma = random.uniform(self.sigma[0], self.sigma[1])
        x = x.filter(ImageFilter.GaussianBlur(radius=0.5))
        return x

# class InfiniteSampler(sampler.Sampler):
#     def __init__(self, num_samples):
#         self.num_samples = num_samples
#
#     def __iter__(self):
#         while True:
#             order = np.random.permutation(self.num_samples)
#             for i in range(self.num_samples):
#                 yield order[i]
#
#     def __len__(self):
#         return None


if __name__ == '__main__':
    K = 5
    epochs = 500
    batch_size = 4
    traindir = r"/media/damilu/file/data_set/MSTAR/train"
    num_workers = min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])
    train_transformation = transforms.Compose(
        [
            transforms.Grayscale(3),
            transforms.RandomResizedCrop(64, scale=(0.85, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomApply([transforms.RandomRotation(30)], p=0.2),
            transforms.RandomApply([transforms.ColorJitter(0.4, 0.4, 0.4)], p=0.4),
            transforms.ToTensor(),
            transforms.RandomApply([GaussianNoise()], p=0.2),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ]
    )
    train_dataset = BDFC_Dataset(traindir, K, batch_size, train_transformation)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    for epoch in range(epochs):
        for batch, (img_list, target_list) in enumerate(train_loader):
            print(img_list)
            print(target_list)