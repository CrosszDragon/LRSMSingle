# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 23:54
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : PropertyDock.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QKeyEvent
from lib.QtProperty.qttreepropertybrowser import QtTreePropertyBrowser
from Documents.MarkData import MarkItem, MarkItemBrowser
from UILayer.CustomWidget.DockWidget import DockWidget


class PropertyBrowserDock(DockWidget):
    def __init__(self, browser: QtTreePropertyBrowser = None, parent=None):
        DockWidget.__init__(self, "属性", parent)
        self._browser = browser

        center_widget = QWidget(self)
        self._layout = QVBoxLayout(center_widget)
        self._layout.setContentsMargins(6, 6, 0, 6)
        self.setWidget(center_widget)
        self._has_browser = False

        if browser:
            browser.setHidden(False)
            self._layout.addWidget(browser)
            self._has_browser = True

    def get_browser(self):
        return self._browser

    def remove_browser(self):
        self._layout.removeWidget(self._browser)
        self._browser.setHidden(False)
        self._browser = None
        self._has_browser = False
        # self.setWidget(None)

    def set_browser(self, new_browser: QtTreePropertyBrowser):
        if not new_browser or new_browser == self._browser:
            return

        if self._has_browser:
            self._browser.setHidden(True)
            self._layout.removeWidget(self._browser)
        self._browser = new_browser
        self._browser.setParent(self)
        self._browser.setHidden(False)
        self._layout.addWidget(self._browser)
        self._has_browser = True
        # self.setWidget(self._browser)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        print("key: ", event.key())


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    f = PropertyBrowserDock(browser=MarkItemBrowser(MarkItem(["何盛信"])))
    f.show()

    sys.exit(app.exec_())
















