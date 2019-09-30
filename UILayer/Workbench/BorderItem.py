import copy

from PyQt5.QtCore import Qt, QPoint, QTimer, QRectF, pyqtSignal, QRect
from PyQt5.QtGui import QPainterPath, QPen, QPainter, QBrush, QTransform
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsItem, QMenu

from CONSTs.CONST import PEN_STANDARD_WIDTH
from CommonHelpers.CommonHelper import adjust_pen_width, add_actions, create_action

from Documents.MarkData import MarkItem
from UILayer.MainWindowPk.MainToolBar import ToolsToolBar
from Manager.ActionManager import ActionManager
from Manager.Id import Id


class BorderItem(QGraphicsObject):

    def __init__(self, scene, view_scale, shape, transform=QTransform(), parent=None):
        super(BorderItem, self).__init__(parent)
        self.setTransform(transform)

        self.shape = shape
        self._item_path = QPainterPath(QPoint(0, 0))
        self._pen = QPen()
        self._pen.setWidthF(adjust_pen_width(PEN_STANDARD_WIDTH, view_scale))

        # 设置蚂蚁线数据
        self._line_len = 4
        self._line_step = .2
        self._line_speed = 100
        self._line_color = Qt.black

        # 线条的长度
        self._dashes = 4
        # 空白长度
        self._spaces = 10
        self._dash_pattern = [self._line_len] * 20
        self._timer = QTimer()
        self._timer.timeout.connect(self.update_value)

        if scene:
            scene.clearSelection()
            scene.addItem(self)

    def is_empty(self):
        return self._item_path.isEmpty()

    def get_path(self):
        return self._item_path

    def get_scene_path(self):
        return self.mapToScene(self.get_path())

    def copy(self):
        new_item = SelectionItem(
            position=self.scenePos(),
            scene=None,
            view_scale=1,
            path=self._item_path,
            shape=self.get_shape(),
            transform=self.transform(),
            parent=self.parent()
        )
        new_item.pen = self.pen
        return new_item

    def set_item_path_by_size(self, width=0, height=0):
        self._item_path = QPainterPath(QPoint(0, 0))
        self._item_path.addRect(QRectF(0, 0, width, height))
        self.update(self.boundingRect())

    def set_item_path_by_path(self, path):
        self._item_path = path

    def set_pen_width_by_scale(self, width: [int, float]):
        pen_width = adjust_pen_width(PEN_STANDARD_WIDTH, width)
        self._pen.setWidthF(pen_width)

    def set_pen_width_by_width(self, width: [int, float]):
        if isinstance(width, int):
            self._pen.setWidth(width)
        elif isinstance(width, float):
            self._pen.setWidthF(width)

    @property
    def pen(self):
        return self._pen

    @pen.setter
    def pen(self, new_pen: QPen):
        self._pen = new_pen

    def update_value(self):
        """"""
        if self._dashes >= self._line_len and self._spaces >= self._line_len:
            self._dashes = self._spaces = 0.

        if self._dashes <= 0 and self._spaces < self._line_len:
            self._spaces += self._line_step
        elif self._dashes < self._line_len <= self._spaces:
            self._dashes += self._line_step

        self._dash_pattern[0] = self._dashes
        self._dash_pattern[1] = self._spaces
        self.update(self.boundingRect())

    def add_area(self, path: QPainterPath):
        """TODO"""

    def cut_area(self, path: QPainterPath):
        """TODO"""

    def combine_area(self, path: QPainterPath):
        """TODO"""

    def intersects(self, other) -> bool:
        p1 = self.mapToScene(self.get_path())
        p2 = other.mapToScene(other.get_path())
        return p1.intersects(p2)

    def shape(self):
        return self._item_path

    # 继承QGraphicsItem类必须实现 boundingRect() paint()两个方法
    # 返回本item的 包围和矩形 QRectF 用于item的点击等判断
    def boundingRect(self):
        return self._item_path.boundingRect().adjusted(0, 0, 2, 2)

    def paint(self, painter: QPainter, option, widget=None) -> None:

        self._pen.setColor(Qt.white)
        self._pen.setStyle(Qt.SolidLine)
        painter.setPen(self._pen)
        painter.drawPath(self._item_path)

        self._pen.setColor(Qt.black)
        self._pen.setDashPattern(self._dash_pattern)
        painter.setPen(self._pen)
        painter.drawPath(self._item_path)

    def __add__(self, other):
        """
        轮廓 +operation
        :param other:
        :return: self
        """
        p1 = self.mapToScene(self._item_path)
        p2 = other.mapToScene(other.get_path())
        new_path = self.mapFromScene(p1 + p2)

        new_item = self.copy()
        new_item.set_item_path_by_path(new_path)
        return new_item

    def __iadd__(self, other):
        """
        轮廓 +=operation
        :param other:
        :return: self
        """
        p1 = self.mapToScene(self._item_path)
        p2 = other.mapToScene(other.get_path())
        new_path = self.mapFromScene(p1 + p2)
        new_path.closeSubpath()
        self._item_path = new_path
        return self

    def __sub__(self, other):
        """
        轮廓 -operation
        :param other:
        :return: self
        """
        p1 = self.mapToScene(self._item_path)
        p2 = other.mapToScene(other.get_path())
        new_path = self.mapFromScene(p1 - p2)
        new_path.closeSubpath()

        new_item = self.copy()
        new_item.set_item_path_by_path(new_path)
        return new_item

    def __isub__(self, other):
        """
        轮廓 -=operation
        :param other:
        :return: self
        """
        p1 = self.mapToScene(self._item_path)
        p2 = other.mapToScene(other.get_path())
        new_path = self.mapFromScene(p1 - p2)
        new_path.closeSubpath()
        self._item_path = new_path
        self.update()
        return self

    def __and__(self, other):
        """
        轮廓 &operation
        :param other:
        :return: self
        """
        p1 = self.mapToScene(self._item_path)
        p2 = other.mapToScene(other.get_path())
        new_path = self.mapFromScene(p1 & p2)
        new_path.closeSubpath()

        new_item = self.copy()
        new_item.set_item_path_by_path(new_path)
        return new_item

    def __iand__(self, other):
        """
        轮廓 &=operation
        :param other:
        :return: self
        """
        p1 = self.mapToScene(self._item_path)
        p2 = other.mapToScene(other.get_path())
        self._item_path = self.mapFromScene(p1 & p2)
        self._item_path.closeSubpath()
        self.update()
        return self


class SelectionItem(BorderItem):
    """
    选区
    """
    item_moved_signal = pyqtSignal()
    cancel_selection_signal = pyqtSignal()
    as_mark_item_signal = pyqtSignal()
    reverse_select_signal = pyqtSignal()

    def __init__(self, position, scene=None, view_scale=None, path: QPainterPath = None,
                 shape=ToolsToolBar.RectangleTool, transform=QTransform(), parent=None):
        super(SelectionItem, self).__init__(scene, view_scale, shape, transform, parent)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

        self._selection = None
        self._item_path = path if path else self._item_path
        self._reverse_path = QPainterPath()

        self._item_has_move = False
        self.old_position = self.pos()
        self.is_left_mouse_press = False
        self.is_left_mouse_move = False

        self.context_menu = self._create_context_menu()
        self._timer.start(self._line_speed)

        self.setPos(position)
        self.setZValue(10.)
        self.setSelected(True)

    def set_reverser_path(self, path: QPainterPath):
        self._reverse_path = path
        self.reverse_select_action.setEnabled(True)

    def get_reverse_path(self):
        return self._reverse_path

    def _create_context_menu(self) -> QMenu:
        menu = QMenu(self.parentWidget())

        self.cancel_select_action = create_action(menu, "取消选择")
        self.reverse_select_action = create_action(menu, "选择反向")
        self.as_mark_item_action = ActionManager.action(Id("AsOutline"))

        self.cancel_select_action.triggered.connect(self.cancel_selection_signal)
        self.as_mark_item_action.triggered.connect(self.as_mark_item_signal)
        self.reverse_select_action.triggered.connect(self.reverse_select_signal)
        self.reverse_select_action.setEnabled(False)

        add_actions(menu, (self.cancel_select_action, self.reverse_select_action, None,
                           self.as_mark_item_action, None))

        mark_menu = menu.addMenu("标注")
        self.origin_outline_action = ActionManager.action(Id("OriginOutline"))
        self.convex_outline_action = ActionManager.action(Id("ConvexOutline"))
        self.polygon_outline_action = ActionManager.action(Id("PolygonOutline"))
        outline_actions = (self.origin_outline_action, self.convex_outline_action, self.polygon_outline_action)
        add_actions(mark_menu, outline_actions)

        correction_menu = menu.addMenu("轮廓微调")
        correction_actions = (ActionManager.action(Id("AddOutlineCorrection")),
                              ActionManager.action(Id("RemoveOutlineCorrection")))
        add_actions(correction_menu, correction_actions)

        menu.aboutToShow.connect(self._update_context_menu)
        return menu

    def as_mark_item(self):
        self.as_mark_item_signal.emit(self._item_path)

    def _update_context_menu(self):
        try:
            if self._selection is not None:
                self.selection_name_action.setText(self._selection.get_name())
        except Exception as e:
            print("update context menu error: ", e)

    def rectangle(self):
        rect = self._item_path.boundingRect()
        pos = self.mapToScene(QPoint(rect.x(), rect.y()))
        return QRect(pos.x(), pos.y(), rect.width(), rect.height())

    def get_shape(self):
        return self.shape

    def get_old_pos(self):
        return self.old_position

    def has_moved(self):
        temp = self._item_has_move
        self._item_has_move = False
        return temp

    def create_selection(self):
        """TODO"""

    def get_pix_dots(self) -> tuple:
        pass

    def parentWidget(self):
        # 返回场景的第一个视图
        scene = self.scene()
        if scene:
            return scene.views()[0]
        return None

    def itemChange(self, change, variant):
        if change == QGraphicsItem.ItemPositionChange:
            return variant
        if change != QGraphicsItem.ItemSelectedChange:
            pass
        return QGraphicsItem.itemChange(self, change, variant)

    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.screenPos())

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        :param event:
        :return:
        """
        self.scene().clearSelection()
        self.setSelected(True)
        if event.button() == Qt.LeftButton:
            self.is_left_mouse_press = True
            self.old_position = self.pos()
        QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        :param event:
        :return:
        """
        self.is_left_mouse_move = self.is_left_mouse_press
        QGraphicsItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        :param event:
        :return:
        """
        if self.is_left_mouse_move:
            self._item_has_move = True
            self.item_moved_signal.emit()
            self.is_left_mouse_move = self.is_left_mouse_press = False
        QGraphicsItem.mouseReleaseEvent(self, event)


class OutlineItem(BorderItem):

    def __init__(self, mark_item: MarkItem, scene, view_scale, transform=QTransform(), parent=None):
        super(OutlineItem, self).__init__(scene=scene, shape=None, view_scale=view_scale,
                                          transform=transform, parent=parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self._is_browser_result = False
        self._pen.setColor(mark_item.color)
        self._mark_item = mark_item
        self._mark_item.visible_changed.connect(self.visible_changed)
        self._mark_item.fill_changed.connect(self.update)
        self._mark_item.mark_item_color_changed.connect(self.update)
        self.setSelected(True)
        self._selected = False

    def __del__(self):
        del self._mark_item

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, select: bool):
        self._selected = select
        if self._selected:
            self._timer.start(self._line_speed)
        elif self._timer.isActive():
            self._timer.stop()

    def mark_item(self) -> MarkItem:
        return self._mark_item

    def locked(self):
        return self._mark_item.locked

    def is_browser_result(self, br: bool):
        self._is_browser_result = br

    def visible_changed(self, visible):
        self.setVisible(visible)

    def get_path(self) -> QPainterPath:
        return self._mark_item.get_outline()

    def __isub__(self, other: BorderItem):
        p1 = self.mapToScene(self.get_path())
        p2 = other.mapToScene(other.get_path())
        self._mark_item.set_outline(self.mapFromScene(p1 - p2))
        self.update()
        return self

    def __iadd__(self, other: BorderItem):
        p1 = self.mapToScene(self.get_path())
        p2 = other.mapToScene(other.get_path())
        self._mark_item.set_outline(self.mapFromScene(p1 + p2))
        self.update()
        return self

    def shape(self):
        return self._mark_item.get_outline()

    def boundingRect(self):
        return self._mark_item.get_outline().boundingRect()

    def paint(self, painter: QPainter, option, widget=None) -> None:

        if self._mark_item.fill or self._is_browser_result:

            brush = QBrush(self._mark_item.color)
            painter.fillPath(self._mark_item.get_outline(), brush)
        else:
            self._pen.setColor(self._mark_item.color)
            painter.setPen(self._pen)
            painter.drawPath(self._mark_item.get_outline())
        if self._selected:
            pen = QPen(self._pen)
            pen.setWidthF(self._pen.widthF() + 0.8)

            pen.setColor(Qt.white)
            pen.setDashPattern(self._dash_pattern)
            painter.setPen(pen)
            painter.drawPath(self._mark_item.get_outline())
