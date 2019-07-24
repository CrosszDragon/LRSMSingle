# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 16:40
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Documents.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm
import numpy as np


from PyQt5.QtGui import QColor, QImage, QPolygonF, QPen
from PyQt5.QtWidgets import QWidget, QUndoStack, \
     QAction, QGraphicsItem, QMessageBox, QVBoxLayout, QSplitter
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QRect, QRectF
from Documents.MarkData import Project, MarkItem
from UILayer.MainWindowPk.MainToolBar import ToolsToolBar, SelectionOptionToolBar

from CommonHelpers.CommonHelper import qimage2numpy
from CommonHelpers.MatToImg import mat_to_img
from Algorithm.doubleArea_distinguish import detect_outline
from HistoryManage.Command import AddItemCommand, MoveItemCommand, AddSelectionItem

from IOFormat.MarkFile import ProjectFormat
from UILayer.Workbench.GraphicsView import GraphicsViewTest, QPainterPath
from UILayer.Workbench.BorderItem import SelectionItem, OutlineItem
from Documents.HistoryProject import HistoryProjectManager
from UILayer.CustomWidget.Thumbnail import Thumbnail
from Documents.ProjectDocument import ProjectDocument
from Manager.MarkItemManager import MarkItemManager
from Algorithm.AIAlgorithm.AiDetect import detect_one
from loadbig.load_big_grahpicsview import LoadIMGraphicsView
from loadbig.util import is_img_big
from loadbig.slide_helper import SlideHelper
from loadbig.img_from_rect import ImgFromRect


class Document(QWidget, ProjectDocument):

    mark_item_created = pyqtSignal(MarkItem)
    added_mark_item = pyqtSignal(Project, MarkItem)
    browser_result_signal = pyqtSignal(bool)
    selected_mark_item_changed = pyqtSignal(MarkItem)

    def __init__(self, gadget, toolbar_gadget, file_name=None, project_name=None,
                 image_path=None, person_name=None, parent=None, eraser_size=3):
        super(Document, self).__init__(parent)
        ProjectDocument.__init__(self, parent=parent)

        self._writer_format = ProjectFormat()
        self._reader_format = ProjectFormat()
        self._export_format = ProjectFormat()

        self._mark_item_to_outline_item = {}
        self._modifier = False

        self._project = Project(image_path, file_name, project_name, person_name)
        self._image_path = image_path if image_path else self._project.image_path

        self._current_tool = gadget
        self._selection_option = toolbar_gadget
        self._eraser_size = eraser_size

        self.__current_index = -1
        self.__mouse_press_index = -1
        self.__mouse_press_offset = QPoint()
        self.__resize_handel_pressed = False
        self.__undo_stack = QUndoStack(self)
        self._selection_item = None
        self._history_widget = None
        self._history_project_manager = None
        self._mark_item_manager = MarkItemManager()
        self._mark_item_manager.selected_item_changed.connect(self.selected_mark_item_changed)

        # # 创建场景
        self._workbench_scene.setObjectName("workbench_scene")

        self._is_big_img = is_img_big(image_path)
        if self._is_big_img:
            self.workbench_view = LoadIMGraphicsView(self._mark_item_manager, gadget, toolbar_gadget, eraser_size,
                                                     image_path, self._workbench_scene, parent=self)
        else:
            self.workbench_view = GraphicsViewTest(self._mark_item_manager, gadget,
                                                   toolbar_gadget, eraser_size, parent=self)
            # 把场景添加到视图中
            self.workbench_view.setScene(self._workbench_scene)

        self.workbench_view.setObjectName("workbench_view")
        self.workbench_view.setBackgroundBrush(QColor(147, 147, 147))

        # 布局
        self.tab_vertical_layout = QVBoxLayout(self)
        self._splitter1 = QSplitter(self)
        self._splitter1.setStyleSheet("margin: 0px")
        self._splitter1.addWidget(self.workbench_view)

        self._splitter2 = QSplitter(self)
        self._splitter2.setOrientation(Qt.Vertical)
        self._splitter2.setStyleSheet("margin: 0px")
        self._splitter2.addWidget(self._splitter1)

        self.tab_vertical_layout.addWidget(self._splitter2)

        # 当前选择小工具
        self.change_gadget(gadget)

        # 信号接收
        self.workbench_view.border_moved_signal.connect(self.border_moved)
        self.workbench_view.border_created.connect(self.created_border)
        self.workbench_view.about_to_create_border.connect(self.about_to_create_border)
        self.workbench_view.eraser_action_signal.connect(self.eraser_action)

        if all([image_path, project_name, file_name]) and not self._is_big_img:
            self.create_document()

    @property
    def is_big_img(self):
        return self._is_big_img

    def about_to_cmp(self, project_documents: ProjectDocument = None):
        if not self._history_widget:
            self._history_project_manager = HistoryProjectManager(project_documents)

            self._history_widget = Thumbnail(self._history_project_manager, self)
            self._history_project_manager.set_scene(self._history_widget.current_project())
            self._splitter1.addWidget(self._history_project_manager.get_view())
            self._splitter2.addWidget(self._history_widget)

            self.workbench_view.set_is_comparing(True)
            self._history_project_manager.get_view().set_is_comparing(True)

            self._history_widget.selected_project_changed.connect(self._selected_history_project_changed)
            self._history_widget.close_event_signal.connect(self._toggle_cmp_history)
            self._history_widget.synchronize_changed_signal.connect(self._toggle_synchronize_view)

            items = project_documents[0].project().get_mark_items()
            for item in items:
                self._project.add_mark_item(item)

        else:
            self._toggle_cmp_history(True)
            self._history_widget.setHidden(False)

        if True:
            self.connect_to_synchronize_view()

    def had_cmp(self):
        return bool(self._history_widget)

    def _toggle_synchronize_view(self, is_synchronize: bool):
        if is_synchronize:
            self.connect_to_synchronize_view()
        else:
            self.disconnect_to_asynchronous_view()

    def connect_to_synchronize_view(self):
        self._history_project_manager.synchronize_with_origin_view(self.workbench_view)
        self._history_project_manager.get_view().connect_to_synchronize_with(self.workbench_view)
        self.workbench_view.connect_to_synchronize_with(self._history_project_manager.get_view())

    def disconnect_to_asynchronous_view(self):
        self._history_project_manager.get_view().disconnect_to_asynchronous_with(self.workbench_view)
        self.workbench_view.disconnect_to_asynchronous_with(self._history_project_manager.get_view())

    def _toggle_cmp_history(self, is_on: bool):
        self._history_project_manager.hidden_view(not is_on)
        self.workbench_view.set_is_comparing(is_on)
        self._history_project_manager.get_view().set_is_comparing(is_on)

    def _selected_history_project_changed(self, project_doc: ProjectDocument):
        self._history_project_manager.set_scene(project_doc)
        self._history_project_manager.synchronize_with_origin_view(self.workbench_view)

    def modifier(self):
        return not self.__undo_stack.isClean()

    def set_project(self, project: Project):
        self._project = project
        if not self._image_path:
            self._image_path = project.image_path
        if not self._is_big_img:
            self.load_document(self._image_path)
        for mark_item in self._project.get_mark_items():
            self.add_mark_item(mark_item)

    def set_current_mark_item(self, mark_item: MarkItem):
        """"""
        if not mark_item:
            return
        item = [item for item in self._workbench_scene.items() if
                isinstance(item, OutlineItem) and item.mark_item() == mark_item]
        if item:
            self._mark_item_manager.set_selected_item(item[0])
            self.workbench_view.centerOn(item[0])

    def delete_mark_item(self, mark_item: [MarkItem, OutlineItem]):
        if not mark_item:
            return
        if isinstance(mark_item, MarkItem):
            if self._mark_item_manager.selected_mark_item().mark_item() == mark_item:
                self._mark_item_manager.set_selected_item(None)
            self._project.remove_mark_item(mark_item)
            item = [item for item in self._workbench_scene.items() if
                    isinstance(item, OutlineItem) and item.mark_item() == mark_item]
            if item:
                self._mark_item_manager.unregister_mark_item(mark_item.item_name)
                self._workbench_scene.removeItem(item[0])
                del item[0]

        elif isinstance(mark_item, OutlineItem):
            if self._mark_item_manager.selected_mark_item() == mark_item:
                self._mark_item_manager.set_selected_item(None)
            self._project.remove_mark_item(mark_item.mark_item())
            self._mark_item_manager.unregister_mark_item(mark_item.item_name)
            self._workbench_scene.removeItem(mark_item)
            del mark_item

    def project(self) -> Project:
        return self._project

    def project_name(self):
        return self._project.project_name

    def undo_stack(self):
        return self.__undo_stack

    def create_document(self):
        self.load_document()
        self.save_project()

    def save_project(self):
        self.writer_format.save_project(self._project)
        self.__undo_stack.clear()

    def export_result(self, path, progress):
        self.writer_format.export_result(path, self._project, self._image.size(), self)

    def get_file_name(self):
        return self._project.project_full_path()

    def get_project_name(self):
        return self._project.parent()

    def about_to_create_border(self):
        if self._selection_option == SelectionOptionToolBar.Replace:
            self._workbench_scene.removeItem(self._selection_item)
            self._selection_item = None

    def cancel_selection(self):
        self._workbench_scene.removeItem(self._selection_item)
        self._selection_item.disconnect()
        self._selection_item = None

    def selection_as_mark_item(self):
        """TODO"""

    def created_border(self, border: SelectionItem):

        if self._selection_option == SelectionOptionToolBar.Replace:
            self._workbench_scene.removeItem(self._selection_item)
            self._selection_item = border

            self.__undo_stack.push(AddSelectionItem(self._workbench_scene, self._selection_item))

        elif self._selection_option == SelectionOptionToolBar.Subtract:
            if self._selection_item:
                self._selection_item -= border
        elif self._selection_option == SelectionOptionToolBar.Add:
            self._selection_item = border if not self._selection_item else self._selection_item + border
        elif self._selection_option == SelectionOptionToolBar.Intersect:
            if self._selection_item:
                self._selection_item &= border

        if self._selection_item:
            self.workbench_view.view_zoom_signal.connect(self._selection_item.set_pen_width)
            self._selection_item.cancel_selection_signal.connect(self.cancel_selection)
            self._selection_item.as_mark_item_signal.connect(self.selection_as_mark_item)
            self._selection_item.reverse_select_signal.connect(self._select_reverser_path)

    def add_border_item(self, item: SelectionItem):
        self.__undo_stack.push(AddItemCommand(self._workbench_scene, item))

    def border_moved(self, item: SelectionItem):
        self.__undo_stack.push(MoveItemCommand(item))

    def change_toolbar_gadget(self, toolbar_gadget: QAction):
        self._selection_option = toolbar_gadget.data()

    def change_gadget(self, tool: QAction):
        if isinstance(tool, QAction):
            tool = tool.data()

        self.workbench_view.set_gadget(tool)
        if tool == ToolsToolBar.BrowserImageTool:
            self.browser_result()
            self.browser_result_signal.emit(True)
        else:
            if self._current_tool == ToolsToolBar.BrowserImageTool:
                self.end_browser()
                self.browser_result_signal.emit(False)
        self._current_tool = tool

    def eraser_size_changed(self, eraser_size: int):
        self._eraser_size = eraser_size
        self.workbench_view.set_eraser_size(eraser_size)

    def browser_result(self):
        self.workbench_view.setBackgroundBrush(QColor(Qt.black))
        self._pixmap_item.setVisible(False)
        if self.workbench_view.is_comparing():
            self._history_project_manager.browser_result()
        if self._selection_item:
            self._selection_item.setVisible(False)

    def end_browser(self):
        self.workbench_view.setBackgroundBrush(QColor(147, 147, 147))
        self._pixmap_item.setVisible(True)
        if self.workbench_view.is_comparing():
            self._history_project_manager.end_browser()
        if self._selection_item:
            self._selection_item.setVisible(True)

    def get_sub_image_in(self, item: SelectionItem) -> [QImage, None]:

        rect = item.rectangle()
        if self.is_big_img:
            slide_helper = SlideHelper(self.project().image_path)
            image_from_rect = ImgFromRect(rect, slide_helper)
            image_from_rect = image_from_rect.area_img
            return image_from_rect
        else:

            rect_sub_image = self._image.copy(rect)
            polygon_path = item.get_path()
            polygon_sub_image = rect_sub_image

            for row in range(0, rect.width()):
                for clo in range(0, rect.height()):
                    point = QPoint(row, clo)
                    if not polygon_path.contains(point):
                        polygon_sub_image.setPixel(point, 0)
            return polygon_sub_image

    def ai_delete_outline(self, detect_policy):

        result_numpy_array = None
        width_num_array = None

        if not self._selection_item:
            image = self._image
        else:
            image = self._image.copy(self._selection_item.rectangle())

        if detect_policy == 5:
            for h in range(0, image.height(), 256):
                for w in range(0, image.width(), 256):
                    image_ = self._image.copy(QRect(w, h, 255, 255))
                    image_ = qimage2numpy(image_)
                    result = detect_one(image_)
                    numpy_array = mat_to_img(result)
                    if width_num_array is not None:
                        width_num_array = np.hstack((width_num_array, numpy_array))
                    else:
                        width_num_array = numpy_array

                if result_numpy_array is not None:
                    result_numpy_array = np.vstack((result_numpy_array, width_num_array))
                else:
                    result_numpy_array = width_num_array
                width_num_array = None

            print(result_numpy_array.shape)
            return result_numpy_array

    def _get_outlines(self, numpy_array, detect_policy):
        outline_path1 = QPainterPath()
        outline_path2 = QPainterPath()
        outline1, outline2 = detect_outline(detect_policy, numpy_array, drop_area=80)

        for array in outline1:
            sub_path = []
            for point in array[0]:
                point = self._selection_item.mapToScene(point[0][0], point[0][1])
                sub_path.append(point)

            polygon = QPolygonF(sub_path)
            path = QPainterPath()
            path.addPolygon(polygon)
            outline_path1 += path

        for array in outline2:
            sub_path = []
            for point in array[0]:
                point = self._selection_item.mapToScene(point[0][0], point[0][1])
                sub_path.append(point)

            polygon = QPolygonF(sub_path)
            path = QPainterPath()
            path.addPolygon(polygon)
            outline_path2 += path

        return outline_path1, outline_path2

    def _get_outline_by_no_selection(self, numpy_array, detect_policy):
        outline_path1 = QPainterPath()
        outline_path2 = QPainterPath()
        outline1, outline2 = detect_outline(detect_policy, numpy_array, drop_area=80)

        for array in outline1:
            sub_path = []
            for point in array[0]:
                point = QPoint(point[0][0], point[0][1])
                sub_path.append(point)

            polygon = QPolygonF(sub_path)
            path = QPainterPath()
            path.addPolygon(polygon)
            outline_path1 += path

        for array in outline2:
            sub_path = []
            for point in array[0]:
                point = QPoint(point[0][0], point[0][1])
                sub_path.append(point)

            polygon = QPolygonF(sub_path)
            path = QPainterPath()
            path.addPolygon(polygon)
            outline_path2 += path

        return outline_path1, outline_path2

    def _to_create_mark_item(self, outline_path1, outline_path2):
        use_outline1_flag = True
        if not outline_path1.isEmpty():
            self.create_mark_item(outline_path1)
        elif not outline_path2.isEmpty():
            self.create_mark_item(outline_path2)
            use_outline1_flag = False
        if self._selection_item:
            self._selection_item.setFlag(QGraphicsItem.ItemIsMovable, False)
            if use_outline1_flag and not outline_path2.isEmpty():
                self._selection_item.set_reverser_path(outline_path2)

    def detect_outline(self, detect_policy):
        """
        将选中的选区对应的部分图片copy出来，然后转为ndarray类型
        用来转为OpenCV识别轮廓的输入数据
        :param detect_policy: 用哪种识别算法识别轮廓
        :return: None
        """

        if detect_policy >= 5:

            numpy_array = self.ai_delete_outline(detect_policy)
            outline_path1, outline_path2 = self._get_outline_by_no_selection(numpy_array, detect_policy)

            if not self._selection_item:
                self._selection_item = SelectionItem(QPoint(0, 0), self._workbench_scene, self.workbench_view.transform().m11())
                path = QPainterPath()
                path.addRect(QRectF(0, 0, self._image.width(), self._image.height()))
                self._selection_item.set_item_path_by_path(path)
                self._selection_item.reverse_select_signal.connect(self._select_reverser_path)
            self._to_create_mark_item(outline_path1, outline_path2)
            return

        if not self._selection_item:
            QMessageBox.warning(self, "警告", "没有选择区域！")
            return

        if isinstance(self._selection_item, SelectionItem):

            outline_path1 = QPainterPath()
            outline_path2 = QPainterPath()
            if detect_policy == 4:
                self._workbench_scene.removeItem(self._selection_item)
                outline_path1 = self._selection_item.mapToScene(self._selection_item.get_path())
                self._selection_item = None
            else:
                sub_img = self.get_sub_image_in(self._selection_item)
                if sub_img is None:
                    return
                if isinstance(sub_img, QImage):
                    sub_img = qimage2numpy(sub_img)
                outline_path1,  outline_path2 = self._get_outlines(sub_img, detect_policy)
            self._to_create_mark_item(outline_path1, outline_path2)

    def correction_outline(self, option):
        """"""
        if not self._selection_item:
            return
        mark_items = [item for item in self._workbench_scene
            .items(self._selection_item.get_scene_path()) if isinstance(item, OutlineItem)]
        for mark_item in mark_items:
            if mark_item.locked():
                continue
            elif option == 1:
                mark_item += self._selection_item
                self._mark_item_manager.set_selected_item(mark_item)
                break
            elif option == 2:
                mark_item -= self._selection_item
                self._mark_item_manager.set_selected_item(mark_item)
                break
        self._workbench_scene.removeItem(self._selection_item)
        self._selection_item = None

    def eraser_action(self, eraser_area: SelectionItem):
        mark_items = [item for item in self._workbench_scene
            .items(eraser_area.get_scene_path()) if isinstance(item, OutlineItem)]
        for item in mark_items:
            if item.locked():
                continue
            item -= eraser_area
        self._workbench_scene.removeItem(eraser_area)
        del eraser_area

    def create_mark_item(self, outline: QPainterPath):
        item_name = self._mark_item_manager.get_unique_mark_item_name()
        new_mark_item = MarkItem(list(self._project.persons), item_name=item_name, outline_path=outline)
        self._project.add_mark_item(new_mark_item)
        self.add_mark_item(new_mark_item, True)

    def add_mark_item(self, mark_item: MarkItem, new_item=False):
        item = OutlineItem(mark_item, self._workbench_scene, self.workbench_view.transform().m11())

        flag = True
        if new_item:
            flag = self.detect_intersect_with_others(item)

        if flag:
            self._mark_item_to_outline_item[mark_item] = item
            self.browser_result_signal.connect(item.is_browser_result)
            self.workbench_view.view_zoom_signal.connect(item.set_pen_width)
            self._mark_item_manager.register_mark_item(item, mark_item.item_name)

            self.added_mark_item.emit(self._project, mark_item)
            self._mark_item_manager.set_selected_item(item)

    def _select_reverser_path(self):
        if self._selection_item:
            item = self._project.get_mark_items()[-1]
            reverse_path = self._selection_item.get_reverse_path()
            self._selection_item.set_reverser_path(item.get_outline())
            item.set_outline(reverse_path)

    def detect_intersect_with_others(self, new_item: OutlineItem):

        selection_path = new_item.get_scene_path()
        mark_items = [item for item in self._workbench_scene.items(selection_path) if isinstance(item, OutlineItem)]

        for mark_item in mark_items:
            if mark_item != new_item:
                new_item -= mark_item

        if new_item.get_path().isEmpty():
            self._workbench_scene.removeItem(new_item)
            del new_item
            return False
        else:
            new_item.get_path().closeSubpath()
            return True

    def paint_make_item(self, mark_item: MarkItem):

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.yellow)
        self._workbench_scene.addPath(mark_item.draw_path(), pen)

    @property
    def writer_format(self):
        return self._reader_format

    @writer_format.setter
    def writer_format(self, new_writer_format):
        self._writer_format = new_writer_format

    @property
    def reader_format(self):
        return self._reader_format

    @reader_format.setter
    def reader_format(self, new_reader_format):
        self._reader_format = new_reader_format

    @property
    def export_format(self):
        return self._export_format

    @export_format.setter
    def export_format(self, new_export_format):
        self._export_format = new_export_format

