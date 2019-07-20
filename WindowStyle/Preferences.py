# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 20:17
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Preferences.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

from enum import Enum

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSettings, QDir, QFileInfo
from PyQt5.QtGui import QColor


class ApplicationStyle(Enum):
    SystemDefaultStyle = 1
    FusionStyle = "fusion"
    LRSMStyle = "lrsm"


class Preferences(QObject):
    """ 首选项控制类 单例模式"""

    application_style_changed_signal = pyqtSignal(ApplicationStyle)
    base_color_changed_signal = pyqtSignal(QColor)
    selection_color_changed_signal = pyqtSignal(QColor)

    _instance = None

    def __init__(self, parent=None):
        if Preferences._instance is None:
            QObject.__init__(self, parent)
            self._settings = QSettings(self)

            self._settings.beginGroup("Interface")
            self._language = self._settings.value("Language")
            self._use_openGL = self.__bool_value("OpenGL", False)
            self._application_style = self._settings.value(
                "ApplicationStyle", ApplicationStyle.SystemDefaultStyle)
            self._base_color = self._settings.value("BaseColor", QColor(Qt.lightGray))
            self._selection_color = self._settings.value("SelectionColor", QColor(48, 140, 198))
            self._settings.endGroup()

            # self._settings.beginGroup('Install')
            # self._first_run = self._settings.value("FirstRun", QDate())
            # self._run_count = self._settings.value("RunCount", 1)
            # self._settings.setValue("FirstRun", self._first_run)
            # self._settings.endGroup()

            self._settings.beginGroup("RecentFiles")
            self.max_recent_project = self._settings.value("MaxRecentProject")
            self._settings.endGroup()

            Preferences._instance = self
        else:
            raise SyntaxError("Preferences是单例类, 请通过静态函数instance获取其实例")

    @staticmethod
    def instance():
        if Preferences._instance is None:
            Preferences._instance = Preferences()
        return Preferences._instance

    def recent_projects(self) -> list:
        return self._settings.value("RecentFiles/ProjectName")

    def add_recent_project(self, project_full_path):
        absolute_file_path = QDir.cleanPath(QFileInfo(project_full_path).absoluteFilePath())

        if not absolute_file_path:
            return

        recent_pros = self.recent_projects()
        if absolute_file_path in recent_pros:
            recent_pros.remove(absolute_file_path)
        recent_pros.insert(0, absolute_file_path)

        while len(recent_pros) > self.max_recent_project:
            recent_pros.pop()

        self._settings.setValue("RecentFiles/ProjectName", recent_pros)

    def clear_recent_projects(self):
        self._settings.remove("RecentFiles/ProjectName")

    def settings(self) -> QSettings:
        return self._settings

    def application_style(self) -> ApplicationStyle:
        return self._application_style

    def set_application_style(self, new_style: ApplicationStyle):
        if isinstance(new_style, ApplicationStyle) and self._application_style == new_style:
            return

        self._application_style = new_style
        self._settings.setValue("Interface/ApplicationStyle", new_style)
        self.application_style_changed_signal.emit(new_style)

    def base_color(self) -> QColor:
        return self._base_color

    def set_base_color(self, base_color: QColor):
        if self._base_color == base_color:
            return
        self._base_color = QColor(base_color)
        self._settings.setValue("Interface/BaseColor", self._base_color)
        self.base_color_changed_signal.emit(base_color)

    def selection_color(self) -> QColor:
        return self._selection_color

    def set_selection_color(self, selection_color: QColor):
        if self._selection_color == selection_color:
            return
        self._selection_color = QColor(selection_color)
        self._settings.setValue("Interface/SelectionColor", self._selection_color)
        self.selection_color_changed_signal.emit(selection_color)

    def __bool_value(self, key: str, default_value=False):
        bool_str = self._settings.value(key, defaultValue=str(default_value))
        bool_str = bool_str.lower()
        res = True if bool_str == "true" else False
        return res


if __name__ == '__main__':

    p1 = Preferences()
    p2 = Preferences.instance()

    print(p1 == p2)
