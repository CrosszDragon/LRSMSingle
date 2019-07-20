# -*- coding: utf-8 -*-
# @Time    : 2019/7/20 12:58
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Utils.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtGui import QGuiApplication

scale = 1.0
default_dpi_scale = 1.0
def_dpi_scale = lambda: QGuiApplication.primaryScreen().logicalDotsPerInchX() / 96.0 \
    if QGuiApplication.primaryScreen() else 1.0


def get_default_dpi_scale():
    global default_dpi_scale
    default_dpi_scale = def_dpi_scale()
    return default_dpi_scale


def dpi_scaled_from_float(value: float):
    global scale
    scale = get_default_dpi_scale()
    return scale * value
