# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 20:22
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : LrsmProxyStyle.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtWidgets import QProxyStyle, QStyle, QStyleOption, QStyleOptionComplex, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QSize, QLibrary, QLibraryInfo

from WindowStyle.FunsionStyleHelper import *


class LRSMProxyStyle(QProxyStyle):
    """
    自定义的窗口风格 继承于QProxy
    使用代理模式以便可以在运行时动态的改变窗口样式
    """

    def __init__(self, palette: QPalette, style: QStyle = None):
        super(LRSMProxyStyle, self).__init__(style)

        self._palette = palette
        self._is_dark = palette.window().color().value() <= 128
        self._dock_close_icon_path = ":/dock-close.png"
        self._dock_restore_icon_path = ":/dock-restore.png"

        self.setObjectName("lrsm")

    def set_palette(self, palette: QPalette):
        self._palette = palette
        self._is_dark = palette.window().color().value() <= 128

    def is_dark(self) -> bool:
        return self._is_dark

    def drawPrimitive(self, element, style_option: QStyleOption, painter: QPainter, widget=None):
        if element == QStyle.PE_FrameGroupBox:
            top_margin = max(self.pixelMetric(QStyle.PM_ExclusiveIndicatorHeight),
                             style_option.fontMetrics.height()) + 3

            frame_rect = style_option.rect.adjusted(0, top_margin, -1, -1)
            tab_frame_color = get_tab_frame_color(style_option.palette)

            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.translate(0.5, 0.5)
            painter.setPen(merged_colors(get_outline_color(style_option.palette), tab_frame_color))
            painter.setBrush(merged_colors(style_option.palette.window().color(), tab_frame_color))
            painter.drawRoundedRect(frame_rect, rounded_rect_radius(), rounded_rect_radius())
            painter.restore()
        else:
            QProxyStyle.drawPrimitive(self, element, style_option, painter, widget)

    def drawControl(self, element, style_option: QStyleOption, painter: QPainter, widget=None):
        """TODO"""
        QProxyStyle.drawControl(self, element, style_option, painter, widget)

    def drawComplexControl(self, element, style_option: QStyleOptionComplex, painter: QPainter, widget=None):
        """TODO"""
        QProxyStyle.drawComplexControl(self, element, style_option, painter, widget)

    def pixelMetric(self, metric, style_option: QStyleOption = None, widget=None) -> int:
        """TODO"""
        return QProxyStyle.pixelMetric(self, metric, style_option, widget)

    def sizeFromContents(self, contents_type, style_option: QStyleOption, size: QSize, widget: QWidget) -> QSize:
        """TODO"""
        return QProxyStyle.sizeFromContents(self, contents_type, style_option, size, widget)

    def subElementRect(self, sub_element, style_option: QStyleOption, widget: QWidget):
        """TODO"""
        return QProxyStyle.subElementRect(self, sub_element, style_option, widget)

    def styleHint(self, style_hint, style_option: QStyleOption = None, widget=None, return_data=None) -> int:
        """TODO"""
        return QProxyStyle.styleHint(self, style_hint, style_option, widget, return_data)

    def standardIcon(self, standard_icon, style_option: QStyleOption = None, widget=None):
        """TODO"""
        return QProxyStyle.standardIcon(self, standard_icon, style_option, widget)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QWidget, QApplication

    app = QApplication(sys.argv)
    frame = QWidget()
    frame.setWindowTitle("test")

    option = QStyleOption()
    option.initFrom(frame)
    print(option.fontMetrics.height())

    frame.show()
    sys.exit(app.exec_())
