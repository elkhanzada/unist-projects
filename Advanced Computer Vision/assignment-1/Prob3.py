import glob

import torch.optim
import tqdm

from Prob2 import TimePredictor
from Prob1 import draw_clock
from torch.utils.data import Dataset
from torchvision.transforms.transforms import Compose, ToTensor, Resize, Normalize
import cv2
import argparse


class TimeDataset(Dataset):
    """
    Our dataset class accepts the number of images, transform, mode.
    """

    def __init__(self, num_of_images, transform=None, mode='train'):
        super(TimeDataset, self).__init__()
        self.mode = mode
        self.transform = transform

        # With this, we make sure that dataset contains every possible scenario during training.
        possible_scenarios = []
        for i in range(1, 13):
            for j in range(60):
                possible_scenarios.append([i, j])
        if mode == 'train':
            self.dataset = []
            for i in range(num_of_images):
                self.dataset.extend(possible_scenarios)
        else:
            # During testing, we simply use generated images.
            files = glob.glob("validation_dataset/*.png")
            self.dataset = files

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        # If in train, we generate the image once requested by calling our clock generation function and pass to the model
        if self.mode == 'train':
            hour, minute = self.dataset[item]
            img = draw_clock(hour, minute, add_noise=True if self.mode == 'train' else False)
            # hour /= 12
            # minute /= 60
        else:
            img = cv2.imread(self.dataset[item])
            file_name = self.dataset[item].split("/")[-1]
            hour, minute = int(file_name.split("_")[1]), int(file_name.split("_")[2].split(".")[0])
        if self.transform:
            img = self.transform(img)
        return img, (hour, minute)


def train_one_epoch(data, model, criterion, optimizer):
    """
    We train our model for one epoch. When performing the loss we unnormalize our sigmoid values. This is proven to be better at accuracy.
    """
    model.train()
    count = 0
    for img, label in tqdm.tqdm(data):
        img = img.cuda()
        pred_h, pred_m = model(img)
        gt_h, gt_m = label
        loss = criterion(pred_h.sigmoid().flatten() * 12, gt_h.type(torch.float32).cuda()) + criterion(
            pred_m.sigmoid().flatten() * 60, gt_m.type(torch.float32).cuda())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        count += 1
    return loss.detach().cpu().item()


def test_model(data, model):
    """
    When testing, we unnormalize and round our predictions. We do not apply margin when checking the accuracy of our model.
    """
    model.eval()
    total_acc = 0
    for img, label in tqdm.tqdm(data):
        pred_h, pred_m = model(img.cuda())
        gt_h, gt_m = label
        # check_h = pred_h.softmax(-1).argmax(-1) == gt_h.cuda()
        # check_m = pred_m.softmax(-1).argmax(-1) == gt_m.cuda()
        check_h = torch.round(pred_h.sigmoid() * 12)
        check_m = torch.round(pred_m.sigmoid() * 60)
        acc = torch.sum((check_h.flatten() == gt_h.cuda()) * (check_m.flatten() == gt_m.cuda()))
        total_acc += acc.detach().cpu().item()

    return total_acc / len(data.dataset)


def train(model):
    """
    This is main function for train. We initialize dataset, optimizer, criterion.
    """
    num_of_images = 15
    val_images = 5
    train_transform = Compose([
        ToTensor(),

    ])
    val_transform = Compose([
        ToTensor(),
    ])
    val_data = TimeDataset(val_images, val_transform, mode='val')
    val_data_loader = torch.utils.data.DataLoader(val_data, batch_size=16)
    train_data = TimeDataset(num_of_images, train_transform)
    train_data_loader = torch.utils.data.DataLoader(train_data, batch_size=8, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-5)
    criterion = torch.nn.L1Loss(reduction='sum')
    num_epochs = 100
    best_acc = -1
    for i in range(1, num_epochs):
        loss = train_one_epoch(train_data_loader, model, criterion, optimizer)
        print("Epoch loss", loss)
        if i % 1 == 0:
            acc = test_model(val_data_loader, model)
            if best_acc < acc:
                best_acc = acc
                print("Best accuracy: ", best_acc)
                torch.save(model.state_dict(), f"weights/best_model_{i}.pth")
            else:
                print("Current accuracy: ", acc)
                print("Current best accuracy: ", best_acc)


def test(model):
    """
    This is main function for test. We initialize our validation dataset and perform testing.
    """
    val_images = 10
    val_transform = Compose([
        ToTensor()
    ])
    val_data = TimeDataset(val_images, val_transform, mode='val')
    val_data_loader = torch.utils.data.DataLoader(val_data, batch_size=16)
    print(test_model(val_data_loader, model))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default=None)
    args = parser.parse_args()
    time_model = TimePredictor()
    if args.checkpoint:
        checkpoint = torch.load(args.checkpoint, map_location='cpu')
        time_model.load_state_dict(checkpoint)
    time_model.to('cuda')
    train(time_model)
