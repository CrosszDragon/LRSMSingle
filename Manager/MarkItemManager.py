# -*- coding: utf-8 -*-
# @Time    : 2019/7/4 13:44
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MarkItemManager.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm
from PyQt5.QtCore import QObject, pyqtSignal
from Documents.MarkData import MarkItem
from CommonHelpers.CommonHelper import counter
from UILayer.Workbench.BorderItem import OutlineItem


class MarkItemManager(QObject):

    selected_item_changed = pyqtSignal(MarkItem)

    class MarkItemManagerPrivate:

        def __init__(self):
            self.id_to_mark_item = {}
            self.child_index_to_mark_id = {}
            self.id_to_child_index = {}
            self.selected_mark_items = []
            self.selected_mark_item = None

    def selected_mark_item(self) -> OutlineItem:
        return self._d.selected_mark_item

    def set_selected_item(self, item: OutlineItem):
        if not isinstance(item, OutlineItem):
            return
        if isinstance(self._d.selected_mark_item, OutlineItem):
            if self._d.selected_mark_item == item:
                return
            if self._d.selected_mark_item:
                self._d.selected_mark_item.selected = False

        self._d.selected_mark_item = item
        self.selected_item_changed.emit(item.mark_item())
        if self._d.selected_mark_item:
            self._d.selected_mark_item.selected = True

    def __init__(self, parent=None):
        super(MarkItemManager, self).__init__(parent)
        self._d = MarkItemManager.MarkItemManagerPrivate()
        self._name_counter = counter(1)

    def register_mark_item(self, mark_item: OutlineItem, mark_item_id):
        if mark_item_id in self._d.id_to_mark_item:
            return
        self._d.id_to_mark_item[mark_item_id] = mark_item

    def unregister_mark_item(self, mark_item_id):
        if mark_item_id not in self._d.id_to_mark_item:
            return
        del self._d.id_to_mark_item[mark_item_id]

    def get_unique_mark_item_name(self):
        unique_name = "标注项" + str(next(self._name_counter))
        while unique_name in self._d.id_to_mark_item:
            unique_name = "标注项" + str(next(self._name_counter))
        print(unique_name)
        return unique_name
