import time
import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from CONST.CONST import *
from UILayer.Workbench.BorderItem import SelectionItem, BorderItem
from CommonHelper.CommonHelper import print_transform


class GraphicsViewTest(QGraphicsView):
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
    border_created = pyqtSignal(SelectionItem)
    border_moved_signal = pyqtSignal(SelectionItem)
    view_zoom_signal = pyqtSignal(float)

    def __init__(self, gadget, toolbar_gadget, parent=None):
        super(GraphicsViewTest, self).__init__(parent)
        # 设置拖拽描述 橡皮筋？
        self.setDragMode(QGraphicsView.RubberBandDrag)
        # 渲染提示 hint提示  Antialiasing：消除锯齿;
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.setStyleSheet(""" border: 0; """)

        self.border = None
        self.temp_border = None
        self.clicked_time = 0.
        # 要画的图形的形状
        self.gadget = gadget
        self.toolbar_gadget = toolbar_gadget
        # 当使用快捷键是可能会临时改变gadget 这个用来保存原来的gadget
        self.temp_gadget = self.gadget
        self.temp_cursor = self.parent().cursor()

        # 上一次鼠标触发的位置
        self.is_mouse_pressed = False
        self.is_dragging = False
        self.has_moving_mouse = False
        self.is_creating_border = False
        self.last_cursor_pos = QPoint()
        self.polygon_points = []

        self.click_signal.connect(self.left_mouse_click)
        # self.border_created.connect(self.created_border)
        self.dragging_signal.connect(self.left_mouse_press_and_moving)
        self.dragged_signal.connect(self.left_mouse_moved_and_release)

    def shape(self):
        return self.gadget

    def set_gadget(self, shape: GadgetDockWidgetState):
        self.gadget = shape

    def set_toolbar_gadget(self, gadget: ToolbarState):
        self.toolbar_gadget = gadget

    def left_mouse_press_and_moving(self, event: QMouseEvent):
        """
        :param event:
        :return:
        """
        print("left_mouse_press_and_moving")
        mouse_point = event.pos()
        if self.gadget == GadgetDockWidgetState.RECTANGLE_SELECT_TOOL:
            self.creating_item(mouse_point, event.modifiers() & Qt.ShiftModifier)
        elif self.gadget == GadgetDockWidgetState.GRIP_TONGS_TOOL:
            self.browser_by_mouse_move(mouse_point)
        elif self.gadget == GadgetDockWidgetState.ZOOM_TOOL:
            self.zoom_by_mouse_move(mouse_point)

    def creating_selection_item(self, mouse_point: QPoint, is_same: bool = False):
        try:
            if self.border is None:
                self.is_creating_border = True
                self.border = SelectionItem(
                    self.mapToScene(self.last_cursor_pos),
                    self.scene(), self.transform().m11(), shape=self.gadget)
        except Exception as e:
            print("creating item error: ", e)
            return
        print("creating item rect ")
        point1 = self.mapToScene(mouse_point)
        point2 = self.mapToScene(self.last_cursor_pos)
        point, width, height = self.counter_size(point1, point2, mouse_point, is_same)
        try:
            self.border.setPos(self.mapToScene(point))
            self.border.set_item_path(width=abs(width), height=abs(height))

            print("creating item rect: ", self.border.get_path().boundingRect(), width, height)
        except Exception as e:
            print("set item error: ", e)

    def creating_border_item(self, mouse_point: QPoint, is_same: bool = False):
        try:
            if self.temp_border is None:
                self.is_creating_border = True
                self.temp_gadget = BorderItem(
                    self.mapToScene(self.last_cursor_pos),
                    self.scene(), self.transform().m11(), shape=self.gadget)
        except Exception as e:
            print("creating item error: ", e)
            return

        point1 = self.mapToScene(mouse_point)
        point2 = self.mapToScene(self.last_cursor_pos)
        point, width, height = self.counter_size(point1, point2, mouse_point, is_same)
        try:
            self.temp_border.setPos(self.mapToScene(point))
            self.temp_border.set_item_path(width=abs(width), height=abs(height))
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

        return QPoint(x, y), width, height

    def creating_item(self, mouse_point: QPoint, is_same: bool = False):
        # if self.toolbar_gadget == ToolbarState.NEW_SELECTION:
        self.creating_selection_item(mouse_point, is_same)

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

    def zoom_by_mouse_move(self, mouse_point: QPoint):
        dx = mouse_point.x() - self.last_cursor_pos.x()
        factor = 1.04 if dx > 0 else 0.96
        self.zoom_by_given_factor(factor, factor)
        self.last_cursor_pos = mouse_point

    def zoom_by_mouse_click(self, is_in=True):
        factor = 1.04 if is_in else 0.96
        self.zoom_by_given_factor(factor, factor)

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

    def left_mouse_moved_and_release(self, event: QMouseEvent):
        """
        :param event:
        :return:
        """
        if self.is_creating_border:
            # 必要 否则使用 itemAt是可能出错
            self.is_creating_border = False
            if self.toolbar_gadget == ToolbarState.NEW_SELECTION:
                if self.border is not None:
                    self.scene().removeItem(self.border)
                    self.border = SelectionItem(
                        self.border.scenePos().toPoint(),
                        scene=self.scene(),
                        view_scale=self.transform().m11(),
                        shape=self.border.get_shape(),
                        path=self.border.get_path()
                    )

                self.border_created.emit(self.border)
                self.border.create_selection()
                self.border.item_moved_signal.connect(self.border_moved)
                self.view_zoom_signal.connect(self.border.set_pen_width)
            else:
                if self.border is not None and self.temp_border is not None:
                    if self.toolbar_gadget == ToolbarState.ADD_TO_SELECTION:
                        self.border += self.temp_border
                    elif self.toolbar_gadget == ToolbarState.SUB_FROM_SELECTION:
                        self.border -= self.temp_border
                    elif self.toolbar_gadget == ToolbarState.AND_WITH_SELECTION:
                        self.border &= self.temp_border

    def border_moved(self):
        self.border_moved_signal.emit(self.border)

    def left_mouse_click(self, event: QMouseEvent):
        """
        :param event:
        :return:
        """
        if self.gadget in [
            GadgetDockWidgetState.RECTANGLE_SELECT_TOOL,
            GadgetDockWidgetState.ELLIPSE_SELECT_TOOL
        ] and self.toolbar_gadget == ToolbarState.NEW_SELECTION:
            self.scene().removeItem(self.border)
            self.border = None
        elif self.gadget == GadgetDockWidgetState.ZOOM_TOOL:
            self.zoom_by_mouse_click(self.toolbar_gadget == ToolbarState.CLICK_ZOOM_IN)

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

    def is_ignore_items(self, position, left):
        """
        flag1: 是否按在底层图片上
        flag2: 是否选中快速选择工具
        1、在选中快速选择工具的情况下按在底层的图片 说明不是准备移动图片，
           则可以把上一个选区情况空，准备画新的选区， 返回True
        2、如果选中的不是快速选择工具则 则说明不是要对选区进行改变，返回True
        3、 当flag1 = False flag2 = True 时说明要移动选区 返回 False
        :param position: 鼠标按下的位置
        :return: bool 是否移动选区
        """
        item = self.scene().itemAt(self.mapToScene(position), self.transform())
        flag1 = isinstance(item, QGraphicsPixmapItem)
        flag2 = (self.gadget == GadgetDockWidgetState.RECTANGLE_SELECT_TOOL or
                 self.gadget == GadgetDockWidgetState.ELLIPSE_SELECT_TOOL)
        if left and flag1 and flag2 and not self.is_creating_border and self.border is not None:
            self.scene().removeItem(self.border)
            self.border = None
        return flag1 and flag2 or (not flag2), flag2

    def test(self, point: QPoint):
        print("*******************************")
        scene_point = self.mapToScene(point)
        item = self.scene().itemAt(point, self.transform())
        flag1 = isinstance(item, QGraphicsPixmapItem)
        print("scene point: ", flag1)

        item = self.scene().itemAt(scene_point, self.transform())
        flag1 = isinstance(item, QGraphicsPixmapItem)
        print("scene scene point: ", flag1)

        item = self.itemAt(point)
        flag1 = isinstance(item, QGraphicsPixmapItem)
        print("view point: ", flag1)

        item = self.itemAt(int(scene_point.x()), int(scene_point.y()))
        flag1 = isinstance(item, QGraphicsPixmapItem)
        print("view scene point: ", flag1)
        print("*******************************")

    def counter_polygon_path(self, pos=None):
        new_path = QPainterPath(QPoint(0, 0))
        for point in self.polygon_points:
            new_path.lineTo(point)
        if pos:
            new_path.lineTo(self.border.mapFromScene(self.mapToScene(pos)))
        return new_path

    def auto_detect_polygon_path_close(self) -> bool:
        start_pos = self.polygon_points[0]
        end_pos = self.polygon_points[-1]
        d_pos = start_pos - end_pos
        if len(self.polygon_points) > 1 and abs(d_pos.x()) < 6 and abs(d_pos.y()) < 18:
            # 两个点很接近 自动闭合
            self.polygon_points[-1] = start_pos
            return True
        return False

    def created_polygon(self):
        path = self.counter_polygon_path()
        self.polygon_points = []
        self.is_creating_border = False
        path.closeSubpath()

        self.scene().removeItem(self.border)
        self.border = SelectionItem(
            self.border.scenePos().toPoint(),
            scene=self.scene(),
            view_scale=self.transform().m11(),
            shape=self.border.get_shape(),
            path=path
        )
        self.border.setSelected(True)
        print("selected items: ", self.scene().selectedItems())

    def creating_polygon(self, pos: QPoint):
        try:
            if self.is_creating_border and self.border:
                self.polygon_points.append(self.border.mapFromScene(self.mapToScene(pos)))
                if self.auto_detect_polygon_path_close():
                    self.created_polygon()
                else:
                    path = self.counter_polygon_path()
                    self.border.set_item_path(path=path)
            else:
                self.is_creating_border = True
                self.border = SelectionItem(self.mapToScene(pos), self.scene(), self.transform().m11(), shape=self.gadget)
        except Exception as e:
            print(e)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        :param event:
        :return:
        """
        is_left_mouse_press = (event.button() == Qt.LeftButton)
        is_ignore_items, is_item_move = self.is_ignore_items(event.pos(), is_left_mouse_press)

        if is_left_mouse_press and is_ignore_items:

            if self.gadget == GadgetDockWidgetState.ELLIPSE_SELECT_TOOL:
                self.creating_polygon(event.pos())
            else:
                self.is_mouse_pressed = True
                self.clicked_time = time.time()
                self.last_cursor_pos = event.pos()
        elif event.button() == Qt.RightButton:
            if self.is_creating_border:
                self.scene().removeItem(self.border)
                self.border = None
                self.is_creating_border = False
                self.polygon_points = []
            else:
                QGraphicsView.mousePressEvent(self, event)

        elif is_item_move:
            # 要移动选中或选区，交给内部处理
            QGraphicsView.mousePressEvent(self, event)
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        :param event:
        :return:
        """
        flag = True
        if self.gadget == GadgetDockWidgetState.ELLIPSE_SELECT_TOOL and self.is_creating_border:
            try:
                path = self.counter_polygon_path(event.pos())
                self.border.set_item_path(path=path)
                event.accept()
                flag = False
            except Exception as e:
                print(e)

        if self.is_mouse_pressed:
            print("moving to create rect")
            self.is_dragging = True
            self.has_moving_mouse = True
            self.dragging_signal.emit(event)
            event.accept()
            flag = False

        if flag:
            QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """"""
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
            # if self.border is not None and self.border.has_moved():
            #     self.border_moved_signal.emit(self.border)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """"""
        d_value = event.angleDelta().y() / 120
        d_value = -4 * d_value
        if event.modifiers() & Qt.ControlModifier:
            horizontal_scrollbar = self.horizontalScrollBar()
            if horizontal_scrollbar.isVisible():
                value = horizontal_scrollbar.value()
                horizontal_scrollbar.setValue(value + d_value)
        elif event.modifiers() & Qt.ShiftModifier:
            factor = 1.09 if d_value < 0 else 0.91
            self.zoom_by_given_factor(factor, factor)
        else:
            vertical_scrollbar = self.verticalScrollBar()
            if vertical_scrollbar.isVisible():
                value = vertical_scrollbar.value()
                vertical_scrollbar.setValue(value + d_value)

    def keyPressEvent(self, event: QKeyEvent) -> None:

        if event.key() == Qt.Key_Space:
            self.temp_gadget = self.gadget
            self.temp_cursor = self.parent().cursor()
            self.gadget = OptionTool.GRIP_TONGS
            self.parent().setCursor(Qt.OpenHandCursor)

        if event.key() == Qt.Key_Shift and self.is_creating_border:
            try:
                self.created_polygon()
            except Exception as e:
                print(e)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Space:
            self.parent().setCursor(self.temp_cursor)
            self.gadget = self.temp_gadget

    # def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    #     print("double click")
    #     try:
    #         BorderItem(self.mapToScene(event.pos()), self.scene())
    #     except Exception as e:
    #         print(e)


class GraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

    def mouseMoveEvent(self, event: QMouseEvent):
        print("mouse move")
