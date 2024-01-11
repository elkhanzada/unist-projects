import numpy as np
import torch
import tqdm

from Prob2 import TimePredictor
import argparse
import os
from os.path import join
from torchvision.transforms.transforms import ToTensor, Compose, Resize, Normalize
import cv2
import json


def main():
    """
    This is main function that takes in a folder as an argument and runs the model on the images inside the given folder
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default=None, type=str)
    args = parser.parse_args()

    transforms = Compose([
        ToTensor(),
    ])
    if not args.folder:
        print("Provide an image folder path!")
    else:
        files = sorted(os.listdir(args.folder))
        model = TimePredictor()
        model.load_state_dict(torch.load("Prob3.pth", map_location='cpu'))
        model.to('cuda')
        results = {}
        for fl in tqdm.tqdm(files):
            img = cv2.imread(join(args.folder, fl))
            img = transforms(img)
            pred_h, pred_m = model(img[None].cuda())
            output_h = int(torch.round(pred_h.sigmoid() * 12).detach().cpu().item())
            output_m = int(torch.round(pred_m.sigmoid() * 60).detach().cpu().item())
            print(f"{fl}: Hour: {output_h}, Minute: {output_m}")
            results[fl] = f"{output_h}h {output_m}m"

        with open("results.json", "w") as f:
            json.dump(results, f)


if __name__ == '__main__':
    main()
