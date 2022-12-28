import os
import os.path as osp
import random
import numpy as np

from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as T


def random_split(data_dir, label_names, div_rate=8):
    image_fps = []
    label_idx = []
        
    for l_idx, l_name in enumerate(label_names):
        curr_label = l_idx
        dir_fp = osp.join(data_dir, l_name)
        for img_fp in sorted(os.listdir(dir_fp)):
            image_fps.append(osp.join(dir_fp, img_fp))
            label_idx.append(curr_label)
    
    num_total = len(image_fps)
    num_test = num_total // div_rate
    num_train = num_total - num_test

    all_indices = np.arange(len(image_fps))
    
    random.shuffle(all_indices)
    test_indices = all_indices[:num_test]
    train_indices = all_indices[num_test:]

    train_image_fps = [image_fps[idx] for idx in train_indices]
    train_label_idx = [label_idx[idx] for idx in train_indices]

    test_image_fps = [image_fps[idx] for idx in test_indices]
    test_label_idx = [label_idx[idx] for idx in test_indices]
    
    return train_image_fps, train_label_idx, test_image_fps, test_label_idx


class PokemonDataset(Dataset):
    def __init__(self, image_fps, label_idx, is_train):
        self.image_fps = image_fps
        self.label_idx = label_idx 
        self.is_train = is_train

        if self.is_train:
            self.transform = T.Compose([T.AutoAugment(), 
                                        T.ToTensor()])
        else:
            self.transform = T.ToTensor()

    def __len__(self):
        return len(self.image_fps)

    def __getitem__(self, idx):
        curr_image_fp = self.image_fps[idx]
        curr_label_idx = self.label_idx[idx]

        sample = dict()
        sample['img'] = self.transform(Image.open(curr_image_fp))
        sample['label'] = curr_label_idx

        return sample

def get_dataloader(data_dir, label_names, batch_size):
    train_image_fps, train_label_idx, test_image_fps, test_label_idx = random_split(data_dir, label_names)
    train_dataset = PokemonDataset(train_image_fps, train_label_idx, True)
    test_dataset = PokemonDataset(test_image_fps, test_label_idx, False)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader, train_dataset, test_dataset