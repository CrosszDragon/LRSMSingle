# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 20:18
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : StyleHelper.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QPixmapCache, QPalette, QColor

from WindowStyle.Preferences import Preferences, ApplicationStyle
from WindowStyle.LrsmProxyStyle import LRSMProxyStyle
from CommonHelpers.CommonHelper import bound


class StyleHelper(QObject):
    """ 窗口样式设置类 单例模式"""

    style_applied_signal = pyqtSignal()

    _instance = None

    def __init__(self):
        if StyleHelper._instance is None:
            QObject.__init__(self, None)

            self._default_style = QApplication.style().objectName()
            self._default_palette = QApplication.palette()
            self._apply()

            preferences = Preferences.instance()
            preferences.application_style_changed_signal.connect(self._apply)
            preferences.base_color_changed_signal.connect(self._apply)
            preferences.selection_color_changed_signal.connect(self._apply)

            StyleHelper._instance = self
        else:
            raise SyntaxError("StyleHelper是单例类, 请通过静态函数instance获取其实例")

    @staticmethod
    def instance():
        if StyleHelper._instance is None:
            StyleHelper._instance = StyleHelper()
        return StyleHelper._instance

    def default_style(self) -> str:
        return self._default_style

    def default_palette(self) -> QPalette:
        return self._default_palette

    def _apply(self):
        """使用当前的style"""
        preferences = Preferences.instance()

        application_style = preferences.application_style()
        if application_style == ApplicationStyle.FusionStyle:
            desired_style = "fusion"
            desired_palette = create_palette(preferences.base_color(), preferences.selection_color())
        elif application_style == ApplicationStyle.LRSMStyle:
            desired_style = "lsrm"
            desired_palette = create_palette(preferences.base_color(), preferences.selection_color())
        else:
            desired_style = self.default_style()
            desired_palette = self.default_palette()

        if QApplication.style().objectName() != desired_style:
            if desired_style == "lsrm":
                style = QStyleFactory.create("fusion")
                style = LRSMProxyStyle(desired_palette, style)
            else:
                style = QStyleFactory.create(desired_style)

            QApplication.setStyle(style)

        if QApplication.palette() != desired_palette:
            QPixmapCache.clear()
            QApplication.setPalette(desired_palette)

            style = QApplication.style()
            if isinstance(style, LRSMProxyStyle):
                style.set_palette(desired_palette)

            self.style_applied_signal.emit()


def create_palette(window_color: QColor, highlight_color: QColor) -> QPalette:
    """
    根据窗口样式window_color 和 高亮(选中)颜色创建窗口风格的palette
    :param window_color: 目标窗口样式
    :param highlight_color: 目标高亮样式
    :return: QPalette
    """

    # 根据HSV样式模型，获取该颜色的 hue色调 sat饱和度 和value明度(最后一个是透明度)
    hue, sat, window_value, _ = window_color.getHsv()

    color_from_value = lambda value: QColor.fromHsv(hue, sat, bound(0, value, 255))

    is_light = window_value > 128
    base_value = window_value + 48 if is_light else window_value - 24

    light_text_value = min(255, window_value + 160)
    dark_text_value = max(0, window_value - 160)

    # 根据界面的元素设置字体颜色以便以后可以看清字体
    light_text_color = QColor(light_text_value, light_text_value, light_text_value)
    dark_text_color = QColor(dark_text_value, dark_text_value, dark_text_value)
    light_disabled_text_color = QColor(light_text_value, light_text_value, light_text_value)
    dark_disabled_text_color = QColor(dark_text_value, dark_text_value, dark_text_value)

    palette = QPalette(color_from_value(window_value))
    palette.setColor(QPalette.Base, color_from_value(base_value))
    palette.setColor(QPalette.AlternateBase, color_from_value(base_value - 10))
    palette.setColor(QPalette.WindowText, dark_text_color if is_light else light_text_color)
    palette.setColor(QPalette.ButtonText, dark_text_color if is_light else light_text_color)
    palette.setColor(QPalette.Text, dark_text_color if is_light else light_text_color)
    palette.setColor(QPalette.Light, color_from_value(window_value + 55))
    palette.setColor(QPalette.Dark, color_from_value(window_value - 55))
    palette.setColor(QPalette.Mid, color_from_value(window_value - 27))
    palette.setColor(QPalette.Midlight, color_from_value(window_value + 27))

    # 按组设置颜色
    palette.setColor(QPalette.Disabled, QPalette.WindowText,
                     dark_disabled_text_color if is_light else light_disabled_text_color)
    palette.setColor(QPalette.Disabled, QPalette.ButtonText,
                     dark_disabled_text_color if is_light else light_disabled_text_color)
    palette.setColor(QPalette.Disabled, QPalette.Text,
                     dark_disabled_text_color if is_light else light_disabled_text_color)

    # 高亮的颜色是否偏黑
    from PyQt5.Qt import qGray
    highlight_is_dark = qGray(highlight_color.rgb()) < 120
    palette.setColor(QPalette.Highlight, highlight_color)
    palette.setColor(QPalette.HighlightedText, Qt.white if highlight_is_dark else Qt.black)

    return palette


if __name__ == '__main__':
    add = lambda a, b: a + b

    print(add(12, 23))
