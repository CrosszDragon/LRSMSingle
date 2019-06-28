# -*- coding: utf-8 -*-
# @Time    : 2019/6/13 22:22
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : ImageItem.py
# @Project : pyqt5_project
# @Software: PyCharm

from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from CONST.CONST import *
from CommonHelper.CommonHelper import *
from ModelLayer.Selection import Selection


class ImageItem(QGraphicsItem):

    def __init__(self, image_data: QImage, pixel_width=None, parent=None):
        super(ImageItem, self).__init__(parent)
        self._image_data = image_data
        self._rect = QRect(0, 0, 300, 300)
        self._rect = QRect(0, 0, self._image_data.width(), self._image_data.height())

        self._pixel_width = pixel_width if pixel_width else 1
        self._pan = QPen()
        self._pan.setWidth(1)

        self.setTransform(QTransform())

    def set_image_data(self, image_data: QPixmap):
        self._image_data = image_data

    def boundingRect(self):
        return QRectF(self._rect.adjusted(-1, -1, 1, 1))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None) -> None:
        for y in range(self._image_data.height()):
            for x in range(self._image_data.width()):
                pixel_color = self._image_data.pixelColor(x, y)
                x_pos = x * self._pixel_width
                y_pos = y * self._pixel_width
                painter.fillRect(QRect(x_pos, y_pos, self._pixel_width, self._pixel_width), pixel_color)
