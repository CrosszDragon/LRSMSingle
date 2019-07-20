# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 19:50
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MatToImg.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm


import numpy as np

m = []
for i in range(256):
    k = []
    for j in range(256):
        if j % 2 == 0:
            k.append(1)
        else:
            k.append(0)
    m.append(k)


def mat_to_img(m: list):
    ''' 传入一个二维01矩阵m，生成一张黑白图返回 '''
    img = np.zeros((len(m), len(m[0]), 3), np.uint8)  # 生成一张全黑色图，根据传入矩阵的len
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] == 0:
                img[i][j][:] = 0  # 赋值颜色为黑色
            else:
                img[i][j][:] = 255  # 赋值颜色为白色
    return img
