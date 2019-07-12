# -*- coding: utf-8 -*-
# @Time    : 2019/6/9 14:04
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Command.py
# @Project : pyqt5_project
# @Software: PyCharm

from PyQt5.QtWidgets import QUndoCommand, QGraphicsScene
from PyQt5.QtCore import QPointF
from UILayer.Workbench.BorderItem import BorderItem, SelectionItem


class AddSelectionItem(QUndoCommand):

    def __init__(self, scene: QGraphicsScene, item: SelectionItem, parent=None):
        super(AddSelectionItem, self).__init__(parent)
        self.scene = scene
        self.item = item
        self.init_pos = item.pos()
        self.setText("创建选区")

    def redo(self) -> None:
        self.scene.addItem(self.item)
        self.scene.clearSelection()
        self.item.setSelected(True)
        self.setText("创建选区")

    def undo(self) -> None:
        self.scene.removeItem(self.item)


class AddItemCommand(QUndoCommand):

    def __init__(self, scene: QGraphicsScene, item: BorderItem, parent=None):

        super(AddItemCommand, self).__init__(parent)

        self.scene = scene
        self.item = item
        self.init_pos = item.pos()
        self.setText("创建选区")

    def redo(self) -> None:
        self.scene.addItem(self.item)
        self.scene.clearSelection()
        self.item.setSelected(True)
        # self.scene.update()

    def undo(self) -> None:
        self.scene.removeItem(self.item)
        # self.scene.update()


class MoveItemCommand(QUndoCommand):

    def __init__(self, item: BorderItem, parent=None):
        super(MoveItemCommand, self).__init__(parent)

        self.item = item
        self.old_pos = item.get_old_pos()
        self.new_pos = item.pos()

    def redo(self) -> None:
        self.item.setPos(self.new_pos)
        self.setText("移动选区")

    def undo(self) -> None:
        self.item.setPos(self.old_pos)
        # self.item.scene().update()


