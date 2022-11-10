# -*- coding: utf-8 -*-
'''
This script performs transformation on images and dumps the output arrays as npzfiles, which saves time for training.
'''

import argparse
import os
import torch
from PIL import Image
import base64
from io import BytesIO
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize, RandomResizedCrop
from tqdm import tqdm
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="../Multimodal_Retrieval/", help="the directory which stores the image tsvfiles")
    parser.add_argument("--image_resolution", type=int, default=224, help="the resolution of transformed images, default to 224*224")
    return parser.parse_args()

def _convert_to_rgb(image):
    return image.convert('RGB')

def build_transform(resolution):
    normalize = Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
    return Compose([
            Resize(resolution, interpolation=Image.BICUBIC),
            CenterCrop(resolution),
            _convert_to_rgb,
            ToTensor(),
            normalize,
        ])

if __name__ == "__main__":
    args = parse_args()
    transform = build_transform(args.image_resolution)
    train_path = os.path.join(args.data_dir, "MR_train_imgs.tsv")
    val_path = os.path.join(args.data_dir, "MR_valid_imgs.tsv")
    test_path = os.path.join(args.data_dir, "MR_test_imgs.tsv")
    #for path, split in zip((train_path, val_path, test_path), ("train", "valid", "test")):
    for path, split in zip((val_path, test_path), ("valid", "test")):
        assert os.path.exists(path), "the {} filepath {} not exists!".format(split, path)
        if not os.path.exists('/data/nxy/Multimodal_Retrieval/'+split):
            os.makedirs('/data/nxy/Multimodal_Retrieval/'+split)
        print("begin to transform {} split".format(split))
        num = 0
        with open(path, "r") as fin:
            for line in tqdm(fin):
                img_id, b64 = line.strip().split("\t")
                image = Image.open(BytesIO(base64.urlsafe_b64decode(b64)))
                image_array = transform(image).numpy()
                output_path = "/data/nxy/Multimodal_Retrieval/{}/{}.npy".format(split, img_id)
                np.save(output_path, image_array)
                num += 1
        print("finished transforming {} images for {} split, the output is saved at {}".format(num, split, '/data/nxy/Multimodal_Retrieval/'+split))
    print("done!")