import os
from enum import IntEnum
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QDockWidget, QInputDialog

from Application.App import BASE_DIR
from CommonHelper.CommonHelper import *
from ModelLayer.MarkProject import MarkProject


class ProjectDockWidget(QDockWidget):

    FOLDER = "folder"
    MAKE_FILE = "mark_file"
    MAKE_ITEM = "mark_item"

    def __init__(self, parent=None):
        super(ProjectDockWidget, self).__init__("标注项目", parent)

        self.setObjectName("projectTreeDockWidget")

        self.project_tree = QTreeWidget(self)
        self.project_tree.setColumnCount(1)
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setObjectName("projectTree")
        self.project_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self.project_tree_item_context_menu)
        self.project_tree_root_context_menu = self._create_project_root_context_menu()
        self.project_tree_folder_context_menu = self._create_folder_child_context_menu()
        self.project_tree_mark_file_context_menu = self._create_mark_file_child_context_menu()
        self.project_tree_mark_item_context_menu = self._create_mark_item_child_context_menu()
        self.setWidget(self.project_tree)

    def _create_project_root_context_menu(self):
        menu = QMenu(self.project_tree)
        self._create_new_menu(menu)

        remove_all_file = create_action(menu, "删除所有文件", slot=self.delete_all_file)
        remove_all_mark_file = create_action(menu, "删除所有标注文件", slot=self.delete_all_mark_file)
        remove_all_mark_item = create_action(menu, "删除所有标注项", slot=self.delete_all_mark_item)
        rename_action = create_action(menu, "重命名", slot=self.rename)
        close_project_action = create_action(menu, "关闭项目", slot=self.close_project)
        property_setting = create_action(menu, "属性", slot=self.property_setting)
        add_actions(menu, (None, remove_all_file, remove_all_mark_file, remove_all_mark_item, None,
                           close_project_action, None, rename_action, None, property_setting))
        return menu

    def _create_folder_child_context_menu(self):
        menu = QMenu(self.project_tree)
        self._create_new_menu(menu)

        remove_self_action = create_action(menu, "删除", slot=self.delete_self)
        remove_all_file = create_action(menu, "删除所有文件", slot=self.delete_all_file)
        remove_all_mark_file = create_action(menu, "删除所有标注文件", slot=self.delete_all_mark_file)
        remove_all_mark_item = create_action(menu, "删除所有标注项", slot=self.delete_all_mark_item)
        rename_action = create_action(menu, "重命名...", slot=self.rename)
        add_actions(menu, (None, remove_all_file, remove_all_mark_file,
                           remove_all_mark_item, remove_self_action, None, rename_action))

        return menu

    def _create_mark_file_child_context_menu(self):
        menu = QMenu(self.project_tree)

        new_empty_mark_item = create_action(menu, "新建标注项", slot=self.create_mark_item)
        new_empty_mark_item.setData(NewFileType.NEW_MARK_ITEM_FROM_MARK_FILE)

        setting_selection_action = create_action(menu, "设置选区...", slot=self.setting_selection)
        remove_self_action = create_action(menu, "删除", slot=self.delete_self)
        remove_all_mark_item = create_action(menu, "删除所有标注项", slot=self.delete_all_mark_item)
        rename_action = create_action(menu, "重命名...", slot=self.rename)

        add_actions(menu, (new_empty_mark_item, None, setting_selection_action, None,
                           remove_self_action, remove_all_mark_item, None, rename_action))
        return menu

    def _create_mark_item_child_context_menu(self):
        menu = QMenu(self.project_tree)

        mark_menu = menu.addMenu("标注")
        origin_outline_action = create_action(menu, "原始轮廓(O)", "Ctrl+A+O", slot=self.outline_detect)
        convex_outline_action = create_action(menu, "凸性缺陷轮廓(C)", "Ctrl+A+C", slot=self.outline_detect)
        polygon_outline_action = create_action(menu, "多边形轮廓(P)", "Ctrl+A+P", slot=self.outline_detect)
        add_actions(mark_menu, (origin_outline_action, convex_outline_action, polygon_outline_action))

        setting_selection_action = create_action(menu, "设置选区...", slot=self.setting_selection)
        remove_self_action = create_action(menu, "删除", slot=self.delete_self)
        rename_action = create_action(menu, "重命名...", slot=self.rename)
        add_actions(menu, (None, setting_selection_action, None, remove_self_action, None, rename_action))

        return menu

    def _create_new_menu(self, parent_menu: QMenu):
        new_menu = parent_menu.addMenu("新建")
        new_folder = create_action(new_menu, "新建文件夹", slot=self.create_folder)
        new_empty_mark_file = create_action(new_menu, "新建空标注文件", slot=self.create_mark_file)
        new_empty_mark_file.setData(NewFileType.NEW_EMPTY_MARK_FILE)
        new_empty_mark_item = create_action(new_menu, "新建空标注项", slot=self.create_mark_item)
        new_empty_mark_item.setData(NewFileType.NEW_EMPTY_MARK_ITEM)

        new_mark_file_from_selection = create_action(new_menu, "根据选区新建标注文件", slot=self.create_mark_file)
        new_mark_file_from_selection.setData(NewFileType.NEW_MARK_FILE_FROM_SELECTION)
        new_mark_item_from_selection = create_action(new_menu, "根据选区新建标注项", slot=self.create_mark_item)
        new_mark_item_from_selection.setData(NewFileType.NEW_MARK_ITEM_FROM_SELECTION)

        add_actions(new_menu, (
            new_folder, None,
            new_empty_mark_file, new_mark_file_from_selection, None,
            new_empty_mark_item, new_mark_item_from_selection
        ))
        return new_menu

    def create_project(self, project_info):
        root = QTreeWidgetItem(self.project_tree)
        root.setText(0, project_info["project_name"])
        root.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/file.png")))

        # 原始图片
        original_img_child = QTreeWidgetItem()
        original_img_child.setText(0, project_info["org_img_name"])
        original_img_child.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/img_icon.png")))
        root.addChild(original_img_child)

        # 项目数据
        project_data = MarkProject(project_info["project_name"])

    def project_tree_item_context_menu(self, point):
        point = self.project_tree.mapToGlobal(point)
        current_item = self.project_tree.currentItem()
        if current_item:
            if not current_item.parent():
                self.project_tree_root_context_menu.exec_(point)
            else:
                what_file = current_item.whatsThis(0)
                if what_file == self.FOLDER:
                    self.project_tree_folder_context_menu.exec_(point)
                elif what_file == self.MAKE_FILE:
                    self.project_tree_mark_file_context_menu.exec_(point)
                elif what_file == self.MAKE_ITEM:
                    self.project_tree_mark_item_context_menu.exec_(point)

    def rename(self):
        current_item = self.project_tree.currentItem()
        new_name, ok = QInputDialog.getText(self, "重命名", "请输入新的名字：", text=current_item.text(0))
        if ok:
            current_item.setText(0, new_name)

    def create_mark_file(self):
        mark_file_name, ok = QInputDialog.getText(self, "新建标注文件", "请输入标注文件名：")
        if ok:
            new_mark_file = QTreeWidgetItem()
            new_mark_file.setText(0, mark_file_name)
            new_mark_file.setWhatsThis(0, self.MAKE_FILE)
            new_mark_file.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/file.png")))
            self.project_tree.currentItem().addChild(new_mark_file)

    def create_mark_item(self):
        mark_item_name, ok = QInputDialog.getText(self, "新建标注项", "请输入标注项的名称：")
        if ok:
            new_mark_item = QTreeWidgetItem()
            new_mark_item.setText(0, mark_item_name)
            new_mark_item.setWhatsThis(0, self.MAKE_ITEM)
            new_mark_item.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/mark_item.jpg")))
            self.project_tree.currentItem().addChild(new_mark_item)

    def create_folder(self):
        folder_name, ok = QInputDialog.getText(self, "新建文件夹", "请输入文件夹的名称：")
        if ok:
            new_folder = QTreeWidgetItem()
            new_folder.setText(0, folder_name)
            new_folder.setWhatsThis(0, self.FOLDER)
            new_folder.setIcon(0, QIcon(os.path.join(BASE_DIR, "sources/images/file.png")))
            self.project_tree.currentItem().addChild(new_folder)

    def delete_all_file(self):
        """"""

    def delete_all_mark_file(self):
        """"""

    def delete_all_mark_item(self):
        """"""

    def close_project(self):
        """"""

    def delete_self(self):
        """"""

    def setting_selection(self):
        """"""

    def outline_detect(self):
        """"""

    # 标注项目属性的设置
    def property_setting(self):
        pass


class ProjectTreeWidget(QTreeWidget):

    def __init__(self, parent=None):
        super(ProjectTreeWidget, self).__init__(parent)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        if self.topLevelItemCount():
            current_item = self.currentItem()
            print(current_item.text(0))


class ProjectTreeItem(QTreeWidgetItem):

    def __init__(self, parent=None):
        super(ProjectTreeItem, self).__init__()


class NewFileType(IntEnum):

    NEW_EMPTY_MARK_FILE = 1
    NEW_MARK_FILE_FROM_SELECTION = 2

    NEW_EMPTY_MARK_ITEM = 3
    NEW_MARK_ITEM_FROM_SELECTION = 4

    NEW_MARK_ITEM_FROM_MARK_FILE = 5
