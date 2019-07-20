# -*- coding: utf-8 -*-
# @Time    : 2019/7/20 16:21
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : ColorButton.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtWidgets import QToolButton, QStyle, QColorDialog
from PyQt5.QtGui import QColor, QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QSize


class ColorButton(QToolButton):
    """
    A tool button for letting the user pick a color. When clicked it shows a
    color dialog and it has an icon to represent the currently chosen color
    """

    color_changed_signal = pyqtSignal(QColor)

    def __init__(self, parent=None):
        QToolButton.__init__(self, parent)

        default_icon_size = self.style().pixelMetric(QStyle.PM_ButtonIconSize)
        self.setIconSize(QSize(default_icon_size * 2, default_icon_size))

        self._color = QColor()
        self.color = QColor(Qt.white)

        self.clicked.connect(self._pick_color)

    @property
    def color(self) -> QColor:
        return self._color

    @color.setter
    def color(self, new_color: QColor):
        if self._color == new_color:
            return
        self._color = new_color
        self._update_icon()
        self.color_changed_signal.emit(new_color)

    def changeEvent(self, event: QEvent):
        QToolButton.changeEvent(self, event)

        if event.type() == QEvent.StyleChange:
            default_icon_size = self.style().pixelMetric(QStyle.PM_ButtonIconSize)
            self.setIconSize(QSize(default_icon_size * 2, default_icon_size))
            # self._update_icon()

    def _pick_color(self):
        new_color = QColorDialog.getColor(self._color, self)
        if isinstance(new_color, QColor) and new_color.isValid():
            self.color = new_color

    def _update_icon(self):
        icon_size = QSize(self.iconSize())
        icon_size.setWidth(icon_size.width() - 2)
        icon_size.setHeight(icon_size.height() - 2)

        pix_map = QPixmap(icon_size)
        pix_map.fill(self._color)

        painter = QPainter()
        painter.begin(pix_map)
        border_color = QColor(Qt.black)
        border_color.setAlpha(128)
        painter.setPen(border_color)
        painter.drawRect(0, 0, pix_map.width() - 1, pix_map.height() - 1)
        painter.end()

        self.setIcon(QIcon(pix_map))
