# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 16:59
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MarkData.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from enum import Enum
from PyQt5.QtGui import QPainterPath, QColor, QPolygonF
from PyQt5.QtCore import QPoint, pyqtSignal, QObject, Qt, QDate
from UILayer.CustomWidget.PropertyManager.PropertyBrowser import MarkItemBrowser, ProjectBrowser


class ProjectObject(QObject):

    visible_changed = pyqtSignal(bool)

    def __init__(self, persons: list, parent=None, date=None, visible=True, locked=False):
        super(ProjectObject, self).__init__(parent)
        self._persons = persons if isinstance(persons, (list, tuple)) else [persons]
        self._locked = locked
        self._visible = visible
        self._date if date else QDate.currentDate()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_date):
        self._date = new_date

    @property
    def persons(self) -> tuple:
        return tuple(self._persons)

    @property
    def locked(self) -> bool:
        return self._locked

    @locked.setter
    def locked(self, lock:bool):
        self._locked = lock

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, is_visible):
        self._visible = is_visible
        self.visible_changed.emit(is_visible)


class MarkType(Enum):

    Grassland = 1
    ResidentialArea = 2


class MarkItem(ProjectObject):

    mark_item_name_changed = pyqtSignal(str, str)
    mark_item_person_added = pyqtSignal(str)
    mark_item_person_removed = pyqtSignal(str)
    mark_item_color_changed = pyqtSignal()

    fill_changed = pyqtSignal()

    def __init__(self, persons: list, item_name, outline_path=None, visible=True, locked=False,
                 mark_type=None, color=None, fill=True, clarity=True, parent=None):
        super(MarkItem, self).__init__(persons, visible=visible, locked=locked, parent=parent)
        """名字要变成唯一的"""

        self._item_name = item_name

        self._draw_path = QPainterPath(outline_path)

        self._item_color = color if color else QColor(Qt.yellow)
        self._mark_type = mark_type if mark_type else [0, 0, 0, '']

        self._fill = fill
        self._clarity = clarity
        self._browser = MarkItemBrowser(self)

    @property
    def browser(self):
        return self._browser

    def _set_draw_path(self):
        for path in self._outline:
            temp_path = QPainterPath()
            temp_path.addPolygon(QPolygonF(path))
            temp_path.closeSubpath()
            self._draw_path += temp_path

    def set_outline(self, outline_path: QPainterPath):
        self._draw_path = outline_path

    def get_outline(self) -> QPainterPath:
        return self._draw_path

    def get_list_mark_data(self) -> tuple:
        return (self._item_name, self.persons, self._mark_type, self._item_color,
                self._visible, self._locked, self._fill, self._draw_path)

    @staticmethod
    def from_list_mark_data_to_item(data: [list, tuple]):
        return MarkItem(
            item_name=data[0],
            persons=data[1],
            mark_type=data[2],
            color=data[3],
            visible=data[4],
            locked=data[5],
            fill=data[6],
            outline_path=data[7]
        )

    @staticmethod
    def from_item_to_string(item) -> str:
        outline_poses = []
        for path in item.get_outline():
            path_pos = []
            for point in path:
                path_pos.append(str((point.x(), point.y())))
            outline_poses.append("|".join(path_pos))

        outline_poses = "#".join(outline_poses)

        mark_type = [str(n) for n in list(item.mark_type)]
        mark_type = "+".join(mark_type)

        names = "@".join(item.persons)
        visible = 1 if item.visible else 0
        locked = 1 if item.locked else 0
        fill = 1 if item.fill else 0
        return "&".join((item.item_name, names, mark_type, str(item.color.name()),
                         str(visible), str(locked), str(fill), outline_poses))

    @staticmethod
    def from_string_to_item(string_data: str):
        """TODO"""
        try:
            data_list = string_data.split("&")
            item_name = data_list[0]
            person_names = data_list[1].split("@")

            mt_list = data_list[2].split("+")
            mark_type = [int(i) for i in mt_list[:-1]]
            mark_type.append(mt_list[-1])

            color = QColor(data_list[3])
            visible = bool(int(data_list[4]))
            locked = bool(int(data_list[5]))
            fill = bool(int(data_list[6]))
            outline = []

            for str_path in data_list[7].split("#"):
                path = []
                for str_point in str_path.split("|"):
                    x, y = list(map(float, str_point[1:-1].split(",")))
                    path.append(QPoint(int(x), int(y)))
                outline.append(path)
            return MarkItem(person_names, item_name, outline, visible, locked, mark_type, color, fill)

        except IndexError as e:
            print("from_item_to_string error: ", e)

    @property
    def clarity(self):
        return self._clarity

    @clarity.setter
    def clarity(self, new_clarity):
        self._clarity = new_clarity

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, is_fill):
        self._fill = is_fill
        self.fill_changed.emit()

    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, new_item_name):
        if self._item_name == new_item_name:
            return
        old_name = self._item_name
        self._item_name = new_item_name
        self.mark_item_name_changed.emit(old_name, new_item_name)

    def set_mark_type(self, mark_type: tuple):
        self._mark_type = mark_type
        print()

    @property
    def color(self) -> QColor:
        return self._item_color

    @color.setter
    def color(self, new_color):
        if new_color == self._item_color:
            return
        self._item_color = new_color
        self.mark_item_color_changed.emit()

    @property
    def mark_type(self):
        return self._mark_type

    @mark_type.setter
    def mark_type(self, new_mark_type):
        self._mark_type = new_mark_type

    def get_person_names(self) -> list:
        return list(self._persons)

    def add_person(self, person_name):
        if person_name in self._persons:
            return
        self._persons.append(person_name)
        self.mark_item_person_added.emit(person_name)

    def remove_person(self, person_name):
        if person_name not in self._persons:
            return
        self._persons.remove(person_name)
        self.mark_item_person_removed.emit(person_name)


class Project(ProjectObject):
    file_name_changed = pyqtSignal(str, str)
    project_name_changed = pyqtSignal(str, str)
    person_name_added = pyqtSignal(str)
    person_name_removed = pyqtSignal(str)
    remove_mark_item_signal = pyqtSignal(MarkItem)

    def __init__(self, image_path, file_name: str, project_name, person_name, parent=None):
        super(Project, self).__init__(person_name, parent)

        self._image_path = image_path
        self._file_name = file_name
        self._project_name = project_name
        self._current_object = None
        self._mark_items = []
        self._browser = ProjectBrowser(self)

    @property
    def browser(self):
        return self._browser

    def get_color(self, pos: QPoint):
        for item in self._mark_items:
            if item.get_outline().contains(pos):
                return item.color
        return QColor(0, 0, 0)

    def contain_mark_item(self, mark_item: MarkItem):
        return mark_item in self._mark_items

    def add_mark_item(self, mark_item: MarkItem):
        if mark_item in self._mark_items:
            return
        self._mark_items.append(mark_item)
        mark_item.mark_item_person_added.connect(self.item_added_person)
        mark_item.mark_item_person_removed.connect(self.item_removed_person)

    def item_added_person(self, person: str):
        if person not in self._persons:
            self._persons.append(person)

    def item_removed_person(self, person: str):
        for item in self._mark_items:
            if person in item.persons:
                return
        self._persons.remove(person)

    def remove_mark_item(self, mark_item: MarkItem):
        if mark_item not in self._mark_items:
            return
        self._mark_items.remove(mark_item)
        # self.remove_mark_item_signal.emit(mark_item)
        mark_item.disconnect()

    def project_full_path(self):
        from os import path
        return path.join(self.file_name, self.project_name)

    def contain_browser(self, browser) -> bool:
        for item in self._mark_items:
            if browser == item.browser:
                return True
        return False

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, new_path):
        self._image_path = new_path

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, new_file_name):
        if new_file_name == self._file_name:
            return
        old_file = self._file_name
        self._file_name = new_file_name
        self.file_name_changed.emit(old_file, self._file_name)

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, new_project_name):
        if self._project_name == new_project_name:
            return
        old_name = self._project_name
        self._project_name = new_project_name
        self.project_name_changed.emit(old_name, self._project_name)

    # def get_person_names(self) -> list:
    #     return list(self._persons)

    def add_person(self, person_name):
        if person_name in self._persons:
            return
        self._persons.append(person_name)
        self.person_name_added.emit(person_name)

    def remove_person(self, person_name):
        if person_name not in self._persons:
            return
        self._persons.remove(person_name)
        self.person_name_removed.emit(person_name)

    def get_mark_items(self) -> list:
        return self._mark_items

    def get_project_data(self) -> tuple:
        result = [self.file_name, self._project_name, self._image_path, self._persons]
        for item in self._mark_items:
            result.append(item.get_list_mark_data())
        return tuple(result)

