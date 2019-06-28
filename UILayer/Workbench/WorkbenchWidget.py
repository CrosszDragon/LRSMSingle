# -*- coding: utf-8 -*-
# @Time    : 2019/6/9 14:04
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Command.py
# @Project : pyqt5_project
# @Software: PyCharm

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap, QPen, QPolygonF, QColor
from PyQt5.QtCore import Qt, QRect

from .GraphicsView import GraphicsViewTest
from .BorderItem import *
from CONST.CONST import *
from .ImageItem import ImageItem
from .AntLineItem import AntLineItem
from .GridItem import GridItem

from CommonHelper.CommonHelper import qimage2numpy
from Algorithm.doubleArea_distinguish import detect_outline
from HistoryManage.Command import *


class WorkbenchWidget(QWidget):
    """
    每个WorkbenchWidget对应一张用户要处理的图片
    """
    def __init__(self, file_name=None, gadget=None, toolbar_gadget=None, parent=None):
        super(WorkbenchWidget, self).__init__(parent)

        self.image_label = QLabel("image_label")
        self.image_label.setAlignment(Qt.AlignCenter)

        # 文件名 包含文件的路径
        self.file_name = file_name
        # 文件是否存在未保存数据标志
        self.dirty = False
        # 当前工作区的图片数据
        self.image = None
        self.grid_item = GridItem()

        # 历史记录有关
        self.undo_stack = QUndoStack(self)

        # 图片的垂直镜像
        self.mirrored_vertically = False
        # 水平镜像
        self.mirrored_horizontally = False
        # 创建视图
        self.workbench_view = GraphicsViewTest(gadget, toolbar_gadget, parent=self)
        self.workbench_view.setObjectName("workbench_view")
        self.workbench_view.setBackgroundBrush(QColor(147, 147, 147))

        # 创建场景
        self.workbench_scene = QGraphicsScene(self)
        self.workbench_scene.setObjectName("workbench_scene")

        # 把场景添加到视图中
        self.workbench_view.setScene(self.workbench_scene)

        # 布局
        self.tab_vertical_layout = QVBoxLayout(self)
        self.tab_vertical_layout.addWidget(self.workbench_view)

        self._load_image()

        # 当前选择小工具
        self.change_gadget(gadget)

        # 信号接收
        self.workbench_view.border_created.connect(self.add_border_item)
        self.workbench_view.border_moved_signal.connect(self.border_moved)
        self.workbench_view.view_zoom_signal.connect(self.grid_item.set_pen_width)

    def get_file_name(self):
        return self.file_name

    def is_dirty(self):
        return self.dirty

    def adjust_size(self, option_type):
        """"""

    def can_redo(self) -> bool:
        return self.undo_stack.canRedo()

    def can_undo(self) -> bool:
        return self.undo_stack.canUndo()

    def redo(self):
        if self.undo_stack.canRedo():
            self.undo_stack.redo()

    def undo(self):
        if self.undo_stack.canUndo():
            self.undo_stack.undo()

    def add_border_item(self, item: SelectionItem):
        self.undo_stack.push(AddItemCommand(self.workbench_scene, item))

    def border_moved(self, item: SelectionItem):
        self.undo_stack.push(MoveItemCommand(item))

    def _load_image(self):
        image = QImage(self.file_name)
        # print(self.file_name + "    ", image.format())

        self.workbench_scene.setSceneRect(0, 0, image.width(), image.height())
        if image.isNull():
            del self
            raise FileOpenFailException(self.file_name)
        else:
            self.image = image
            pix_image = QPixmap.fromImage(self.image)
            pixmap_item = QGraphicsPixmapItem(pix_image)
            pixmap_item.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
            pixmap_item.setPos(0, 0)
            pixmap_item.setZValue(0.)
            self.grid_item.set_rect(QRect(0, 0, image.width(), image.height()))

            self.workbench_scene.addItem(pixmap_item)
            # self.workbench_scene.addItem(self.grid_item)

    def rotate(self, angle):
        for item in self.workbench_scene.selectedItems():
            item.rotate(angle)

    def delete(self):
        items = self.workbench_scene.selectedItems()

        if len(items) and QMessageBox.question(
                self, "您确认要删除这些项吗？",
                "?????", QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            while items:
                item = items.pop()
                self.workbench_scene.removeItem(item)
                del item
            self.dirty = True

    def change_toolbar_gadget(self, toolbar_gadget: ToolbarState):
        if isinstance(toolbar_gadget, ToolbarState):
            self.workbench_view.set_toolbar_gadget(toolbar_gadget)

    def change_gadget(self, gadget: GadgetDockWidgetState):
        if isinstance(gadget, GadgetDockWidgetState):
            current_gadget = gadget
            if current_gadget == GadgetDockWidgetState.MOVE_TOOL:
                self.setCursor(Qt.SizeAllCursor)
            elif current_gadget == GadgetDockWidgetState.RECTANGLE_SELECT_TOOL or \
                    current_gadget == GadgetDockWidgetState.ELLIPSE_SELECT_TOOL:
                self.setCursor(Qt.CrossCursor)
            elif current_gadget == GadgetDockWidgetState.GRIP_TONGS_TOOL:
                self.setCursor(Qt.OpenHandCursor)
            elif current_gadget == GadgetDockWidgetState.ROTATE_ZOOM:
                self.setCursor(Qt.SizeFDiagCursor)
            elif current_gadget == GadgetDockWidgetState.ZOOM_TOOL:
                self.setCursor(Qt.SizeHorCursor)

            self.workbench_view.set_gadget(current_gadget)

    def detect_outline(self, detect_policy):
        """
        将选中的选区对应的部分图片copy出来，然后转为ndarray类型
        用来转为OpenCV识别轮廓的输入数据
        :param detect_policy: 用哪种识别算法识别轮廓
        :return: None
        """
        selected_items = self.workbench_scene.selectedItems()
        if selected_items and isinstance(selected_items[0], SelectionItem):
            rect = selected_items[0].rectangle()
            sub_img = self.image.copy(rect)
            res = qimage2numpy(sub_img)

            outline1, outline2 = detect_outline(detect_policy, res, drop_area=80)

            pen = QPen()
            pen.setWidth(1)
            pen.setColor(Qt.yellow)

            try:
                for array in outline1:
                    polygon = QPolygonF()
                    for point in array[0]:
                        point = selected_items[0].mapToScene(point[0][0], point[0][1])
                        polygon.append(point)
                    polygon_item = QGraphicsPolygonItem(polygon)
                    polygon_item.setPen(pen)
                    self.workbench_scene.addItem(polygon_item)
            except Exception as e:
                print(e)


class FileOpenFailException(Exception):

    def __init__(self, file_name):
        self.message = "打开文件\"" + file_name + "\"失败"

    def __str__(self):
        return repr(self.message)
