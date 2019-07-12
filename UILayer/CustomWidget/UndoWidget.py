# -*- coding: utf-8 -*-
# @Time    : 2019/7/1 13:55
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : UndoWidget.py
# @Project : LSRMSingalVersion2
# @Software: PyCharm
from PyQt5.QtWidgets import QDockWidget, QWidget, QUndoView, QVBoxLayout, QUndoStack, QUndoGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent


class UndoDock(QDockWidget):

    def __init__(self, parent=None):
        QDockWidget.__init__(self, "历史", parent)
        self.setObjectName("undoViewDock")
        self._undo_view = QUndoView(self)
        self._clear_icon = QIcon("../../Sources/Icons/16x16/drive-harddisk.png")

        self._undo_view.setCleanIcon(self._clear_icon)
        self._undo_view.setUniformItemSizes(True)
        self._widget = QWidget(self)
        self._layout = QVBoxLayout(self._widget)
        self._layout.setStretch(0, 0)
        self._layout.addWidget(self._undo_view)
        self.setWidget(self._widget)
        self.retranslateUi()

    def set_stack(self, stack: QUndoStack):
        self._undo_view.setStack(stack)

    def set_group(self, group: QUndoGroup):
        self._undo_view.setGroup(group)

    def changeEvent(self, event: QEvent) -> None:
        pass
        # if e.type():
        # self.LanguageChange
        # self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("历史")
        self._undo_view.setEmptyLabel("<空>")
