# -*- coding: utf-8 -*-
"""ERA_Session6_Assignment_v3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XemiIDByNIQ5_6IwmC1Z4C5Qrjm9D18P
"""

# Google Colab specific code - commented out for local execution
# from google.colab import drive
# drive.mount('/content/drive')

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# Google Colab specific file copying commands - commented out for local execution
# !cp /content/drive/MyDrive/The\ School\ of\ AI/Session\ 6\ Assignment/model.py /content
# !cp /content/drive/MyDrive/The\ School\ of\ AI/Session\ 6\ Assignment/utils.py /content

#import model
#import utils
from model import Net
from utils import *
from tqdm import tqdm
from torchsummary import summary

import json
import matplotlib.pyplot as plt
import numpy as np

def save_model_metrics(test_acc, epoch, total_params):
    metrics = {
        "test_accuracy": float(test_acc),
        "best_epoch": int(epoch),
        "total_parameters": int(total_params)
    }
    with open('model_metrics.json', 'w') as f:
        json.dump(metrics, f)

def visualize_predictions(model, device, test_loader):
    model.eval()
    test_iter = iter(test_loader)
    images, labels = next(test_iter)
    
    fig = plt.figure(figsize=(12, 4))
    for idx in range(5):
        ax = fig.add_subplot(1, 5, idx+1)
        img = images[idx].numpy().squeeze()
        plt.imshow(img, cmap='gray')
        
        image = images[idx].unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(image)
            pred = output.argmax(dim=1)
            
        ax.set_title(f'Pred: {pred.item()}\nActual: {labels[idx].item()}')
        ax.axis('off')
    plt.show()

# Train data transformations
train_transforms = transforms.Compose([
    transforms.RandomApply([transforms.CenterCrop(22), ], p=0.1),
    transforms.Resize((28, 28)),
    transforms.RandomRotation((-15., 15.), fill=0),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
    ])

# Test data transformations
test_transforms = transforms.Compose([
    transforms.ToTensor(),
    #transforms.Normalize((0.1407,), (0.4081,)) --> This is incorrect line and hence commented
    transforms.Normalize((0.1307,), (0.3081,))
    ])

"""See how to get separate validations dataset"""

if __name__ == '__main__':
    train_data = datasets.MNIST('../data', train=True, download=True, transform=train_transforms)
    test_data = datasets.MNIST('../data', train=False, download=True, transform=test_transforms)

    batch_size = 128
    kwargs = {'batch_size': batch_size, 'shuffle': True, 'num_workers': 0, 'pin_memory': True}

    test_loader = torch.utils.data.DataLoader(test_data, **kwargs)
    train_loader = torch.utils.data.DataLoader(train_data, **kwargs)

    # Visualization code
    batch_data, batch_label = next(iter(train_loader))
    
    fig = plt.figure()
    for i in range(12):
        plt.subplot(3,4,i+1)
        plt.tight_layout()
        plt.imshow(batch_data[i].squeeze(0), cmap='gray')
        plt.title(batch_label[i].item())
        plt.xticks([])
        plt.yticks([])

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model = Net().to(device)
    total_params = sum(p.numel() for p in model.parameters())
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=15, gamma=0.1, verbose=True)
    criterion = nn.CrossEntropyLoss()
    num_epochs = 20
    best_acc = 0.0

    for epoch in range(1, num_epochs+1):
        print(f'Epoch {epoch}')
        train(model, device, train_loader, optimizer, criterion)
        test_acc = test(model, device, test_loader, criterion)
        scheduler.step()
        
        if test_acc >= 99.4:
            print(f"Target accuracy reached at epoch {epoch}!")
            torch.save(model.state_dict(), 'best_model.pt')
            save_model_metrics(test_acc, epoch, total_params)
            break
        elif test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), 'best_model.pt')

    # Visualize predictions
    visualize_predictions(model, device, test_loader)
    printTrainTest_LossAcc(train_losses, train_acc, test_losses, test_acc)