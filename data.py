from tarfile import DIRTYPE
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision
from torch import nn, optim
from torch.nn import functional as F
from torch.utils.data import TensorDataset, DataLoader
# from torch.utils.data.dataset import Dataset
from torch.utils.data import Dataset
import os 
from tqdm import tqdm
# from rectangle_builder import rectangle,test_img
import sys
# sys.path.append(r"C:\Users\aki\Documents\GitHub\deep\pytorch_test\snu")
# from model import snu_layer
# from model import network
from tqdm import tqdm
#from mp4_rec import record, rectangle_record
import pandas as pd
# import scipy.io
# from torchsummary import summary
import argparse
import h5py

class LoadDataset(Dataset):
    def __init__(self, dir, time = 100, width = 240, height = 180):
        self.dir = dir
        #h5ファイルのディレクトリのリスト
        self.dir_h5 = []
        self.width = width
        self.height = height
        self.time = time
        for _, _, files in os.walk(self.dir):
            for file in files:
                if file.endswith('.h5'):
                    self.dir_h5.append(os.path.join(self.dir, file)) 
        self.index = len(self.dir_h5)
        
    def __len__(self):
        return self.index

    def __getitem__(self, index):
        events = torch.zeros(2, self.time, self.width, self.height)
        label = torch.zeros(3)
        with h5py.File(self.dir_h5[index], "r") as f:
            self.label_ = f['truth'][()]
            self.label_ = self.label_[1:-1]
            self.label_ = self.label_.split(',')
            label[0]= float(self.label_[0])
            label[1] = float(self.label_[1])
            label[2] = float(self.label_[2])

            self.events_ = f['events'][()]
            for i in self.events_:
                events[ i[3], i[0], i[1], i[2]] = 1
        return events, label

if __name__ == "__main__":
    a = LoadDataset('C:/Users/oosim/Desktop/snn/v2e/output/')
    ru = a.__getitem__(2)
    print(ru)
    print(ru[0].shape)