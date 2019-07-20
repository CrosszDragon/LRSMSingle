# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 0:01
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Thumbnail.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QListWidget, QAction, QToolBar, \
    QVBoxLayout, QListWidgetItem, QCheckBox, QFileDialog, QWidget
from PyQt5.QtGui import QIcon
from UILayer.CustomWidget.DockWidget import DockWidget
from Documents.HistoryProject import HistoryProjectManager
from Documents.ProjectDocument import ProjectDocument
from IOFomat.MarkFile import ProjectFormat
from Algorithm.calculation import get_projects_area_data
from DataDisplay.PolygonalChart import PolygonalChart


class Thumbnail(DockWidget):

    item_double_clicked = pyqtSignal(int)

    current_index_changed = pyqtSignal(int)
    remove_project_signal = pyqtSignal(int)
    selected_project_changed = pyqtSignal(ProjectDocument)
    analysis_compare = pyqtSignal(int)

    synchronize_changed_signal = pyqtSignal(bool)

    def __init__(self, history_project_manager: HistoryProjectManager, origin_project, parent=None):
        DockWidget.__init__(self, widget_title="历史项目", parent=parent)

        self.content_widget = QWidget()
        self.setWidget(self.content_widget)

        # 初始化窗口内组件
        self.tb = QToolBar(self)
        self.list_widget = QListWidget()
        self.layout = QVBoxLayout()

        self._origin_project = origin_project
        self._list_item_to_project = {}
        self._history_project_manger = history_project_manager
        self.__create_layout()
        self.__create_tool_bar(self.tb)
        self.__create_list_widget()

        projects = self._history_project_manger.get_projects_document()
        for project in projects:
            self.add_project(project)

    def __del__(self):
        del self.list_widget
        del self.tb
        del self._history_project_manger

    # 创建布局
    def __create_layout(self):
        self.layout.addWidget(self.tb)
        self.layout.addWidget(self.list_widget)
        self.content_widget.setLayout(self.layout)

    def current_project(self) -> ProjectDocument:
        return self._list_item_to_project[self.list_widget.currentItem()]

    # 创建工具栏
    def __create_tool_bar(self, toolbar):
        self.new_action = QAction(QIcon("../Sources/Icons/22x22/add.png"), "添加", self)
        self.new_action.triggered.connect(self.open_new_project)
        toolbar.addAction(self.new_action)

        self.delete_action = QAction(QIcon('../Sources/Icons/22x22/remove.png'), "关闭", self)
        self.delete_action.triggered.connect(self.remove_project)
        toolbar.addAction(self.delete_action)

        self.analysis = QAction(QIcon("../Sources/Icons/24x24/fenxi.png"), "历史数据分析", parent=self)
        self.analysis.triggered.connect(self.analysis_all_project)
        toolbar.addAction(self.analysis)

        self.analysis_compare = QAction(QIcon("../Sources/Icons/24x24//duibifenxi.png"), "数据对比", parent=self)
        toolbar.addAction(self.analysis_compare)
        self.analysis_compare.triggered.connect(self.analysis_project_with)

        self._is_synchronize_checked = QCheckBox("同步", self)
        self._is_synchronize_checked.setChecked(True)
        # self._is_synchronize_checked.to
        self._is_synchronize_checked.toggled.connect(self.synchronize_changed_signal)
        toolbar.addSeparator()
        toolbar.addWidget(self._is_synchronize_checked)

    def analysis_all_project(self):
        projects = self._history_project_manger.get_projects()
        projects.insert(0, self._origin_project.project())

        years = []
        for year in range(len(projects)):
            years.append(2014 + year)

        data = get_projects_area_data(projects, years)
        if not data:
            return

        chart = PolygonalChart("历史数据对比", data,  self)
        chart.show()

    def analysis_project_with(self):
        """"""

    def __create_list_widget(self):
        # 设置列表窗口
        self.list_widget.setGeometry(QtCore.QRect(90, 330, 621, 171))
        self.list_widget.setIconSize(QtCore.QSize(100, 100))
        self.list_widget.setMovement(QtWidgets.QListView.Static)
        self.list_widget.setResizeMode(QtWidgets.QListView.Adjust)
        self.list_widget.setGridSize(QtCore.QSize(150, 150))
        self.list_widget.setViewMode(QtWidgets.QListView.IconMode)
        self.list_widget.setObjectName("listWidget")
        # item样式设置
        self.list_widget.setStyleSheet("QListWidget::item{border:1px solid gray; color:black; margin-top:20px;}")
        # 列表窗口右键点击菜单
        self.list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.my_listwidget_context)
        # 关闭自动排序
        self.list_widget.setSortingEnabled(False)
        # 去除垂直滚动条
        self.list_widget.setWrapping(0)
        self.list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # 设置双击缩略图的信号与槽连接
        self.list_widget.itemClicked.connect(self.__item_clicked)
        self.list_widget.itemDoubleClicked.connect(self.__item_double_clicked)

    def add_project(self, project):
        fit_pixmap = project.get_pixmap()
        fit_pixmap = fit_pixmap.scaled(80, 80, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        new_item = ListWidgetItem(QIcon(fit_pixmap), project.project_brief_info())
        new_item.setToolTip(project.project_brief_info())
        new_item.setSizeHint(QtCore.QSize(90, 130))
        self.list_widget.addItem(new_item)
        self.list_widget.setCurrentItem(new_item)
        self._list_item_to_project[new_item] = project

    # 右键菜单
    def my_listwidget_context(self, point):
        pop_menu = QtWidgets.QMenu()

        if self.list_widget.itemAt(point):
            pop_menu.addAction(self.new_action)
            pop_menu.addAction(self.delete_action)
        else:
            pop_menu.addAction(self.new_action)
        pop_menu.exec_(QtGui.QCursor.pos())

    # 鼠标单击
    def __item_clicked(self, clicked_item):
        """"""

    def __item_double_clicked(self, item):
        if item in self._list_item_to_project:
            self.selected_project_changed.emit(self._list_item_to_project[item])

    def open_new_project(self):
        file_format = "Project files (*.mfb)"
        dir_ = "."
        file_names = QFileDialog.getOpenFileNames(self, "选择遥感图片", dir_, file_format)[0]

        if file_names:
            project_format = ProjectFormat()
            had_files = self._history_project_manger.get_all_files()

            for file in file_names:
                if file == self._origin_project.get_file_name() or file in had_files:
                    continue
                project = ProjectDocument(project_format.read_project(file))
                if not project:
                    continue
                self._history_project_manger.add_history_project(project)
                self.add_project(project)
        else:
            return None

    # 工具栏删除
    def remove_project(self):
        current_project_item = self.list_widget.currentItem()
        if current_project_item and current_project_item in self._list_item_to_project:
            project = self._list_item_to_project[current_project_item]
            self._history_project_manger.remove_history_project(project)
            self.list_widget.removeItemWidget(current_project_item)
            self.list_widget.takeItem(self.list_widget.row(current_project_item))
            del self._list_item_to_project[current_project_item]
            del current_project_item
            self.list_widget.update()


class ListWidgetItem(QListWidgetItem):

    def __init__(self, icon: QIcon, text: str, parent=None):
        super(ListWidgetItem, self).__init__(icon, text, parent)

    def __hash__(self):
        return id(self)
