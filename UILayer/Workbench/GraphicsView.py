import time

from PyQt5.QtCore import pyqtSignal, QPoint, Qt
from PyQt5.QtGui import QTransform, QPainter, QMouseEvent, QKeyEvent, \
    QWheelEvent, QImage, QPixmap, QCursor, QPainterPath
from PyQt5.QtWidgets import QGraphicsView

from UILayer.Workbench.BorderItem import SelectionItem, BorderItem, OutlineItem
from UILayer.MainWindowPk.MainToolBar import ToolsToolBar
from Manager.MarkItemManager import MarkItemManager


class GraphicsView(QGraphicsView):

    vertical_scrollbar_value_changed = pyqtSignal(int, int)
    horizontal_scrollbar_value_changed = pyqtSignal(int, int)
    transform_changed_signal = pyqtSignal(QTransform)
    view_zoom_signal = pyqtSignal(float)

    # 滚动条互斥锁
    _vertical_scrollbar_locked = False
    _horizontal_scrollbar_locked = False

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self._is_move = False
        self.last_cursor_pos = QPoint()
        self._is_comparing = False

        self.verticalScrollBar().setCursor(Qt.ArrowCursor)
        self.horizontalScrollBar().setCursor(Qt.ArrowCursor)
        self.verticalScrollBar().valueChanged.connect(self.vertical_scrollbar_changed)
        self.horizontalScrollBar().valueChanged.connect(self.horizontal_scrollbar_changed)

    def connect_to_synchronize_with(self, view: QGraphicsView):
        view.vertical_scrollbar_value_changed.connect(self.synchronize_vertical_scrollbar_value_with)
        view.horizontal_scrollbar_value_changed.connect(self.synchronize_horizontal_scrollbar_value_with)
        view.transform_changed_signal.connect(self.setTransform)
        GraphicsView._horizontal_scrollbar_locked = False
        GraphicsView._vertical_scrollbar_locked = False

    def disconnect_to_asynchronous_with(self, view: QGraphicsView):
        view.vertical_scrollbar_value_changed.disconnect(self.synchronize_vertical_scrollbar_value_with)
        view.horizontal_scrollbar_value_changed.disconnect(self.synchronize_horizontal_scrollbar_value_with)
        view.transform_changed_signal.disconnect(self.setTransform)

    def vertical_scrollbar_changed(self, value: int):
        if self._is_comparing and not GraphicsView._vertical_scrollbar_locked:
            max_mun = self.verticalScrollBar().maximum()
            # 以下两行顺序不能改
            GraphicsView._vertical_scrollbar_locked = True
            self.vertical_scrollbar_value_changed.emit(max_mun, value)

    def synchronize_vertical_scrollbar_value_with(self, other_max_mnu, other_value):
        adjusted_value = GraphicsView.adjust_scrollbar_value(
            self.verticalScrollBar().maximum(), other_max_mnu, other_value
        )
        # 以下两行顺序不能改
        self.verticalScrollBar().setValue(adjusted_value)
        GraphicsView._vertical_scrollbar_locked = False

    @staticmethod
    def adjust_scrollbar_value(des_max, src_max, value):
        if src_max:
            adjusted_value = int(des_max / src_max * value)
        else:
            adjusted_value = value
        return adjusted_value

    def horizontal_scrollbar_changed(self, value: int):
        if self._is_comparing and not GraphicsView._horizontal_scrollbar_locked:
            max_mun = self.horizontalScrollBar().maximum()
            # 以下两行顺序不能改
            GraphicsView._horizontal_scrollbar_locked = True
            self.horizontal_scrollbar_value_changed.emit(max_mun, value)

    def synchronize_horizontal_scrollbar_value_with(self, other_max_mnu, other_value):
        adjusted_value = GraphicsView.adjust_scrollbar_value(
            self.horizontalScrollBar().maximum(), other_max_mnu, other_value
        )
        # 以下两行顺序不能改
        self.horizontalScrollBar().setValue(adjusted_value)
        GraphicsView._horizontal_scrollbar_locked = False

    def set_is_comparing(self, is_comparing: bool):
        self._is_comparing = is_comparing

    def is_comparing(self):
        return self._is_comparing

    def browser_by_mouse_move(self, mouse_point: QPoint):
        dx = mouse_point.x() - self.last_cursor_pos.x()
        dy = mouse_point.y() - self.last_cursor_pos.y()
        vertical_scrollbar = self.verticalScrollBar()
        horizontal_scrollbar = self.horizontalScrollBar()
        if vertical_scrollbar.isVisible():
            vertical_scrollbar.setValue(vertical_scrollbar.value() - dy)
        if horizontal_scrollbar.isVisible():
            horizontal_scrollbar.setValue(horizontal_scrollbar.value() - dx)
        self.last_cursor_pos = mouse_point

    def zoom_by_given_factor(self, factor1: float, factor2: float):
        is_have_zoom = False
        if (factor1 > 1 and self.transform().m11() < GraphicsViewTest.MAX_ZOOM_MULTIPLE) or \
                (factor2 < 1 and self.transform().m11() > GraphicsViewTest.MIN_ZOOM_MULTIPLE):
            is_have_zoom = True
            self.scale(factor1, factor2)

        transform = self.transform()
        fac = transform.m11()

        if fac > GraphicsViewTest.MAX_ZOOM_MULTIPLE:
            fac = GraphicsViewTest.MAX_ZOOM_MULTIPLE  # if fac > GraphicsViewTest.MAX_ZOOM_MULTIPLE else fac + 1
            self.setTransform(QTransform(
                fac, transform.m12(), transform.m13(),
                transform.m21(), fac, transform.m23(),
                transform.m31(), transform.m32(), transform.m33()
            ))

        if self.transform().m11() < GraphicsViewTest.MIN_ZOOM_MULTIPLE:
            self.setTransform(QTransform(
                GraphicsViewTest.MIN_ZOOM_MULTIPLE, transform.m12(), transform.m13(),
                transform.m21(), GraphicsViewTest.MIN_ZOOM_MULTIPLE, transform.m23(),
                transform.m31(), transform.m32(), transform.m33()
            ))
        if is_have_zoom:
            self.view_zoom_signal.emit(self.transform().m11())
            if self._is_comparing:
                self.transform_changed_signal.emit(self.transform())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.last_cursor_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_move:
            self.browser_by_mouse_move(event.pos())
            event.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Space:
            self.setCursor(Qt.OpenHandCursor)
            self._is_move = True

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Space:
            self.setCursor(Qt.ArrowCursor)
            self._is_move = True

    def wheelEvent(self, event: QWheelEvent) -> None:
        """"""
        d_value = event.angleDelta().y() / 120
        d_value = -4 * d_value
        if event.modifiers() & Qt.ShiftModifier:
            horizontal_scrollbar = self.horizontalScrollBar()
            if horizontal_scrollbar.isVisible():
                value = horizontal_scrollbar.value()
                horizontal_scrollbar.setValue(value + d_value)
        elif event.modifiers() & Qt.ControlModifier:
            factor = 1.09 if d_value < 0 else 0.91
            self.zoom_by_given_factor(factor, factor)
        else:
            vertical_scrollbar = self.verticalScrollBar()
            if vertical_scrollbar.isVisible():
                value = vertical_scrollbar.value()
                vertical_scrollbar.setValue(value + d_value)


class GraphicsViewTest(GraphicsView):
    """
    只负责选区的创建
    """
    # 自定义点击间隔
    CLICK_INVERT_TIME = .45
    MAX_ZOOM_MULTIPLE = 41
    MIN_ZOOM_MULTIPLE = 0.08

    click_signal = pyqtSignal(QMouseEvent)
    dragging_signal = pyqtSignal(QMouseEvent)
    dragged_signal = pyqtSignal(QMouseEvent)
    border_created = pyqtSignal(BorderItem)
    border_moved_signal = pyqtSignal(SelectionItem)

    about_to_create_border = pyqtSignal(QPoint)
    current_tool_changed_signal = pyqtSignal()
    eraser_action_signal = pyqtSignal(BorderItem)

    def __init__(self, item_manager: MarkItemManager, gadget=None, toolbar_gadget=None, eraser_size=3, parent=None):
        super(GraphicsViewTest, self).__init__(parent)
        # 设置拖拽描述 橡皮筋？

        self.border = None
        self.temp_border = None
        self.clicked_time = 0.
        # 要画的图形的形状
        self.gadget = gadget
        self.toolbar_gadget = toolbar_gadget
        # 当使用快捷键是可能会临时改变gadget 这个用来保存原来的gadget
        self.temp_gadget = self.gadget
        self.temp_cursor = self.cursor()

        self._mark_item_manager = item_manager
        self._eraser_size = eraser_size

        # 上一次鼠标触发的位置
        self.is_mouse_pressed = False
        self.is_dragging = False
        self.has_moving_mouse = False
        self.is_creating_border = False
        self.is_creating_polygon = False
        self.last_cursor_pos = QPoint()
        self.polygon_points = []

        self._eraser_cursor_img = QPixmap(QImage("../Sources/Icons/circle-cursor.png"))

        self.click_signal.connect(self.left_mouse_click)
        self.dragging_signal.connect(self.left_mouse_press_and_moving)
        self.dragged_signal.connect(self.left_mouse_moved_and_release)
        self.current_tool_changed_signal.connect(self.current_tool_changed)

    def get_border_item(self):
        return self.border

    def shape(self):
        return self.gadget

    def set_eraser_size(self, eraser_size):
        self._eraser_size = eraser_size

    def set_gadget(self, shape):
        self.gadget = shape
        self.current_tool_changed_signal.emit()

    def current_tool_changed(self):
        if self.gadget == ToolsToolBar.RectangleTool:
            self.setCursor(Qt.CrossCursor)
        elif self.gadget == ToolsToolBar.PolygonTool:
            self.setCursor(Qt.ArrowCursor)
        elif self.gadget == ToolsToolBar.MoveImageTool:
            self.setCursor(Qt.OpenHandCursor)
        elif self.gadget == ToolsToolBar.EraserTool:
            self.setCursor(QCursor(self._eraser_cursor_img))
        else:
            self.setCursor(Qt.ArrowCursor)

    def set_toolbar_gadget(self, gadget):
        self.toolbar_gadget = gadget

    def left_mouse_press_and_moving(self, event: QMouseEvent):
        """
        :param event:
        :return:
        """
        mouse_point = event.pos()
        if self.gadget == ToolsToolBar.RectangleTool:
            self.creating_item(mouse_point, event.modifiers() & Qt.ShiftModifier)

    def creating_selection_item(self, mouse_point: QPoint, is_same: bool = False):

        if self.border is None:
            self.is_creating_border = True
            self.border = SelectionItem(position=self.mapToScene(self.last_cursor_pos),
                                        scene=self.scene(),
                                        view_scale=self.transform().m11(),
                                        shape=self.gadget)
        point1 = self.mapToScene(mouse_point)
        point2 = self.mapToScene(self.last_cursor_pos)
        point, width, height = self.counter_size(point1, point2, mouse_point, is_same)

        try:
            sp = self.mapToScene(point)
            self.border.setPos(sp)
            self.border.set_item_path_by_size(width=width, height=height)
        except Exception as e:
            print("set item error: ", e)

    def counter_size(self, point1, point2, mouse_point, is_same):
        d_point = point1 - point2
        width = d_point.x()
        height = d_point.y()

        x, y = self.last_cursor_pos.x(), self.last_cursor_pos.y()
        if width < 0:
            x = mouse_point.x()
        if height < 0:
            y = mouse_point.y()
        if is_same:
            width = height = min(width, height)

        return QPoint(x, y), abs(width), abs(height)

    def creating_item(self, mouse_point: QPoint, is_same: bool = False):
        self.creating_selection_item(mouse_point, is_same)

    def zoom_by_mouse_move(self, mouse_point: QPoint):
        dx = mouse_point.x() - self.last_cursor_pos.x()
        factor = 1.04 if dx > 0 else 0.96
        self.zoom_by_given_factor(factor, factor)
        self.last_cursor_pos = mouse_point

    def zoom_by_mouse_click(self, is_in=True):
        factor = 1.04 if is_in else 0.96
        self.zoom_by_given_factor(factor, factor)

    def left_mouse_moved_and_release(self, event: QMouseEvent):
        """
        :param event:
        :return:
        """
        if self.is_creating_border and self.border:
            self.created_border()

    def border_moved(self):
        self.border_moved_signal.emit(self.border)

    def left_mouse_click(self, event: QMouseEvent):
        """TODO
        :param event:
        :return:
        """

    def set_item_focus(self, position):
        """
        :param position: item position
        :return: None
        """
        item = self.itemAt(position)
        if item is None:
            return
        if isinstance(item, SelectionItem):
            self.scene().clearSelection()
            item.setSelected(True)
            item.setFocus()

    def counter_polygon_path(self, pos=None):
        new_path = QPainterPath(QPoint(0, 0))
        for point in self.polygon_points:
            new_path.lineTo(point)
        if pos:
            new_path.lineTo(self.border.mapFromScene(self.mapToScene(pos)))
        return new_path

    def created_border(self):
        self.is_creating_border = False
        self.is_creating_polygon = False
        self.scene().removeItem(self.border)
        self.border_created.emit(self.border)
        self.border = None

    def auto_detect_polygon_path_close(self) -> bool:
        start_pos = self.polygon_points[0]
        end_pos = self.polygon_points[-1]
        d_pos = start_pos - end_pos
        if len(self.polygon_points) > 1 and abs(d_pos.x()) < 5 and abs(d_pos.y()) < 5:
            # 两个点很接近 自动闭合
            self.polygon_points[-1] = start_pos
            return True
        return False

    def created_polygon(self):
        path = self.counter_polygon_path()
        self.polygon_points = []
        path.closeSubpath()
        self.border.set_item_path(path=path)
        self.created_border()

    def creating_polygon(self, pos: QPoint):
        try:
            if self.is_creating_polygon and self.border:
                self.polygon_points.append(self.border.mapFromScene(self.mapToScene(pos)))
                if self.auto_detect_polygon_path_close():
                    self.created_polygon()
                else:
                    path = self.counter_polygon_path()
                    self.border.set_item_path(path=path)
            else:
                self.is_creating_polygon = True
                self.border = SelectionItem(self.mapToScene(pos), self.scene(), self.transform().m11(),
                                            shape=self.gadget)
        except Exception as e:
            print("creating polygon error: ", e)

    def eraser_action(self, pos: QPoint):
        pos = self.mapToScene(pos)
        path = QPainterPath()
        path.addEllipse(QPoint(0, 0), self._eraser_size, self._eraser_size)
        eraser_area = SelectionItem(pos, path=path, view_scale=1, scene=self.scene())
        eraser_area.setVisible(False)
        self.eraser_action_signal.emit(eraser_area)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        :param event:
        :return:
        """
        if self.gadget == ToolsToolBar.BrowserImageTool:
            self.setCursor(Qt.ClosedHandCursor)
            self.is_mouse_pressed = True
            event.accept()
            return

        if self.gadget == ToolsToolBar.EraserTool:
            self.eraser_action(event.pos())
            event.accept()
            return

        self.last_cursor_pos = event.pos()
        pressed_item = self.scene().itemAt(self.mapToScene(event.pos()), self.transform())

        if not self.is_creating_polygon and isinstance(pressed_item, SelectionItem):
            QGraphicsView.mousePressEvent(self, event)
            return

        if isinstance(pressed_item, OutlineItem):
            self._mark_item_manager.set_selected_item(pressed_item)

        if self.gadget == ToolsToolBar.MoveImageTool:
            self.is_mouse_pressed = True
            event.accept()
            return

        if event.button() == Qt.LeftButton:
            if self.gadget == ToolsToolBar.RectangleTool or self.gadget == ToolsToolBar.PolygonTool:
                self.about_to_create_border.emit(event.globalPos())
                if self.gadget == ToolsToolBar.PolygonTool:
                    self.creating_polygon(event.pos())
                else:
                    self.is_mouse_pressed = True
                    self.clicked_time = time.time()
            else:
                QGraphicsView.mousePressEvent(self, event)
        elif event.button() == Qt.RightButton:
            if self.is_creating_polygon:
                self.scene().removeItem(self.border)
                self.border = None
                self.is_creating_polygon = False
                self.polygon_points = []
            else:
                QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        :param event:
        :return:
        """
        if not self._is_move:
            flag = True
            if self.gadget == ToolsToolBar.PolygonTool and self.is_creating_polygon:
                try:
                    path = self.counter_polygon_path(event.pos())
                    self.border.set_item_path_by_path(path=path)
                    event.accept()
                    flag = False
                except Exception as e:
                    print(e)

            elif self.gadget == ToolsToolBar.EraserTool:
                self.eraser_action(event.pos())
                event.accept()
                return

            elif self.is_mouse_pressed:
                self.is_dragging = True
                self.has_moving_mouse = True
                self.dragging_signal.emit(event)
                event.accept()
                flag = False

            if flag:
                QGraphicsView.mouseMoveEvent(self, event)
        else:
            GraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """"""
        if self.gadget == ToolsToolBar.BrowserImageTool:
            self.setCursor(Qt.OpenHandCursor)

        if self.is_mouse_pressed:
            if not self.has_moving_mouse:
                self.click_signal.emit(event)
            if self.is_dragging:
                self.dragged_signal.emit(event)
                self.is_dragging = False

            self.is_mouse_pressed = False
            self.has_moving_mouse = False
            event.accept()
        else:
            QGraphicsView.mouseReleaseEvent(self, event)

    def keyPressEvent(self, event: QKeyEvent) -> None:

        if event.key() == Qt.Key_Space:
            self.temp_gadget = self.gadget
            self.set_gadget(ToolsToolBar.MoveImageTool)
            self._is_move = True
        if event.key() == Qt.Key_Shift and self.is_creating_polygon:
            try:
                self.created_polygon()
            except Exception as e:
                print(e)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Space:
            self.set_gadget(self.temp_gadget)
            self._is_move = False
        elif event.key() == Qt.Key_B and event.modifiers() & Qt.ControlModifier and self.polygon_points:
            self.polygon_points.pop()
            if not self.polygon_points:
                self.scene().removeItem(self.border)
                self.is_creating_polygon = False
                self.border = None
            elif self.border:
                self.border.set_item_path_by_path(self.counter_polygon_path())
