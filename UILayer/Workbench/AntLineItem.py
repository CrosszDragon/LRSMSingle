# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 19:40
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : AntLineItem.py
# @Project : pyqt5_project
# @Software: PyCharm

from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem
from PyQt5.QtGui import QVector2D, QPainter, QPen, QColor
from PyQt5.QtCore import Q_ENUMS, Qt, QTimer, pyqtSignal, QRectF, QPoint


class AntLineItem(QGraphicsItem):
    """"""

    def __init__(self, line_len=6., line_width=2, line_step=1.5, line_speed=100, line_color=Qt.black, parent=None):
        super(AntLineItem, self).__init__(parent)

        self._line_len = line_len
        self._line_width = line_width
        self._line_step = line_step
        self._line_speed = line_speed
        self._line_color = line_color

        # 线条的长度
        self._dashes = line_len
        # 空白长度
        self._spaces = line_len
        self._dash_pattern = [line_len] * 5
        self._timer = QTimer()

        self._timer.timeout.connect(self.update_value)
        self.stop = False
        # self._timer.start(self._line_speed)

    def update_value(self):
        """"""
        if self._dashes >= self._line_len and self._spaces >= self._line_len:
            self._dashes = self._spaces = 0.

        if self._dashes <= 0 and self._spaces < self._line_len:
            self._spaces += self._line_step
        elif self._dashes < self._line_len <= self._spaces:
            self._dashes += self._line_step

        self._dash_pattern[0] = self._dashes
        self._dash_pattern[1] = self._spaces
        # self.update(QRectF(0, 0, 202, 202))

    def get_pattern(self, src, dashes, spaces):
        if dashes >= self._line_len and spaces >= self._line_len:
            dashes = spaces = 0.

        if dashes <= 0 and spaces < self._line_len:
            spaces += self._line_step
        elif dashes < self._line_len <= spaces:
            dashes += self._line_step

        src[0] = dashes
        src[1] = spaces
        return src, dashes, spaces

    def boundingRect(self):
        return QRectF(1, 1, 200, 200).adjusted(-1, -1, 1, 1)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        """"""
        pen = QPen()
        pen.setWidthF(1)
        pen.setColor(self._line_color)
        pen.setDashPattern(self._dash_pattern)

        painter.setPen(pen)
        # painter.drawRect(QRectF(1, 1, 200, 200))

        # painter.fillRect(QRectF(0, 0, 500, 500), QColor(10, 123, 80))
        painter.drawLine(QPoint(10, 20), QPoint(100, 20))

        pattern = [4, 4, 4, 4]
        pen.setDashPattern(pattern)

        painter.setPen(pen)
        painter.drawLine(QPoint(10, 30), QPoint(200, 30))

        # pattern = [4, 4, 4, 4]
        # pen.setDashPattern(pattern)
        pen.setColor(Qt.white)
        painter.setPen(pen)
        painter.drawLine(QPoint(6, 30), QPoint(200, 30))
        # try:
        #     y = 20
        #     src_pa = list(self._dash_pattern)
        #     dash = self._dashes
        #     space = self._spaces
        #
        #     for i in range(1, 6):
        #         y1 = y + 10 * i
        #         src_pa, dash, space = self.get_pattern(src_pa, dash, space)
        #         pen.setDashPattern(src_pa)
        #         painter.setPen(pen)
        #         painter.drawLine(QPoint(10, y1), QPoint(100, y1))
        # except Exception as e:
        #     print(e)

    def __del__(self):
        self._timer.stop()


















