# import cv2
# import numpy as np
# import torch
# from Algorithm.AIAlgorithm.model import ModernUNet
#
# # config
# MODEL_PARAMS = 'params.pth'
# IMAGE_PATH = r'D:/Level_16.tif'
# print(IMAGE_PATH)
# # load image
# image = cv2.imread(IMAGE_PATH)
#
# # create model
# net = ModernUNet()
#
# # initialization
# net.init(device='cpu', params=MODEL_PARAMS)
#
# mask = net.predict(image)
#
