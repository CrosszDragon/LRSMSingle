# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 20:21
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : GridItem.py
# @Project : pyqt5_project
# @Software: PyCharm

from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem
from PyQt5.QtCore import QRect, QRectF, Qt, QPoint
from PyQt5.QtGui import QBrush, QPen, QPainter, QColor

from CONST.CONST import PEN_STANDARD_WIDTH
from CommonHelper.CommonHelper import adjust_pen_width


class GridItem(QGraphicsItem):

    def __init__(self, rect: QRect = QRect(), parent=None):
        super(GridItem, self).__init__(parent)
        self._rect = rect

        self._pen = QPen()
        self._pen.setWidthF(PEN_STANDARD_WIDTH)

        self._is_show = True

        self.setPos(QPoint(0, 0))

    def toggle_show(self):
        self._is_show = not self._is_show
        self.update(self.boundingRect())

    def is_show(self, is_show: bool):
        self._is_show = is_show
        self.update(self.boundingRect())

    def set_rect(self, rect: QRect):
        self._rect = rect
        self.update(self.boundingRect())

    def set_pen_width(self, width: [int, float]):
        """"""
        # pen_width = adjust_pen_width(PEN_STANDARD_WIDTH, width)
        # self._pen.setWidthF(pen_width)
        # self.update(self.boundingRect())
        # print("pwn width: ", pen_width)

    def boundingRect(self) -> QRectF:
        return QRectF(self._rect.adjusted(0, 0, 2, 2))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None) -> None:
        """"""
        if self._is_show:
            brush = QBrush(QColor(220, 220, 220), Qt.CrossPattern)
            self._pen.setBrush(brush)
            Qt.BrushStyle
            painter.setPen(self._pen)
            # painter.setBrush(brush)
            painter.drawRect(self._rect)
