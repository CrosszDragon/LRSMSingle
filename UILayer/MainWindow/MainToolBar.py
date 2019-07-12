# -*- coding: utf-8 -*-
# @Time    : 2019/7/1 21:56
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MainToolBar.py
# @Project : LSRMSingalVersion2
# @Software: PyCharm
from enum import Enum
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore

from Manager.ActionManager import ActionManager
from Manager.Id import Id


class MainToolBar(QToolBar):

    def __init__(self, parent=None):
        QToolBar.__init__(self, parent)

        self._new_button = QToolButton(self)
        self._open_button = QToolButton(self)
        self._export_action = ActionManager.action(Id("Export"))
        self._save_action = ActionManager.action(Id("SaveProject"))
        self._undo_action = ActionManager.action(Id("Undo"))
        self._redo_action = ActionManager.action(Id("Redo"))

        new_menu = QMenu(self)
        new_menu.addAction(ActionManager.action(Id("NewProject")))
        new_menu.addAction(ActionManager.action(Id("NewMarkItem")))
        self._new_button.setMenu(new_menu)
        # 设置弹出模式 按下工具按钮时，菜单会立即显示。 在此模式下，不会触发按钮自己的操作。
        self._new_button.setPopupMode(QToolButton.InstantPopup)

        open_menu = QMenu(self)
        open_menu.addAction(ActionManager.action(Id("OpenProject")))
        open_menu.addAction(ActionManager.action(Id("OpenOriginalImage")))
        open_menu.addAction(ActionManager.action(Id("OpenMarkFile")))
        self._open_button.setMenu(open_menu)
        self._open_button.setPopupMode(QToolButton.InstantPopup)

        self.setObjectName("ManTooBar")
        self.setWindowTitle("Main Toolbar")
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)

        new_icon = QIcon("../../Sources/Icons/24x24/document-new.png")
        open_icon = QIcon("../../Sources/Icons/24x24/document-open.png")
        save_icon = QIcon("../../Sources/Icons/24x24/document-save.png")
        export_icon = QIcon("../../Sources/Icons/24x24/daochu.png")
        undo_icon = QIcon("../../Sources/Icons/24x24/edit-undo.png")
        redo_icon = QIcon("../../Sources/Icons/24x24/edit-redo.png")

        new_icon.addFile("../../Sources/Icons/16x16/document-new.png")
        open_icon.addFile("../../Sources/Icons/16x16/document-open.png")
        save_icon.addFile("../../Sources/Icons/16x16/document-save.png")
        undo_icon.addFile("../../Sources/Icons/16x16/edit-undo.png")
        redo_icon.addFile("../../Sources/Icons/16x16/edit-redo.png")

        self._new_button.setIcon(new_icon)
        self._new_button.setToolTip("新建")
        self._open_button.setIcon(open_icon)
        self._open_button.setToolTip("打开")
        self._export_action.setIcon(export_icon)
        self._export_action.setToolTip("导出结果")
        self._save_action.setIcon(save_icon)
        self._save_action.setToolTip("保存")
        self._undo_action.setIcon(undo_icon)
        self._undo_action.setToolTip("撤销")
        self._redo_action.setIcon(redo_icon)
        self._redo_action.setToolTip("重做")

        # 优先级
        self._redo_action.setPriority(QAction.LowPriority)

        self.addWidget(self._new_button)
        self.addWidget(self._open_button)
        self.addAction(self._export_action)
        self.addAction(self._save_action)
        self.addSeparator()
        self.addAction(self._undo_action)
        self.addAction(self._redo_action)

        self.orientationChanged.connect(self.orientation_changed)   # toolbar方向改变

        self._restranslateUi()

    def current_document_changed(self, document):
        self._save_action.setEnabled(bool(document))

    def orientation_changed(self, orientation: Qt.Orientation):
        new_style = Qt.ToolButtonFollowStyle if orientation == Qt.Horizontal else Qt.ToolButtonIconOnly
        self.setToolButtonStyle(new_style)

    def _restranslateUi(self):
        """TODO"""

    def changeEvent(self, event: QtCore.QEvent) -> None:
        QToolBar.changeEvent(self, event)
        if event.type() == QtCore.QEvent.LanguageChange:
            self._restranslateUi()


class SelectionOptionToolBar(QToolBar):

    class SelectionOption(Enum):
        Replace = 1
        Add = 2
        Subtract = 3
        Intersect = 4

    Replace = SelectionOption.Replace
    Add = SelectionOption.Add
    Subtract = SelectionOption.Subtract
    Intersect = SelectionOption.Intersect
    del SelectionOption

    selection_option_changed = pyqtSignal(QAction)

    def __init__(self, parent=None):
        super(SelectionOptionToolBar, self).__init__(parent)

        self.setObjectName("ToolsTooBar")
        self.setWindowTitle("Tools Toolbar")
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)

        self._replace = QAction(self)
        self._add = QAction(self)
        self._subtract = QAction(self)
        self._intersect = QAction(self)
        self._action_group = QActionGroup(self)

        self._replace.setIcon(QIcon("../../Sources/Icons/16x16/selection-replace.png"))
        self._replace.setCheckable(True)
        self._replace.setChecked(True)
        self._replace.setToolTip("新建选区")
        self._replace.setData(SelectionOptionToolBar.Replace)

        self._add.setIcon(QIcon("../../Sources/Icons/16x16/selection-add.png"))
        self._add.setCheckable(True)
        self._add.setToolTip("添加到选区")
        self._add.setData(SelectionOptionToolBar.Add)

        self._subtract.setIcon(QIcon("../../Sources/Icons/16x16/selection-subtract.png"))
        self._subtract.setCheckable(True)
        self._subtract.setToolTip("从选区中减去")
        self._subtract.setData(SelectionOptionToolBar.Subtract)

        self._intersect.setIcon(QIcon("../../Sources/Icons/16x16/selection-intersect.png"))
        self._intersect.setCheckable(True)
        self._intersect.setToolTip("与选区相交")
        self._intersect.setData(SelectionOptionToolBar.Intersect)

        self._action_group.addAction(self._replace)
        self._action_group.addAction(self._add)
        self._action_group.addAction(self._subtract)
        self._action_group.addAction(self._intersect)

        self.addAction(self._replace)
        self.addAction(self._add)
        self.addAction(self._subtract)
        self.addAction(self._intersect)

        self.__register()
        self._action_group.triggered.connect(self.selection_option_changed)

    def current_selection_option(self):
        return self._action_group.checkedAction().data()

    def __register(self):
        ActionManager.register_action(self._replace, Id("ReplaceSelection"))
        ActionManager.register_action(self._add, Id("AddSelection"))
        ActionManager.register_action(self._subtract, Id("SubtractSelection"))
        ActionManager.register_action(self._intersect, Id("IntersectSelection"))


class EraserOptionToolBar(QToolBar):

    eraser_size_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(EraserOptionToolBar, self).__init__(parent)

        self._spin_box = QSpinBox(self)
        self._spin_box.setMinimum(3)
        self._spin_box.setMaximum(100)
        self.addWidget(self._spin_box)

        self._spin_box.valueChanged.connect(self.eraser_size_changed)

    def current_eraser_size(self):
        return self._spin_box.value()


class ToolsToolBar(QToolBar):

    tools_changed = pyqtSignal(QAction)

    class Tools(Enum):
        EraserTool = 1
        RectangleTool = 2
        PolygonTool = 3
        MagicTool = 4
        BrowserImageTool = 5
        MoveImageTool = 6

    MoveImageTool = Tools.MoveImageTool
    BrowserImageTool = Tools.BrowserImageTool
    EraserTool = Tools.EraserTool
    RectangleTool = Tools.RectangleTool
    PolygonTool = Tools.PolygonTool
    MagicTool = Tools.MagicTool
    del Tools

    selection_option_changed = pyqtSignal(QAction)
    eraser_size_changed = pyqtSignal(int)

    def __init__(self, parent: QMainWindow = None):
        super(ToolsToolBar, self).__init__(parent)

        self.setObjectName("ToolsTooBar")
        self.setWindowTitle("Tools Toolbar")
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        parent.addToolBar(self)

        self._browser_result_tool = QAction()
        self._eraser_tool = QAction()
        self._rectangle_tool = ActionManager.action(Id("Rectangle"))
        self._polygon_tool = ActionManager.action(Id("Polygon"))
        self._magic_tool = QAction()

        self._browser_result_tool.setIcon(QIcon("../../Sources/Icons/22x22/plugin.png"))
        self._browser_result_tool.setCheckable(True)
        self._browser_result_tool.setToolTip("预览结果")
        self._browser_result_tool.setData(ToolsToolBar.BrowserImageTool)

        self._eraser_tool.setIcon(QIcon("../../Sources/Icons/22x22/stock-tool-eraser.png"))
        self._eraser_tool.setCheckable(True)
        self._eraser_tool.setToolTip("橡皮擦")
        self._eraser_tool.setData(ToolsToolBar.EraserTool)

        self._rectangle_tool.setIcon(QIcon("../../Sources/Icons/22x22/stock-tool-rect-select.png"))
        self._rectangle_tool.setCheckable(True)
        self._rectangle_tool.setChecked(True)
        self._rectangle_tool.setToolTip("矩形选择框")
        self._rectangle_tool.setData(ToolsToolBar.RectangleTool)

        self._polygon_tool.setIcon(QIcon("../../Sources/Icons/24x24/tool-edit-polygons.png"))
        self._polygon_tool.setCheckable(True)
        self._polygon_tool.setToolTip("多边形选择框")
        self._polygon_tool.setData(ToolsToolBar.PolygonTool)

        self._magic_tool.setIcon(QIcon("../../Sources/Icons/22x22/stock-tool-fuzzy-select-22.png"))
        self._magic_tool.setCheckable(True)
        self._magic_tool.setToolTip("魔法棒")
        self._magic_tool.setData(ToolsToolBar.MagicTool)

        self._tools_group = QActionGroup(self)
        self._tools_group.addAction(self._eraser_tool)
        self._tools_group.addAction(self._rectangle_tool)
        self._tools_group.addAction(self._polygon_tool)
        self._tools_group.addAction(self._magic_tool)
        self._tools_group.addAction(self._browser_result_tool)

        self.addAction(self._browser_result_tool)
        self.addAction(self._eraser_tool)
        self.addAction(self._rectangle_tool)
        self.addAction(self._polygon_tool)
        self.addAction(self._magic_tool)

        self._tools_group.triggered.connect(self.checked_action_changed)
        self._tools_group.triggered.connect(self.tools_changed)
        self.__register()

        self._selection_option_toolbar = SelectionOptionToolBar(self)
        self._eraser_option_toolbar = EraserOptionToolBar(self)
        self.parent().addToolBar(self._selection_option_toolbar)
        self.parent().addToolBar(self._eraser_option_toolbar)
        self._eraser_option_toolbar.setHidden(True)

        self._selection_option_toolbar.selection_option_changed.connect(self.selection_option_changed)
        self._eraser_option_toolbar.eraser_size_changed.connect(self.eraser_size_changed)

    def checked_action_changed(self, action: QAction):
        if action == self._rectangle_tool or action == self._polygon_tool:
            # self._selection_toolbar.setEnabled(True)
            self._eraser_option_toolbar.setHidden(True)
            self._selection_option_toolbar.setHidden(False)
            self._selection_option_toolbar.setEnabled(True)
        elif action == self._eraser_tool:
            self._eraser_option_toolbar.setHidden(False)
            self._selection_option_toolbar.setHidden(True)
            self._eraser_option_toolbar.setEnabled(True)
        else:
            self._selection_option_toolbar.setHidden(True)
            self._eraser_option_toolbar.setHidden(True)

    def selection_toolbar(self):
        return self._selection_option_toolbar

    def eraser_toolbar(self):
        return self._eraser_option_toolbar

    def eraser_toolbar(self):
        return self._eraser_option_toolbar

    def setHidden(self, hidden: bool) -> None:
        if hidden:
            self._eraser_option_toolbar.setHidden(hidden)
            self._selection_option_toolbar.setHidden(hidden)
        else:
            if self._tools_group.checkedAction() == self._rectangle_tool:
                self._selection_option_toolbar.setHidden(False)
            elif self._tools_group.checkedAction() == self._eraser_tool:
                self._eraser_option_toolbar.setHidden(False)
        QToolBar.setHidden(self, hidden)

    def current_tools(self):
        try:
            return self._tools_group.checkedAction().data()
        except Exception as e:
            print(e)
            return SelectionOptionToolBar.Replace

    def __register(self):
        ActionManager.register_action(self._eraser_tool, Id("橡皮擦"))
        ActionManager.register_action(self._rectangle_tool, Id("矩形选择框"))
        ActionManager.register_action(self._eraser_tool, Id("多边形选择框"))
        ActionManager.register_action(self._eraser_tool, Id("魔法棒"))


class ToolPopuplAction(QAction):

    def __init__(self, text=None, parent=None):
        super(ToolPopuplAction, self).__init__(text, parent)

        self._popu_toolbar = QToolBar()

        # self._selection_mode = AbstractSelectionTool.SelectionMode.Replace
        # self._default_mode = AbstractSelectionTool.SelectionMode.Replace
        # self._selection_region = QRegion()

        self._popu_toolbar.addAction(self._replace)
        self._replace = QAction(self)
        self._add = QAction(self)
        self._subtract = QAction(self)
        self._intersect = QAction(self)
        self._action_group = QActionGroup(self)

        self._replace.setIcon(QIcon("../../Sources/Icons/16x16/selection-replace.png"))
        self._replace.setCheckable(True)
        self._replace.setChecked(True)
        self._replace.setToolTip("新建选区")

        self._add.setIcon(QIcon("../../Sources/Icons/16x16/selection-add.png"))
        self._add.setCheckable(True)
        self._add.setToolTip("添加到选区")

        self._subtract.setIcon(QIcon("../../Sources/Icons/16x16/selection-subtract.png"))
        self._subtract.setCheckable(True)
        self._subtract.setToolTip("从选区中减去")

        self._intersect.setIcon(QIcon("../../Sources/Icons/16x16/selection-intersect.png"))
        self._intersect.setCheckable(True)
        self._intersect.setToolTip("与选区相交")

        self._action_group.addAction(self._replace)
        self._action_group.addAction(self._add)
        self._action_group.addAction(self._subtract)
        self._action_group.addAction(self._intersect)
        self._popu_toolbar.addAction(self._add)
        self._popu_toolbar.addAction(self._subtract)
        self._popu_toolbar.addAction(self._intersect)

        self.__register()

    def __register(self):
        ActionManager.register_action(self._replace, Id("ReplaceSelection"))
        ActionManager.register_action(self._add, Id("AddSelection"))
        ActionManager.register_action(self._subtract, Id("SubtractSelection"))
        ActionManager.register_action(self._intersect, Id("IntersectSelection"))


if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication
    import sys
    import os
    app = QApplication(sys.argv)
    print(os.getcwd())
    icon = QIcon("../../Sources/Icons/24x24/document-new.png")
    print(icon.isNull())
    w = QMainWindow()
    w.setWindowIcon(icon)
    w.show()

    print(Id("OpenOriginalImage"))
    sys.exit(app.exec_())

