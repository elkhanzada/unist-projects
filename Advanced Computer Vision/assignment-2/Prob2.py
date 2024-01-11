import torch.nn as nn
import torch.optim as optim
from torchvision.models import resnet18
from torch.utils.data import DataLoader, TensorDataset

# some initial imports
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn.functional as F

from tqdm import tqdm
from cl_dataset import ContinualMNIST as MNIST
from einops import rearrange
from model import Net
from utils import seed_everything, evaluate_task, train_task
import argparse

# * ----------------------- global setup ------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
seed_value = 42
seed_everything(seed_value)
parser = argparse.ArgumentParser()
parser.add_argument("--checkpoint", default=None, type=str)
args = parser.parse_args()
# * ----------------------- hyper params and mdoel ------------------------------
model = Net().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

NUM_EPOCH = 3
dataset = MNIST()

# If checkpoint is given, only test the model on tasks.
if args.checkpoint:
    model.adapt_last_layer(10)
    model.load_state_dict(torch.load(args.checkpoint))
    model.eval()
    print(f"\n -----------------------evaluation start-----------------------")
    accuracy = []
    seen_classes_list = []
    for task_i, (_, _, x_test, t_test) in enumerate(dataset.task_data):
        seen_classes = np.unique(t_test).tolist()
        seen_classes_list.extend(seen_classes)
        seen_classes_list = list(set(seen_classes_list))
        current_task_classes = np.unique(t_test).tolist()
        x_test = torch.tensor(x_test).float()
        t_test = torch.tensor(t_test).long()
        test_data = TensorDataset(x_test, t_test)
        test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

        acc = evaluate_task(model, test_loader, current_task_classes)
        accuracy.append(acc)
    avg_accuracy = sum(accuracy) / len(accuracy)
    print(f"seen classes : {seen_classes_list} \t seen classes acc : {avg_accuracy:.6f}")
    print(f"-" * 50, "\n")
else:
    # * ----------------------- task process ------------------------------
    seen_classes_list = []  # Renamed from accumulate
    for task_idx, (x_train_task, t_train_task, x_test_task, t_test_task) in enumerate(dataset.task_data):
        # Update seen_classes_list
        seen_classes = np.unique(t_train_task).tolist()
        seen_classes_list.extend(seen_classes)
        seen_classes_list = list(
            set(seen_classes_list))  # if use the replay method, for preventing ovelapping each classes

        # Adapt model's last layer
        model.adapt_last_layer(len(seen_classes_list))

        # Convert numpy arrays to PyTorch tensors and ensure they're on the correct device
        x_train_task = torch.tensor(x_train_task).float()
        t_train_task = torch.tensor(t_train_task).long()

        train_dataset = TensorDataset(x_train_task, t_train_task)
        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

        # if in the second task, disable all model parameters except last layer
        if task_idx == 1:
            for name, param in model.named_parameters():
                if 'fc2' not in name:
                    param.requires_grad = False

        # * ----------------------- train ------------------------------
        train_task(model, train_loader, optimizer, criterion, NUM_EPOCH)

        # save the model parameters
        if task_idx > 0:
            torch.save(model.state_dict(), "Prob2.pth")

        # * ----------------------- eval ------------------------------
        print(f"\n -----------------------evaluation start-----------------------")
        accuracy = []
        for task_i, (_, _, x_test, t_test) in enumerate(dataset.task_data):
            if task_i > task_idx:
                continue

            current_task_classes = np.unique(t_test).tolist()
            x_test = torch.tensor(x_test).float()
            t_test = torch.tensor(t_test).long()
            test_data = TensorDataset(x_test, t_test)
            test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

            acc = evaluate_task(model, test_loader, current_task_classes)
            accuracy.append(acc)
        avg_accuracy = sum(accuracy) / len(accuracy)
        print(f"seen classes : {seen_classes_list} \t seen classes acc : {avg_accuracy:.6f}")
        print(f"-" * 50, "\n")
