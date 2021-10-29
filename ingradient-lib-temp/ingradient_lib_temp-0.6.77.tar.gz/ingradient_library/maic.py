from torch.utils.data import Dataset, DataLoader
from ingradient_library.transform import Transform
from ingradient_library.preprocessing import *
from ingradient_library.get_nnunet_setting import get_transform_params
import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np
import os
import h5py
import copy


class MAIC_Sampling(object):
    def __init__(self,  train = True, transform = Transform(*get_transform_params(None))):
        self.transform = transform
        self.train = train
    def __call__(self, images, seg = None, is_CT = True):
        temp = copy.deepcopy(images)
        if is_CT:
            temp[np.where(temp < - 700)] = 0
        non_zero_index = np.where(temp.astype(int) != 0)
        min_val = np.min(non_zero_index, axis = 1)
        max_val = np.max(non_zero_index, axis = 1)
        random_move = np.random.randint([-5,-5,-5], [5, 5, 5])
        images = images[:, min_val[-3]:max_val[-3]+1, min_val[-2]:max_val[-2]+1, min_val[-1]:max_val[-1]+1]
        z_start = int(images.shape[-1] * 0.25)
        z_term = 96
        y_start = images.shape[-2]//2 - 32
        y_end= images.shape[-2]//2 + 32
        x_term = 64
        images = images[:, 5 + random_move[0]:x_term+random_move[0]+5, y_start+random_move[1]:y_end+random_move[1],
                       -(z_start + z_term) + random_move[2]:-z_start + random_move[2]]
        if self.train:
            seg = seg[min_val[-3]:max_val[-3]+1, min_val[-2]:max_val[-2]+1, min_val[-1]:max_val[-1]+1]
            seg = seg[5 + random_move[0]:x_term+random_move[0]+5, y_start+random_move[1]:y_end+random_move[1],
                       -(z_start + z_term) + random_move[2]:-z_start + random_move[2]]
            images = torch.tensor(images).unsqueeze(0).double()
            seg = torch.tensor(seg).unsqueeze(0).long()
            if self.transform != None:
                images, seg = self.transform(images, seg, None)
            images = images.squeeze(0).numpy()
            seg = seg.squeeze(0).numpy()
        else: 
            seg = None

        return images, seg


class MAIC_Dataset(Dataset):
    def __init__(self, path = None, normalizer = True, train = True, transform = Transform(*get_transform_params(None))):
        if path == None:
            path = '../mnt/dataset/'
        
        self.path = path
        self.file_list = []
        for f in os.listdir(path):
            if not 'py' in f:
                self.file_list.append(f)
        
        self.file_list = sorted(self.file_list)
        self.normalizer = normalizer
        self.train = train
        self.sampler = MAIC_Sampling(transform = transform, train = train)
        self.norm1 = Fixed_Normalizer(mean = 20.78, std = 180.50, min = -986, max = 271,  device = None)
        
    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        current_file = os.path.join(self.path, self.file_list[idx])
        hdf_file = h5py.File(current_file , 'r')
        CT = np.array(hdf_file['CT'])
        PET = np.array(hdf_file['PET'])
        spacing = np.array(hdf_file['Size'])
        images = np.expand_dims(CT, axis = 0)
        
        if self.train:
            seg = np.array(hdf_file['Aorta'])

        hdf_file.close()
        
        images, seg = self.sampler(images, seg)
        if self.normalizer:
            images[0] = self.norm1(images[0])
        
        return images, seg, spacing, CT.shape



def conv_block(in_channels, out_channels, kernel_size, stride, padding):
    return nn.Sequential(nn.Conv3d(in_channels, out_channels, kernel_size, stride, padding),
                         nn.Dropout3d(),
                         nn.InstanceNorm3d(out_channels),
                         nn.LeakyReLU())

def trans_conv_block(in_channels, out_channels, kernel_size, stride, padding, output_padding):
    return nn.Sequential(nn.ConvTranspose3d(in_channels, out_channels, kernel_size, stride, padding, output_padding),
                         nn.Dropout3d(),
                         nn.BatchNorm3d(out_channels),
                         nn.LeakyReLU())
    
def encoder_block(in_channels, out_channels, kernel_size = 3, stride = 2):
    return nn.Sequential(conv_block(in_channels, out_channels, kernel_size, stride, padding = 1),
                         conv_block(out_channels, out_channels, kernel_size, stride = 1, padding = 1))

class UNet3d_MultiModal(nn.Module):
    def __init__(self, in_channels = 1, out_channels = 2, n_channels = 32, channel_bound = 1024):
        super().__init__()
        channel_bound = min(n_channels * 32, channel_bound)
        self.expand_channels_CT = encoder_block(in_channels, n_channels, stride = 1)
        self.conv_downsample1_CT = encoder_block(n_channels, n_channels * 2)
        self.conv_downsample2_CT = encoder_block(n_channels * 2, n_channels * 4)
        self.conv_downsample3_CT = encoder_block(n_channels * 4, n_channels * 8)
        self.conv_downsample4_CT = encoder_block(n_channels * 8, n_channels * 16)
        self.conv_downsample5_CT = encoder_block(n_channels * 16, channel_bound)

        self.conv_upsample1_CT = nn.ConvTranspose3d(channel_bound, n_channels * 16, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample2_CT = nn.ConvTranspose3d(n_channels * 16, n_channels * 8, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample3_CT= nn.ConvTranspose3d(n_channels * 8, n_channels * 4, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample4_CT= nn.ConvTranspose3d(n_channels * 4, n_channels * 2, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample5_CT= nn.ConvTranspose3d(n_channels * 2, n_channels, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        

        self.decoder1_CT = encoder_block(n_channels * 1 * 2, n_channels, stride = 1)
        self.decoder2_CT = encoder_block(n_channels * 2 * 2, n_channels * 2, stride = 1)
        self.decoder3_CT = encoder_block(n_channels * 4 * 2, n_channels * 4, stride = 1)
        self.decoder4_CT = encoder_block(n_channels * 8 * 2, n_channels * 8, stride = 1)
        self.decoder5_CT = encoder_block(n_channels * 16 * 2, n_channels * 16, stride = 1)

        self.expand_channels_PET = encoder_block(in_channels, n_channels, stride = 1)
        self.conv_downsample1_PET = encoder_block(n_channels, n_channels * 2)
        self.conv_downsample2_PET = encoder_block(n_channels * 2, n_channels * 4)
        self.conv_downsample3_PET = encoder_block(n_channels * 4, n_channels * 8)
        self.conv_downsample4_PET = encoder_block(n_channels * 8, n_channels * 16)
        self.conv_downsample5_PET = encoder_block(n_channels * 16, channel_bound)

        self.conv_upsample1_PET = nn.ConvTranspose3d(channel_bound, n_channels * 16, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample2_PET = nn.ConvTranspose3d(n_channels * 16, n_channels * 8, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample3_PET= nn.ConvTranspose3d(n_channels * 8, n_channels * 4, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample4_PET= nn.ConvTranspose3d(n_channels * 4, n_channels * 2, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        self.conv_upsample5_PET= nn.ConvTranspose3d(n_channels * 2, n_channels, kernel_size = 3, stride = 2, padding = 1, output_padding = 1)
        
        self.decoder1_PET = encoder_block(n_channels * 1 * 2, n_channels, stride = 1)
        self.decoder2_PET = encoder_block(n_channels * 2 * 2, n_channels * 2, stride = 1)
        self.decoder3_PET = encoder_block(n_channels * 4 * 2, n_channels * 4, stride = 1)
        self.decoder4_PET = encoder_block(n_channels * 8 * 2, n_channels * 8, stride = 1)
        self.decoder5_PET = encoder_block(n_channels * 16 * 2, n_channels * 16, stride = 1)
        
        self.classifier1 = nn.Conv3d(n_channels, out_channels, kernel_size = 1)
        self.classifier2 = nn.Conv3d(n_channels * 2, out_channels, kernel_size = 1)
        self.classifier3 = nn.Conv3d(n_channels * 4, out_channels, kernel_size = 1)
        self.classifier4 = nn.Conv3d(n_channels * 8, out_channels, kernel_size = 1)
        self.classifier5 = nn.Conv3d(n_channels * 16, out_channels, kernel_size = 1)

        self.classifier_PET = nn.Conv3d(n_channels, 1, kernel_size = 1)

        self.upsample5 = nn.Upsample(scale_factor=16)
        self.upsample4 = nn.Upsample(scale_factor=8)
        self.upsample3 = nn.Upsample(scale_factor=4)
        self.upsample2 = nn.Upsample(scale_factor=2)


    def forward(self, CT, PET):
        PET = self.expand_channels_PET(PET)
        PET_downsample1 = self.conv_downsample1_PET(PET)
        PET_downsample2 = self.conv_downsample2_PET(PET_downsample1)
        PET_downsample3 = self.conv_downsample3_PET(PET_downsample2)
        PET_downsample4 = self.conv_downsample4_PET(PET_downsample3)
        PET_downsample5 = self.conv_downsample5_PET(PET_downsample4)

        PET_downsample5_up = self.conv_upsample1_PET(PET_downsample5)
        l5_output_PET = self.decoder5_PET(torch.cat((PET_downsample5_up, PET_downsample4), dim = 1))
        PET_downsample4_up = self.conv_upsample2_PET(l5_output_PET)
        l4_output_PET = self.decoder4_PET(torch.cat((PET_downsample4_up, PET_downsample3), dim = 1))
        PET_downsample3_up = self.conv_upsample3_PET(l4_output_PET)
        l3_output_PET = self.decoder3_PET(torch.cat((PET_downsample3_up, PET_downsample2), dim = 1))
        PET_downsample2_up = self.conv_upsample4_PET(l3_output_PET)
        l2_output_PET = self.decoder2_PET(torch.cat((PET_downsample2_up, PET_downsample1), dim = 1))
        PET_downsample1_up = self.conv_upsample5_PET(l2_output_PET)
        l1_output_PET = self.decoder1_PET(torch.cat((PET_downsample1_up, PET), dim = 1))
        spatial_attention_map = self.classifier_PET(l1_output_PET)

        spatial_attention_map_div2 = F.interpolate(spatial_attention_map, scale_factor = 0.5, mode ='trilinear')
        spatial_attention_map_div4 = F.interpolate(spatial_attention_map, scale_factor = 0.25, mode ='trilinear')
        spatial_attention_map_div8 = F.interpolate(spatial_attention_map, scale_factor = 0.125, mode ='trilinear')
        spatial_attention_map_div16 = F.interpolate(spatial_attention_map, scale_factor = 0.0625, mode ='trilinear')

        CT = self.expand_channels_CT(CT)
        CT_downsample1 = self.conv_downsample1_CT(CT)
        CT_downsample2 = self.conv_downsample2_CT(CT_downsample1)
        CT_downsample3 = self.conv_downsample3_CT(CT_downsample2)
        CT_downsample4 = self.conv_downsample4_CT(CT_downsample3)
        CT_downsample5 = self.conv_downsample5_CT(CT_downsample4)
        
        CT_downsample5_up = self.conv_upsample1_CT(CT_downsample5)
        l5_output_CT = self.decoder5_CT(torch.cat((CT_downsample5_up, CT_downsample4 * spatial_attention_map_div16), dim = 1))
        CT_downsample4_up = self.conv_upsample2_CT(CT_downsample4)
        l4_output_CT = self.decoder4_CT(torch.cat((CT_downsample4_up, CT_downsample3*spatial_attention_map_div8), dim = 1))
        CT_downsample3_up = self.conv_upsample3_CT(l4_output_CT)
        l3_output_CT = self.decoder3_CT(torch.cat((CT_downsample3_up, CT_downsample2*spatial_attention_map_div4), dim = 1))
        CT_downsample2_up = self.conv_upsample4_CT(l3_output_CT)
        l2_output_CT = self.decoder2_CT(torch.cat((CT_downsample2_up, CT_downsample1*spatial_attention_map_div2), dim = 1))
        CT_downsample1_up = self.conv_upsample5_CT(l2_output_CT)
        l1_output_CT = self.decoder1_CT(torch.cat((CT_downsample1_up, CT*spatial_attention_map), dim = 1))

        l1_output = self.classifier1(l1_output_CT * l1_output_PET)
        l2_output = self.upsample2(self.classifier2(l2_output_CT))
        l3_output = self.upsample3(self.classifier3(l3_output_CT))
        l4_output = self.upsample4(self.classifier4(l4_output_CT))
        l5_output = self.upsample5(self.classifier5(l5_output_CT))
        
        return [l1_output, l2_output, l3_output, l4_output, l5_output]


class MAIC_Dataset_Inference(Dataset):
    def __init__(self, path = None, normalizer = True, train = True, transform = Transform(*get_transform_params(None))):
        if path == None:
            path = '../mnt/dataset/'
        
        self.path = path
        self.file_list = []
        for f in os.listdir(path):
            if not 'py' in f:
                self.file_list.append(f)
        
        self.file_list = sorted(self.file_list)
        self.normalizer = normalizer
        self.train = train
        self.sampler = MAIC_Sampling(transform = transform, train = train)
        self.norm1 = Fixed_Normalizer(mean = 20.78, std = 180.50, min = -986, max = 271,  device = None)
        
    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        current_file = os.path.join(self.path, self.file_list[idx])
        hdf_file = h5py.File(current_file , 'r')
        CT = np.array(hdf_file['CT'])
        PET = np.array(hdf_file['PET'])
        spacing = np.array(hdf_file['Size'])
        images = np.stack((CT, PET))
        
        if self.train:
            seg = np.array(hdf_file['Aorta'])
        
        else:
            seg = None
        hdf_file.close()
        
        images, seg = self.sampler(images, seg)
        if self.normalizer:
            images[0] = self.norm1(images[0])
        
        return images[0], seg, spacing, images[1]