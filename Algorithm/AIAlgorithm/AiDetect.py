# -*- coding: utf-8 -*-
# @Time    : 2019/7/9 20:53
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : AiDetect.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

from sys import path
import cv2
import numpy as np
import torch
from Algorithm.AIAlgorithm.model import ModernUNet

# config
MODEL_PARAMS = 'C:/Users/h2958/Desktop/LSRMSingalVersion3/Algorithm/AIAlgorithm/params.pth'
IMAGE_PATH = r'D:/1.png'
print(IMAGE_PATH)
# load image
# image = cv2.imread(IMAGE_PATH)


def detect_one(image):
    # create model
    net = ModernUNet()

    # initialization
    net.init(device='cpu', params=MODEL_PARAMS)
    mask = net.predict(image)

    return mask


def detect_image(images):
    result = []

    for image in images:
        try:
            res = detect_one(image)
            result.append(res)
        except Exception as e:
            print("智能识别出错： ", e)

    return result


if __name__ == '__main__':
    image = cv2.imread(IMAGE_PATH)

    # create model
    net = ModernUNet()

    print(type(image))
    # initialization
    net.init(device='cpu', params=MODEL_PARAMS)

    # predict
    mask = net.predict(image)
    print(mask)
