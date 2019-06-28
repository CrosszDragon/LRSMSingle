# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 21:57
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Selection.py
# @Project : LRSMSingleVersion
# @Software: PyCharm

from PyQt5.QtCore import QRect
from CONST.CONST import *
from ModelLayer.AbstractMarkItem import AbstractMarkItem


class Selection(object):
    """ 描述 """
    __name_count_num = counter(1)

    def __init__(self, rect: QRect = QRect(), shape=OptionTool.RECT_QUICK_SELECT_TOOL, name=None):
        self._rect = rect
        self._shape = shape
        self._name = None
        self._has_bind_to = []
        self.set_name(name)

    def get_rect(self):
        return self._rect

    def set_rect(self, rect: QRect):
        self._rect = rect

    def set_size(self, width, height):
        self._rect.setWidth(width)
        self._rect.setHeight(height)

    def get_shape(self):
        return self._shape

    def get_name(self):
        return self._name

    def set_name(self, name=None):
        if self._name is None:
            num = next(Selection.__name_count_num)
            name = "新建选区" + str(num)
        self._name = name

    def bind_to(self, mark_item: AbstractMarkItem):
        pass

    def unbind_to(self, mark_item: AbstractMarkItem):
        pass
