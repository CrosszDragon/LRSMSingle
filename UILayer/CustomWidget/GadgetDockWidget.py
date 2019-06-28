import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDockWidget, QWidget, \
    QButtonGroup, QVBoxLayout, QSpacerItem, QSizePolicy
from Application.App import BASE_DIR
from CONST.CONST import *
from UILayer.CustomWidget.GadgetButton import GadgetButton
from UILayer.CustomWidget.DockWidget import DockWidget


class GadgetDockWidget(DockWidget):
    gadget_changed = pyqtSignal(GadgetDockWidgetState)

    def __init__(self, widget_title=None, parent=None):
        if widget_title is None:
            widget_title = " "
        super(GadgetDockWidget, self).__init__(widget_title, parent)

        self.setObjectName("gadget_dock_window")
        self.content_widget.setObjectName("gadget_dock_content_widget")

        # self.current_quick_select_tool = OptionTool.ELLIPSE_QUICK_SELECT_TOOL
        # self.current_grip_tool = OptionTool.GRIP_TONGS
        self.current_gadget = GadgetDockWidgetState.NONE_TOOL

        self._init_content_widget()

    def _init_content_widget(self):
        gadget_dock_widget_stylesheet = """
        QPushButton { 
            border: 0;
            padding: 8px;
        }
        QPushButton:hover{
            background-color: rgb(151, 151, 151)
        }
        QPushButton:checked{
            background-color: rgb(151, 151, 151)
        }
        """
        self.content_widget.setStyleSheet(gadget_dock_widget_stylesheet)

        quick_select_context_menu = (
            ("椭圆选框工具", GadgetDockWidgetState.ELLIPSE_SELECT_TOOL),
            ("矩形选框工具", GadgetDockWidgetState.RECTANGLE_SELECT_TOOL)
        )
        grip_context_menu = (
            ("抓手工具(H)", GadgetDockWidgetState.GRIP_TONGS_TOOL),
            ("视图旋转工具(H)", GadgetDockWidgetState.ROTATE_ZOOM)
        )

        move_tool_action = self.create_context_button(
            tip="移动工具(V)", parent=self.content_widget,
            image=os.path.join(BASE_DIR, "sources/icons/move_select.ico"))
        self.quick_select_action = self.create_context_button(
            data=GadgetDockWidgetState.RECTANGLE_SELECT_TOOL,
            context_menu=quick_select_context_menu,
            context_slot=self.select_quick_select_tool,
            tip="矩形选择框(M)", parent=self.content_widget,
            image=os.path.join(BASE_DIR, "sources/icons/quick_select_rectangle.ico"))
        self.grip_action = self.create_context_button(
            data=GadgetDockWidgetState.GRIP_TONGS_TOOL,
            context_menu=grip_context_menu,
            context_slot=self.select_grip_tool,
            tip="抓手工具(H)", parent=self.content_widget,
            image=os.path.join(BASE_DIR, "sources/icons/cursor_hand.ico"))
        zoom_action = self.create_context_button(
            data=GadgetDockWidgetState.ZOOM_TOOL,
            tip="缩放工具(Z)", parent=self.content_widget,
            image=os.path.join(BASE_DIR, "sources/icons/zoom.ico"))

        self.gadget_button_group = QButtonGroup(self)
        self.join_group(
            self.gadget_button_group,
            (move_tool_action, self.quick_select_action, self.grip_action, zoom_action))
        self.gadget_button_group.buttonClicked.connect(self.select_gadget)

        self.verticalLayout = QVBoxLayout(self.content_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout.addWidget(move_tool_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(self.quick_select_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(self.grip_action, alignment=Qt.AlignLeft)
        self.verticalLayout.addWidget(zoom_action, alignment=Qt.AlignLeft)
        spacer_item1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item1)

    def get_current_gadget(self):
        return self.current_gadget

    @staticmethod
    def create_context_button(data=None, context_menu=None, context_slot=None, slot=None, tip=None,
                              checkable=True, image=None, signal="toggled", parent=None):
        new_action = GadgetButton(data, context_menu, context_slot, parent)
        if checkable:
            new_action.setCheckable(True)
        if tip:
            new_action.setToolTip(tip)
            new_action.setStatusTip(tip)
        if slot and callable(slot):
            if signal == "clicked":
                new_action.clicked.connect(slot)
            elif signal == "toggled":
                new_action.toggled.connect(slot)
        if image:
            new_action.setIcon(QIcon(image))
        return new_action

    @staticmethod
    def join_group(target, actions):
        for action in actions:
            target.addButton(action)

    def select_quick_select_tool(self, selected):
        if selected == GadgetDockWidgetState.RECTANGLE_SELECT_TOOL:
            self.quick_select_action.setToolTip("矩形选择框(M)")
            self.quick_select_action.setStatusTip("矩形选择框(M)")
            self.quick_select_action.setIcon(
                QIcon(os.path.join(BASE_DIR, "sources/icons/quick_select_rectangle.ico")))
        elif selected == GadgetDockWidgetState.ELLIPSE_SELECT_TOOL:
            self.quick_select_action.setToolTip("椭圆选择框(M)")
            self.quick_select_action.setStatusTip("椭圆选择框(M)")
            self.quick_select_action.setIcon(
                QIcon(os.path.join(BASE_DIR, "sources/icons/quick_select_oval.ico")))

        self.quick_select_action.set_data(selected)
        self.current_gadget = selected
        self.change_gadget()

    def select_grip_tool(self, selected):
        if selected == GadgetDockWidgetState.GRIP_TONGS_TOOL:
            self.grip_action.setToolTip("抓手工具(H)")
            self.grip_action.setStatusTip("抓手工具(H)")
            self.grip_action.setIcon(
                QIcon(os.path.join(BASE_DIR, "sources/icons/cursor_hand.ico")))
        elif selected == GadgetDockWidgetState.ROTATE_ZOOM:
            self.grip_action.setToolTip("视图旋转工具(R)")
            self.grip_action.setStatusTip("视图旋转工具(R)")
            self.grip_action.setIcon(
                QIcon(os.path.join(BASE_DIR, "sources/icons/rotate.ico")))

        self.quick_select_action.set_data(selected)
        self.current_gadget = selected
        self.change_gadget()

    def select_gadget(self, action):
        gadget = action.get_data()
        self.current_gadget = gadget
        # btn_id = self.gadget_button_group.checkedId()
        # try:
        #     self.current_gadget = OptionTool(btn_id)
        # except ValueError:
        #     return
        # if self.current_gadget == OptionTool.QUICK_SELECT_TOOL:
        #     self.current_gadget = self.current_quick_select_tool
        # elif self.current_gadget == OptionTool.GRIP_TOOL:
        #     self.current_gadget = self.current_grip_tool
        self.change_gadget()

    def change_gadget(self, gadget: GadgetDockWidgetState = None):
        try:
            self.gadget_changed.emit(gadget) if gadget else self.gadget_changed.emit(self.current_gadget)
        except Exception as e:
            print(e)
