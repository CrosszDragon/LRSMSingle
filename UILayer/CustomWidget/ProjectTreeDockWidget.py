import os
from abc import abstractmethod
from enum import IntEnum
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, \
    QInputDialog, QWidget, QVBoxLayout, QMenu

from CommonHelpers.CommonHelper import create_action, add_actions
from Documents.MarkData import MarkItem, Project
from lib.QtProperty.qttreepropertybrowser import QtTreePropertyBrowser
from UILayer.CustomWidget.DockWidget import DockWidget


class ProjectDockWidget(DockWidget):

    FOLDER = "folder"
    MAKE_FILE = "mark_file"
    MAKE_ITEM = "mark_item"
    OriginImage = "image"

    current_item_changed_signal = pyqtSignal(QtTreePropertyBrowser)
    delete_mark_item_signal = pyqtSignal(Project, MarkItem)
    double_click_mark_item = pyqtSignal(Project, MarkItem)

    def __init__(self, parent=None):
        super(ProjectDockWidget, self).__init__("标注项目", parent)

        self.setObjectName("projectTreeDockWidget")

        self._item_to_project = {}
        self._project_to_root_index = {}

        self.project_tree = QTreeWidget(self)
        self.project_tree.setColumnCount(1)
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setObjectName("projectTree")
        self.project_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self.project_tree_item_context_menu)

        self.project_tree_mark_item_context_menu = self._create_mark_item_child_context_menu()

        self.project_tree.currentItemChanged.connect(self.current_item_changed)
        self.project_tree.doubleClicked.connect(self.mouse_double_clicked)

        self._widget = QWidget(self)
        self._layout = QVBoxLayout(self._widget)
        self._layout.setStretch(0, 0)
        self._layout.setContentsMargins(0, 6, 6, 6)
        self._layout.addWidget(self.project_tree)
        self.setWidget(self._widget)

    def _create_mark_item_child_context_menu(self):
        menu = QMenu(self.project_tree)

        remove_self_action = menu.addAction("删除")  # create_action(menu, "删除", slot=self.delete_self)
        remove_self_action.triggered.connect(self.delete_self)
        rename_action = create_action(menu, "重命名...", slot=self.rename)
        add_actions(menu, (remove_self_action, None, rename_action))
        return menu

    def create_project(self, project):
        if project in self._project_to_root_index:
            return

        root = TopLevelTreeItem(project, self.project_tree)
        root.setSelected(True)

        # 原始图片
        original_img_child = QTreeWidgetItem()
        original_img_child.setText(0, os.path.basename(project.image_path))
        original_img_child.setToolTip(0, project.image_path)
        original_img_child.setIcon(0, QIcon("../Sources/images/img_icon.png"))
        original_img_child.setWhatsThis(0, self.OriginImage)
        root.addChild(original_img_child)

        self._project_to_root_index[project] = self.project_tree.indexOfTopLevelItem(root)

    def add_mark_item(self, project, mark_item: MarkItem):
        if project not in self._project_to_root_index:
            return
        mark_item_child = MarkTreeItem(mark_item)
        self._item_to_project[mark_item] = project
        self.project_tree.topLevelItem(self._project_to_root_index[project]).addChild(mark_item_child)

    def project_tree_item_context_menu(self, point):
        point = self.project_tree.mapToGlobal(point)
        current_item = self.project_tree.currentItem()
        if current_item:
            if not current_item.parent():
                """TODO"""
            else:
                what_file = current_item.whatsThis(0)
                if what_file == self.MAKE_ITEM:
                    self.project_tree_mark_item_context_menu.exec_(point)

    def rename(self):
        current_item = self.project_tree.currentItem()
        new_name, ok = QInputDialog.getText(self, "重命名", "请输入新的名字：", text=current_item.text(0))
        if ok and current_item.text(0) != new_name:
            if isinstance(current_item, MarkTreeItem):
                current_item.get_mark_item().item_name = new_name

    def mouse_double_clicked(self) -> None:
        """"""
        current_item = self.project_tree.currentItem()
        if isinstance(current_item, MarkTreeItem):
            item = current_item.get_mark_item()
            self.double_click_mark_item.emit(self._item_to_project[item], item)
        elif isinstance(current_item, TopLevelTreeItem):
            project = current_item.get_project()
            self.double_click_mark_item.emit(project, None)

    def current_item_changed(self, current_item, p):
        if isinstance(current_item, AbstractProjectTreeItem):
            self.current_item_changed_signal.emit(current_item.get_item_browser())

    def delete_all_file(self):
        """"""

    def delete_all_mark_file(self):
        """"""

    def delete_all_mark_item(self):
        """"""

    def selected_mark_changed(self, selected_item: MarkItem):
        """"""
        # self.project_tree.
        if selected_item in self._item_to_project:
            project = self._item_to_project[selected_item]
            top_level_index = self._project_to_root_index[project]
            top_level_item  = self.project_tree.topLevelItem(top_level_index)
            for index in range(top_level_item.childCount()):
                item = top_level_item.child(index)
                if isinstance(item, MarkTreeItem):
                    if item.get_mark_item() == selected_item:
                        self.project_tree.setCurrentItem(item)
                        return

    def close_project(self, project):
        if project not in self._project_to_root_index:
            return
        self.project_tree.takeTopLevelItem(self._project_to_root_index[project])

    def delete_self(self):

        current_item = self.project_tree.currentItem()
        if isinstance(current_item, MarkTreeItem):
            project = self._item_to_project[current_item.get_mark_item()]
            self.delete_mark_item_signal.emit(project, current_item.get_mark_item())

            parent = current_item.parent()
            parent.removeChild(current_item)

            if current_item.get_mark_item() in self._item_to_project:
                del self._item_to_project[current_item.get_mark_item()]
            del current_item

    def setting_selection(self):
        """"""

    def outline_detect(self):
        """"""

    # 标注项目属性的设置
    def property_setting(self):
        pass


class AbstractProjectTreeItem(QTreeWidgetItem):

    def __init__(self, parent=None):
        super(AbstractProjectTreeItem, self).__init__(parent)

    @abstractmethod
    def get_item_browser(self) -> QtTreePropertyBrowser:
        """TODO"""


class TopLevelTreeItem(AbstractProjectTreeItem):

    def __init__(self, project: Project, parent= None):
        super(TopLevelTreeItem, self).__init__(parent)
        self._project = project

        self.setText(0, self._project.project_name)
        self.setWhatsThis(0, ProjectDockWidget.FOLDER)
        self.setIcon(0, QIcon("../Sources/images/file.png"))

        self.setToolTip(0, self._project.project_full_path())
        self._project.project_name_changed.connect(self._name_changed)

    def get_project(self):
        return self._project

    def _name_changed(self):
        self.setText(0, self._project.project_name)

    def get_item_browser(self) -> QtTreePropertyBrowser:
        return self._project.browser

    def set_project(self, project: Project):
        if self._project == project:
            return
        self._project.project_name_changed.disconnect(self._name_changed)
        self._project = project
        self._project.project_name_changed.connect(self._name_changed)


class MarkTreeItem(AbstractProjectTreeItem):

    def __init__(self, mark_item: MarkItem, parent=None):
        super(MarkTreeItem, self).__init__(parent)
        self._mark_item = mark_item
        self.setText(0, mark_item.item_name)
        self.setWhatsThis(0, ProjectDockWidget.MAKE_ITEM)
        self.setIcon(0, QIcon("../Sources/images/mark_item.jpg"))
        self._mark_item.mark_item_name_changed.connect(self._name_changed)

    def _name_changed(self):
        self.setText(0, self._mark_item.item_name)

    def get_mark_item(self):
        return self._mark_item

    def get_item_browser(self):
        return self._mark_item.browser

    def set_mark_item(self, mark_item):
        if self._mark_item == mark_item:
            return
        self._mark_item.mark_item_name_changed.disconnect(self._name_changed)
        self._mark_item = mark_item
        self._mark_item.mark_item_name_changed.connect(self._name_changed)


class NewFileType(IntEnum):

    NEW_EMPTY_MARK_FILE = 1
    NEW_MARK_FILE_FROM_SELECTION = 2

    NEW_EMPTY_MARK_ITEM = 3
    NEW_MARK_ITEM_FROM_SELECTION = 4

    NEW_MARK_ITEM_FROM_MARK_FILE = 5
