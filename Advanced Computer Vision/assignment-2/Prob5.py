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


def train_joint_task(model, old_outputs, data_loader, optimizer, criterion, num_epochs=10, task_id=0):
    """
    Trains the model using LwF (Learning without Forgetting) approach

    :param model: current model
    :param old_outputs: recorded outputs from the old model on current task data
    :param data_loader: current task data loader
    :param optimizer: optimizer for model
    :param criterion: loss for the current model
    :param num_epochs: number of epochs
    :param task_id: to check whether we are in the first or second task
    :return: None
    """
    model.train()
    for epoch in range(num_epochs):
        total_loss = 0.0
        correct = 0
        total = 0

        # Use tqdm for a progress bar
        loop = tqdm(data_loader, total=len(data_loader), leave=True)
        if task_id == 0:
            for (images, labels), index in loop:
                images, labels = images.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                # Update tqdm progress bar
                loop.set_description(f"Epoch [{epoch + 1}/{num_epochs}]")
                loop.set_postfix(loss=loss.item(), acc=100 * correct / total)
        else:
            temperature = 2
            # parameter to control loss influence between new and old task
            lmb = 0.005
            for (images, labels), index in loop:
                images, labels = images.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = model(images)
                # extract the recorded outputs from the old task using the indices
                outputs_old = old_outputs[index]
                # perform cross entropy loss for new task
                loss1 = criterion(outputs, labels)
                # convert outputs to respective probabilities for current and old outputs
                softmax = F.softmax(outputs[:, :outputs_old.shape[1]], dim=1)
                softmax_old = F.softmax(outputs_old, dim=1)
                softmax = F.softmax(softmax ** (1 / temperature), dim=1)
                softmax_old = F.softmax(softmax_old ** (1 / temperature), dim=1)
                # perform loss for the old task
                loss2 = softmax_old.mul(-1 * torch.log(softmax))
                loss2 = loss2.sum(1).mean()
                # multiply by their respective weights and sum
                loss = loss1 * lmb + loss2 * (1 - lmb)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                # Update tqdm progress bar
                loop.set_description(f"Epoch [{epoch + 1}/{num_epochs}]")
                loop.set_postfix(loss=loss.item(), acc=100 * correct / total)

        avg_loss = total_loss / len(data_loader)
        accuracy = 100 * correct / total
        print(f"Epoch [{epoch + 1}/{num_epochs}] training - Avg Loss: {avg_loss:.6f}, Accuracy: {accuracy:.6f}%")


# Modified Tensor Dataset that returns indices as well.
class ModTensorDataset(TensorDataset):
    def __getitem__(self, index):
        return tuple(tensor[index] for tensor in self.tensors), index


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

        # Convert numpy arrays to PyTorch tensors and ensure they're on the correct device
        x_train_task = torch.tensor(x_train_task).float()
        t_train_task = torch.tensor(t_train_task).long()

        train_dataset = ModTensorDataset(x_train_task, t_train_task)
        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
        outputs_old = []
        # if second task, extract the outputs by running the old model on new task data
        if task_idx == 1:
            test_loader = DataLoader(train_dataset, batch_size=1, shuffle=False)
            loop = tqdm(test_loader, total=len(test_loader), leave=True)
            with torch.no_grad():
                for (images, labels), index in loop:
                    images, labels = images.to(device), labels.to(device)
                    optimizer.zero_grad()
                    outputs = model(images)
                    outputs_old.append(outputs.flatten())
            outputs_old = torch.stack(outputs_old)
        # * ----------------------- train ------------------------------
        # Adapt model's last layer
        model.adapt_last_layer(len(seen_classes_list))
        train_joint_task(model, outputs_old, train_loader, optimizer, criterion, NUM_EPOCH, task_idx)
        # save the model parameters
        if task_idx > 0:
            torch.save(model.state_dict(), "Prob5.pth")
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
