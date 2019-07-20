# --coding:utf-8--
"""常用函数模块

包含了加载大图片时可能会用到的两个函数，第一个用于根据切片大小以及
原图分辨率（宽高）大小生成切片对应于原图的位置的矩形边框的矩形集

第二个函数用于传入两个图片，将两个图片拼接起来返回
"""
import numpy as np
from PIL import Image
import cv2
import openslide
from PyQt5.QtCore import QFileInfo


def cv_read(path):
    cv_img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    return cv_img


def slice_rect(slide_w, slide_h, tile_size):
    '''
    传入一个level总像素以及一个tile的size,返回一个铺满level的tile_rec的list
    '''
    tiles_rects = []
    x, y = (0, 0)
    x_size, y_size = slide_w, slide_h  # level size
    x_step, y_step = tile_size  # tile size
    while y < y_size:
        while x < x_size:  # 控制在level的size中
            '''
            就是算出铺满level图像需要的所有tile，append到tiles_recs中
            '''
            w = x_step
            if x + w >= x_size:  # w+tile_x > level_x此层level宽
                w = x_size - x
            h = y_step
            if y + h >= y_size:
                h = y_size - y
            tiles_rects.append((x, y, w, h))  # 以行为主，为铺满level所需要的所有tile声明一个rect
            x += x_step
        x = 0
        y += y_step
    return tiles_rects


def joint_two_image(png1: Image, png2: Image, flag='horizontal'):
    '''传入两张图片，拼接起来返回'''
    img1, img2 = png1, png2
    size1, size2 = img1.size, img2.size
    if flag == 'horizontal':

        joint = Image.new('RGB', (size1[0] + size2[0], size1[1]))
        loc1, loc2 = (0, 0), (size1[0], 0)
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        return joint
    elif flag == 'vertical':
        joint = Image.new('RGB', (size1[0], size1[1] + size2[1]))
        loc1, loc2 = (0, 0), (0, size1[1])
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        return joint


def is_img_big(path):
    '''判断一副图像是否是大图 分界 <=200M'''

    file_info = QFileInfo(path)
    file_m_size = file_info.size() / 1024 / 1024
    if file_m_size > 200:  # 大于2G
        return True
    else:
        return False


def is_img_so_big(path):
    '''判断图片是否大于2G'''
    file_info = QFileInfo(path)
    file_g_size = file_info.size() / 1024 / 1024 / 1024
    if file_g_size >= 2:  # 大于2G
        return True
    else:
        return False
