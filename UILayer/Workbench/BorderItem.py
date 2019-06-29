import functools

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from CONST.CONST import *
from CommonHelper.CommonHelper import *
from ModelLayer.Selection import Selection


class BorderItem(QGraphicsObject):

    def __init__(self, position, scene, view_scale, shape, transform=QTransform(), parent=None):
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

        scene.clearSelection()
        scene.addItem(self)
        self.setPos(position)
        self.setZValue(10.)
        self.setSelected(True)

    def get_path(self):
        return self._item_path

    def set_item_path(self, **kwargs):
        keys = tuple(kwargs.keys())
        if 'width' in keys and 'height' in keys:
            self._item_path = QPainterPath(QPoint(0, 0))
            self._item_path.addRect(QRectF(0, 0, kwargs["width"], kwargs["height"]))
            print("item path: ", self._item_path)
            self.update(self.boundingRect())
        elif tuple(kwargs.keys()) == ("path", ):
            self._item_path = kwargs["path"]

    def set_pen_width(self, width: [int, float]):
        pen_width = adjust_pen_width(PEN_STANDARD_WIDTH, width)
        self._pen.setWidthF(pen_width)
        self.update(self.boundingRect())

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
        # painter.drawRect(self._item_path.boundingRect())

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
        self._item_path += other.get_path()
        return self

    def __iadd__(self, other):
        """
        轮廓 +=operation
        :param other:
        :return: self
        """
        self._item_path += other.get_path()
        return self

    def __sub__(self, other):
        """
        轮廓 -operation
        :param other:
        :return: self
        """
        self._item_path -= other.get_path()
        return self

    def __isub__(self, other):
        """
        轮廓 -=operation
        :param other:
        :return: self
        """
        self._item_path -= other.get_path()
        return self

    def __and__(self, other):
        """
        轮廓 &operation
        :param other:
        :return: self
        """
        self._item_path &= other.get_path()
        return self

    def __iand__(self, other):
        """
        轮廓 &=operation
        :param other:
        :return: self
        """
        self._item_path &= other.get_path()
        return self


class SelectionItem(BorderItem):
    """
    选区
    """
    item_moved_signal = pyqtSignal()

    def __init__(self, position, scene, view_scale, path: QPainterPath = None,
                 shape=GadgetDockWidgetState.RECTANGLE_SELECT_TOOL, transform=QTransform(), parent=None):
        super(SelectionItem, self).__init__(position, scene, view_scale, shape, transform, parent)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)

        self._selection = None
        self._item_path = path if path else self._item_path

        self._item_has_move = False
        self.old_position = self.pos()
        self.is_left_mouse_press = False
        self.is_left_mouse_move = False

        self.context_menu = self._create_context_menu()
        self._timer.start(self._line_speed)

    def _create_context_menu(self) -> QMenu:
        menu = QMenu(self.parentWidget())

        self.cancel_select_action = create_action(menu, "取消选择")
        self.selection_name_action = create_action(menu, "选区名称...")
        self.new_mark_file_action = create_action(menu, "新建标注文件")
        self.new_mark_item_action = create_action(menu, "新建标注项")

        add_actions(menu, (self.cancel_select_action, None,
                           self.selection_name_action, None,
                           self.new_mark_file_action, self.new_mark_item_action, None))

        mark_menu = menu.addMenu("标注")
        self.origin_outline_action = create_action(mark_menu, "原始轮廓(O)", "Ctrl+A+O")
        self.convex_outline_action = create_action(mark_menu, "凸性缺陷轮廓(C)", "Ctrl+A+C")
        self.polygon_outline_action = create_action(mark_menu, "多边形轮廓(P)", "Ctrl+A+P")
        outline_actions = (self.origin_outline_action, self.convex_outline_action, self.polygon_outline_action)
        add_actions(mark_menu, outline_actions)

        menu.aboutToShow.connect(self._update_context_menu)
        return menu

    def _update_context_menu(self):
        try:
            if self._selection is not None:
                self.selection_name_action.setText(self._selection.get_name())
        except Exception as e:
            print(e)

    def rectangle(self):
        rect = self._item_path.boundingRect()
        return QRect(self.scenePos().x(), self.scenePos().y(), rect.width(), rect.height())

    def get_shape(self):
        return self.shape

    def get_old_pos(self):
        return self.old_position

    def has_moved(self):
        temp = self._item_has_move
        self._item_has_move = False
        return temp

    def create_selection(self):
        try:
            if self._selection is None:
                self._selection = Selection(self.rectangle(), self.shape)
        except Exception as e:
            print(e)

    def get_pix_dots(self) -> tuple:
        pass

    def parentWidget(self):
        # 返回场景的第一个视图
        return self.scene().views()[0]

    def itemChange(self, change, variant):
        # 非选择状态的变化 要设置dirty标志
        # print("item change: ", change, "  variant: ", variant)
        if change == QGraphicsItem.ItemPositionChange:
            return variant
        if change != QGraphicsItem.ItemSelectedChange:
            pass
        return QGraphicsItem.itemChange(self, change, variant)

    def contextMenuEvent(self, event):

        if self.isSelected() and \
                self.shape in (OptionTool.RECT_QUICK_SELECT_TOOL, OptionTool.ELLIPSE_QUICK_SELECT_TOOL):
            self.context_menu.exec_(event.screenPos())

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        :param event:
        :return:
        """
        if event.button() == Qt.LeftButton:
            self.scene().clearSelection()
            self.setSelected(True)
            self.is_left_mouse_press = True
            self.old_position = self.pos()
        else:
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
