# -*- coding: utf-8 -*-
# @Time    : 2019/7/7 13:48
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : HistoryProject.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QColor
from UILayer.Workbench.GraphicsView import GraphicsView
from Documents.ProjectDocument import ProjectDocument
from UILayer.Workbench.BorderItem import OutlineItem


class HistoryProjectManager(QObject):

    def __init__(self, history_projects: [ProjectDocument, None] = None, parent=None):
        super(HistoryProjectManager, self).__init__(parent)

        self._history_projects = history_projects if history_projects else []
        self._workbench_view = GraphicsView()
        self._workbench_view.setObjectName("history_view")
        self._workbench_view.setBackgroundBrush(QColor(147, 147, 147))
        self._current_project = ProjectDocument()

    def set_scene(self, project: ProjectDocument):
        if self._current_project == project:
            return

        self._current_project = project
        self._workbench_view.setScene(project.get_scene())

    def get_view(self) -> QGraphicsView:
        return self._workbench_view

    def synchronize_with_origin_view(self, other_view: GraphicsView):
        self._workbench_view.setTransform(other_view.transform())

        self._workbench_view.verticalScrollBar().setValue(GraphicsView.adjust_scrollbar_value(
            self._workbench_view.verticalScrollBar().maximum(),
            other_view.verticalScrollBar().maximum(),
            other_view.verticalScrollBar().value()
        ))
        self._workbench_view.horizontalScrollBar().setValue(GraphicsView.adjust_scrollbar_value(
            self._workbench_view.horizontalScrollBar().maximum(),
            other_view.horizontalScrollBar().maximum(),
            other_view.horizontalScrollBar().value()
        ))

    def hidden_view(self, hidden: bool):
        self._workbench_view.setHidden(hidden)

    def get_projects_document(self) -> list:
        return self._history_projects

    def get_projects(self) -> list:
        projects = []
        for project_doc in self._history_projects:
            projects.append(project_doc.project())
        return projects

    def get_all_files(self) -> tuple:
        files = []
        for project in self._history_projects:
            files.append(project.project_full_path())
        return tuple(files)

    def set_history_projects(self, history_projects: list):
        if not isinstance(history_projects, (tuple, list)):
            self._history_projects.append(history_projects)
            return
        if len(set(self._history_projects).difference(history_projects)) <= 0:
            return
        self._history_projects = history_projects

    def add_history_project(self, history_project: ProjectDocument):
        if not isinstance(history_project, ProjectDocument):
            return
        if history_project not in self._history_projects:
            self._history_projects.append(history_project)

    def remove_history_project(self, history_project: ProjectDocument):
        if not isinstance(history_project, ProjectDocument):
            return
        if history_project in self._history_projects:
            self._history_projects.remove(history_project)
            del history_project

    def get_project_pixmaps(self):
        pixmaps = []
        for project in self._history_projects:
            pixmaps.append(project.get_pixmap())
        return pixmaps

    def current_index_changed(self, index):
        if 0 <= index < len(self._history_projects):
            self._history_projects[index].set_scale(self._workbench_view.transform().m11())
            self.set_scene(self._history_projects[index])

    def browser_result(self):
        self._workbench_view.setBackgroundBrush(QColor(Qt.black))
        self._current_project.get_pixmap_item().setVisible(False)
        [item.is_browser_result(True) for item in
         self._current_project.get_scene().items() if isinstance(item, OutlineItem)]

        # for item in items:
        #     item.is_browser_result(True)

    def end_browser(self):
        self._workbench_view.setBackgroundBrush(QColor(147, 147, 147))
        self._current_project.get_pixmap_item().setVisible(True)

        [item.is_browser_result(False) for item in
         self._current_project.get_scene().items() if isinstance(item, OutlineItem)]