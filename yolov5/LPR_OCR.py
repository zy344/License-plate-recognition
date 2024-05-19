# -*- coding: utf-8 -*-
# /usr/bin/env/python3

"""
simple lpr model.
Author: zy2770169045.
"""

from 洗车房车牌识别.LPRNet_Pytorch.data.load_data import CHARS
from torch.autograd import Variable
import numpy as np
import argparse
import torch
import time
import cv2


def get_parser():
    parser = argparse.ArgumentParser(description='parameters to train net')
    parser.add_argument('--img_size', default=(94, 24), help='the image size')
    parser.add_argument('--dropout_rate', default=0, help='dropout rate.')
    parser.add_argument('--lpr_max_len', default=8, help='license plate number max length.')
    parser.add_argument('--test_batch_size', default=100, help='testing batch size.')
    parser.add_argument('--phase_train', default=False, type=bool, help='train or test phase flag.')
    parser.add_argument('--num_workers', default=8, type=int, help='Number of workers used in dataloading')
    parser.add_argument('--cuda', default=True, type=bool, help='Use cuda to train model')
    parser.add_argument('--pretrained_model', default='../weights/车牌预训练.pth', help='pretrained base model')

    args = parser.parse_args()
    return args


def Greedy_Decode_Eval(Net, image, args):
    t1 = time.time()
    # load train data
    height, width, _ = image.shape
    if height != args.img_size[1] or width != args.img_size[0]:
        image = cv2.resize(image, args.img_size)
    image = transform(image)

    image = torch.tensor(image)
    image = image.unsqueeze(0)

    if args.cuda:
        image = Variable(image.cuda())
    else:
        image = Variable(image)

    # forward
    prebs = Net(image)
    # greedy decode
    prebs = prebs.cpu().detach().numpy()
    preb_labels = list()
    for i in range(prebs.shape[0]):
        preb = prebs[i, :, :]
        preb_label = list()
        for j in range(preb.shape[1]):
            preb_label.append(np.argmax(preb[:, j], axis=0))
        no_repeat_blank_label = list()
        pre_c = preb_label[0]
        if pre_c != len(CHARS) - 1:
            no_repeat_blank_label.append(pre_c)
        for c in preb_label:  # dropout repeate label and blank label
            if (pre_c == c) or (c == len(CHARS) - 1):
                if c == len(CHARS) - 1:
                    pre_c = c
                continue
            no_repeat_blank_label.append(c)
            pre_c = c
        preb_labels.append(no_repeat_blank_label)
    result = ''
    for label in preb_labels:
        lb = ''
        for i in label:
            lb += CHARS[i]
        result = lb

    t2 = time.time()
    print("[Info] OCR Speed: {}s".format(t2 - t1))
    return result


def transform(img):
    img = img.astype('float32')
    img -= 127.5
    img *= 0.0078125
    img = np.transpose(img, (2, 0, 1))
    return img

