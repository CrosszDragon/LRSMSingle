# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 23:52
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : FunsionStyleHelper.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

from PyQt5.QtGui import QColor, QPalette
from CommonHelpers.CommonHelper import gray_from_rgb, bound
from CommonHelpers.Utils import dpi_scaled_from_float


def get_button_color(pal: QPalette) -> QColor:
    button_color = pal.button().color()
    val = gray_from_rgb(button_color.rgb())
    button_color = button_color.lighter(100 + max(1, (180 - val) / 6))
    button_color.setHsv(button_color.hue(), button_color.saturation() * 0.75, button_color.value())

    return button_color


def get_tab_frame_color(pal: QPalette):
    return get_button_color(pal).lighter(104)


def get_outline_color(pal: QPalette) -> QColor:
    return pal.window().color().darker(140)


def rounded_rect_radius():
    radius = dpi_scaled_from_float(2.0)
    return radius


def merged_colors(color1: QColor, color2: QColor, factor=50):
    """
    根据合并因子factor合并两个颜色color1和color2
    :param color1:
    :param color2:
    :param factor: color1的占比因子
    :return: 合并后的颜色
    """

    max_factor = 100
    temp = color1
    factor = bound(0, factor, max_factor)

    temp.setRed(temp.red() * factor / max_factor + color2.red() * (max_factor - factor) / max_factor)
    temp.setGreen(temp.green() * factor / max_factor + color2.green() * (max_factor - factor) / max_factor)
    temp.setBlue(temp.blue() * factor / max_factor + color2.blue() * (max_factor - factor) / max_factor)
    return temp
