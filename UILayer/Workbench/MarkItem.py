# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 18:44
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MarkItem.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent,QGraphicsItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform, QPainter
from UILayer.Workbench.BorderItem import BorderItem
from Document.MarkData import MarkItem as MakeData


class MarkItem(BorderItem):

    def __init__(self,  mark_data: MakeData, bound_path, position, scene, view_scale, shape=None, transform=QTransform(), parent=None):
        super(MarkItem, self).__init__(position, scene, view_scale, shape, transform, parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self._item_path = bound_path
        self._mark_data = mark_data

    def get_mark_data(self):
        return self._mark_data

    def set_mark_data(self, mark_data: MakeData):
        self._mark_data = mark_data

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.scene().clearSelection()
        self.setSelected(True)

    def shape(self):
        return self._mark_data.draw_path()

    def paint(self, painter: QPainter, option, widget=None) -> None:
        path = self._mark_data.draw_path()

        self._pen.setColor(Qt.white)
        self._pen.setStyle(Qt.SolidLine)
        painter.setPen(self._pen)
        painter.drawPath(path)
        # painter.drawRect(self._item_path.boundingRect())

        self._pen.setColor(self._mark_data.color)
        self._pen.setDashPattern(self._dash_pattern)
        painter.setPen(self._pen)
        painter.drawPath(path)
