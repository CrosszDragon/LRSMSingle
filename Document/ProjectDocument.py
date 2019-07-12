# -*- coding: utf-8 -*-
# @Time    : 2019/7/7 21:06
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : ProjectDocument.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from Document.MarkData import Project
from UILayer.Workbench.BorderItem import OutlineItem


class ProjectDocument(QObject):

    def __init__(self, project: Project = None, parent=None):
        super(ProjectDocument, self).__init__(parent)

        self._image = None
        self._pixmap = None
        self._pixmap_item = QGraphicsPixmapItem()
        self._workbench_scene = QGraphicsScene(self)
        self._project = None
        if project and isinstance(project, Project):
            self.set_project(project)

    def get_scene(self):
        return self._workbench_scene

    def set_project(self, project: Project):
        self._project = project
        self.load_document()
        self.load_mark_items()

    def load_mark_items(self, scale: int = 1):
        if not self._project:
            return
        for mark_item in self._project.get_mark_items():
            OutlineItem(mark_item, self._workbench_scene, scale)

    def set_scale(self, scale):
        for item in self._workbench_scene.items():
            item.set_pen_width(scale)

    def get_pixmap(self):
        return self._pixmap

    def get_pixmap_item(self):
        return self._pixmap_item

    def project_brief_info(self):
        return self._project.project_name

    def project_full_path(self):
        if self._project:
            return self._project.project_full_path()

    def load_document(self):
        image = QImage(self._project.image_path)
        print(self._project.image_path + "    ", image.format())

        self._workbench_scene.setSceneRect(0, 0, image.width(), image.height())
        if image.isNull():
            del self
            raise FileOpenFailException(self._project.image_path)
        else:
            self._image = image
            self._pixmap = QPixmap.fromImage(self._image)
            self._pixmap_item.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
            self._pixmap_item.setPos(0, 0)
            self._pixmap_item.setZValue(0.)
            self._pixmap_item.setFlag(QGraphicsItem.ItemIsSelectable, False)
            self._pixmap_item.setPixmap(self._pixmap)
            self._workbench_scene.addItem(self._pixmap_item)


class FileOpenFailException(Exception):

    def __init__(self, file_name):
        self.message = "打开文件\"" + file_name + "\"失败"

    def __str__(self):
        return repr(self.message)
