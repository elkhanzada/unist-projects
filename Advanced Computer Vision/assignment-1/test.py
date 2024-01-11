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
from PIL import Image
import shutil

if __name__ == '__main__':
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
        with open("sayem/test.json", "r") as f:
            sayem = json.load(f)
        acc = 0
        for fl in tqdm.tqdm(files):
            img = cv2.imread(join(args.folder, fl))
            img = transforms(img)
            pred_h, pred_m = model(img[None].cuda())
            # hour, minute = int(fl.split("_")[1]), int(fl.split("_")[2].split(".")[0])
            # gt = [hour, minute]
            gt = sayem[join('test', fl)]
            # output_h = pred_h.argmax(-1).detach().cpu().item()
            # output_m = pred_m.argmax(-1).detach().cpu().item()
            output_h = int(torch.round(pred_h.sigmoid() * 12).detach().cpu().item())
            output_m = int(torch.round(pred_m.sigmoid() * 60).detach().cpu().item())
            # print(f"{fl}: Hour: {output_h}, Minute: {output_m}")
            # results[fl] = f"{output_h}h {output_m}m"
            # if output_h == 0:
            #     output_h = 12
            result = output_h == gt[0] and (output_m >= gt[1] - 5 and output_m <= gt[1] + 5)
            if not result:
                print(fl)
                # shutil.copy(join(args.folder, fl), join("wrong_cases", f"{fl}_{output_h}_{output_m}"))
            acc += int(output_h == gt[0] and (output_m >= gt[1] - 5 and output_m <= gt[1] + 5))
        print(acc / len(files))
        # with open("results.json", "w") as f:
        #     json.dump(results, f)
