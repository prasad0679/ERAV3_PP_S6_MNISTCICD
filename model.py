# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17GAZA2GkGwtJuNWlItXOPDjp2T2IZTUY
"""

# Google Colab specific code - commented out for local execution
# from google.colab import drive
# drive.mount('/content/drive')

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# Check CUDA availability
cuda = torch.cuda.is_available()
print("CUDA Available?", cuda)

class Net(nn.Module):
    #This defines the structure of the NN.
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 128, 3, padding=1), 
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.Dropout(0.1)
        ) # 28*28*128
        
        self.trans1 = nn.Sequential(
            nn.Conv2d(128, 8, 1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(8),
            nn.Dropout(0.1)
        ) # 30*30*8

        self.conv2 = nn.Sequential(
            nn.Conv2d(8, 16, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.Dropout(0.1),
            nn.MaxPool2d(2, 2)            
        ) # 30*30*16 | 15*15*16
        
        self.conv3 = nn.Sequential(
            nn.Conv2d(16, 16, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.Dropout(0.1)
        ) # 15*15*16

        self.conv4 = nn.Sequential(
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Dropout(0.1),
            nn.MaxPool2d(2, 2)            
        ) # 15*15*32 | 7*7*32

        self.trans2 = nn.Sequential(
            nn.Conv2d(32, 16, 1, padding=1)
        ) # 9*9*32

        self.conv5 = nn.Sequential(
            nn.Conv2d(16, 16, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.Dropout(0.1)            
        ) # 9**9*16

        self.conv6 = nn.Sequential(
            nn.Conv2d(16, 32, 3, padding=1), # 1*1
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Dropout(0.1)            
        ) # 9*9*32

        self.conv7 = nn.Sequential(
            nn.Conv2d(32, 10, 1, padding=1),
            nn.AvgPool2d(kernel_size=7)            
        ) # 11*11*10 | 1*1*10
        
    def forward(self, x):
      x = self.conv1(x)
      #print("size after 1st layer: " ,x.shape)
      x = self.trans1(x)
      x = self.conv2(x)
      #print("size after 2nd layer: " ,x.shape)
      x = self.conv3(x)
      #print("size after 3rd layer: " ,x.shape)
      x = self.conv4(x)
      x = self.trans2(x)
      x = self.conv5(x)
      x = self.conv6(x)
      x = self.conv7(x)
      #print("size after 4th layer: " ,x.shape)
      x = x.view(x.size(0), -1)
      #print("size after flattening: " ,x.shape)
      x = F.log_softmax(x, dim=1)
      return x