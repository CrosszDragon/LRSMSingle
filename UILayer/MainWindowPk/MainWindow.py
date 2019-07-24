import os
import sys

from PyQt5.QtCore import Qt, pyqtSignal, QFile, QSettings, QTimer, QVariant
from PyQt5.QtGui import QPalette, QColor, QPixmapCache, QIcon
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QFileDialog, QMessageBox, QUndoGroup, QApplication, QAction

from IOFormat.MarkFile import ProjectFormat, Stream
from CommonHelpers.CommonHelper import create_action, add_actions
from CONSTs.CONST import GadgetDockWidgetState, ToolbarState
from UILayer.CustomWidget.NewProjectDialog import NewProjectDialog
from UILayer.MainWindowPk.MainWindowUi import MainWindowUI
from Manager.ActionManager import ActionManager, Id
from Documents.Document import Document
from Documents.ProjectDocument import FileOpenFailException, ProjectDocument
from UILayer.CustomWidget.PropertyDock import PropertyBrowserDock
from UILayer.MainWindowPk.MainToolBar import MainToolBar, ToolsToolBar
from UILayer.MainWindowPk.NoEditorWidget.noEditorWidget import NoEditorWidget
from UILayer.ProgressBar.Progress import Progress
from Documents.MarkData import Project, MarkItem
from DataDisplay.PieChart import PieChart
from Algorithm.calculation import count_project_data_area, count_project_data_perimeter
from UILayer.CustomWidget.PreferencesWidget.PreferencesDialog import PreferencesDialog
from UILayer.CustomWidget.OpenProjectAsWidget.OpenProjectAsDialog import OpenProjectAsDialog


class WindowStateData(object):

    def __init__(self):
        self.recent_files = []
        self.recent_projects = []


class MainWindow(QMainWindow, MainWindowUI):

    toolbar_gadget_changed_signal = pyqtSignal(ToolbarState)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        super(MainWindow, self)._init_ui(self)
        self.setWindowIcon(QIcon("../Sources/Icons/app-icon.png"))

        self._action_manager = ActionManager.instance(self)
        self._undo_group = QUndoGroup(self)
        self.cmp_browser_dock = None
        self._preferences_dialog = None
        self._undo_widget.set_group(self._undo_group)

        # undo redo action 要重新create
        self.undo_action = self._undo_group.createUndoAction(self)
        self.redo_action = self._undo_group.createRedoAction(self)
        self.undo_action.setText("撤销")
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action.setText("重做")
        self.redo_action.setShortcut("Ctrl+Shift+Z")

        self.edit_menu.insertAction(self.edit_menu.actions()[0], self.undo_action)
        self.edit_menu.insertAction(self.undo_action, self.redo_action)
        self.edit_menu.insertSeparator(self.edit_menu.actions()[2])
        self.__register_actions()

        self._has_editor = False

        self._property_dock = PropertyBrowserDock(parent=self)
        self._property_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._property_dock)
        self.project_dock_widget.current_item_changed_signal.connect(self._property_dock.set_browser)

        self._main_toolbar = MainToolBar(self)
        self.addToolBar(self._main_toolbar)
        self._tools_toolbar = ToolsToolBar(self)

        self._selection_toolbar = self._tools_toolbar.selection_toolbar()
        self._eraser_toolbar = self._tools_toolbar.eraser_toolbar()
        self.toolbar_gadget = ToolbarState.NONE_SELECTED

        self.window_state_data = WindowStateData()
        self._connect_notify()
        self._load_initial_file()
        self._restore_data()
        self.update_actions()

        self._show_no_editor_widget()

    def _init_style(self):
        file = QFile(os.path.join(os.getcwd(), "other/qss/lightblue.qss"))
        if file.open(QFile.ReadOnly):
            qss = file.readAll()
            palette_color = qss.mid(23, 7)
            self.setPalette(QPalette(QColor(str(palette_color))))
            self.setStyleSheet(str(qss))
            file.close()

    def _show_no_editor_widget(self):
        self.project_dock_widget.setHidden(True)
        self._undo_widget.setHidden(True)
        self._property_dock.setHidden(True)

        self._main_toolbar.setHidden(True)
        self._tools_toolbar.setHidden(True)
        # self._selection_toolbar.setHidden(True)
        # self.center_tab_widget.setHidden(True)

        self.menubar.clear()
        self.menubar.addMenu(self.file_menu)
        self.menubar.addMenu(self.edit_menu)
        # self.menubar.addMenu(self.view_menu)
        self.menubar.addMenu(self.help_menu)

        self.save_project_action.setEnabled(False)
        self.save_all_action.setEnabled(False)
        self.save_project_as_action.setEnabled(False)
        self.export_action.setEnabled(False)
        self.import_action.setEnabled(False)
        self.project_info_action.setEnabled(False)
        self.undo_action.setEnabled(False)
        self.redo_action.setEnabled(False)
        self.find_replace_menu.setEnabled(False)

        self._no_editor_widget = NoEditorWidget(self)
        self.setCentralWidget(self._no_editor_widget)
        self._has_editor = False

    def _show_document_widget(self):
        self.project_dock_widget.setHidden(False)
        self._undo_widget.setHidden(False)
        self._property_dock.setHidden(False)
        self._no_editor_widget.setHidden(True)

        self._main_toolbar.setHidden(False)
        self._tools_toolbar.setHidden(False)
        # self._selection_toolbar.setHidden(False)
        # self.center_tab_widget.setHidden(False)

        self.menubar.clear()
        self.menubar.addMenu(self.file_menu)
        self.menubar.addMenu(self.edit_menu)
        self.menubar.addMenu(self.view_menu)
        self.menubar.addMenu(self.project_menu)
        self.menubar.addMenu(self.graph_menu)
        self.menubar.addMenu(self.mark_menu)
        self.menubar.addMenu(self.count_menu)
        self.menubar.addMenu(self.cmp_menu)
        self.menubar.addMenu(self.help_menu)

        self.save_project_action.setEnabled(True)
        self.save_all_action.setEnabled(True)
        self.save_project_as_action.setEnabled(True)
        self.export_action.setEnabled(True)
        self.import_action.setEnabled(True)
        self.project_info_action.setEnabled(True)
        self.find_replace_menu.setEnabled(True)

        # 窗体的中心 使用 QTabWidget # 中心部件
        self.center_tab_widget = QTabWidget(self)
        self.center_tab_widget.setMovable(True)
        self.center_tab_widget.setTabsClosable(True)
        self.center_tab_widget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.center_tab_widget)  # 设置此label为窗口的

        self._property_dock.setBaseSize(200, 600)

        self.center_tab_widget.tabCloseRequested.connect(self.close_file)
        self.center_tab_widget.currentChanged.connect(self.current_document_changed)
        self._has_editor = True

    def update_actions(self, index=-1):
        """TODO"""

    def __register_actions(self):
        ActionManager.register_menu(self.file_menu, Id("File"))
        ActionManager.register_menu(self.edit_menu, Id("Edit"))
        ActionManager.register_menu(self.project_menu, Id("Project"))
        ActionManager.register_menu(self.graph_menu, Id("Graph"))
        ActionManager.register_menu(self.mark_menu, Id("Mark"))
        ActionManager.register_menu(self.cmp_menu, Id("Comp"))
        ActionManager.register_menu(self.help_menu, Id("Help"))
        ActionManager.register_menu(self.view_menu, Id("View"))
        ActionManager.register_menu(self.outline_correction_menu, Id("OutlineCorrection"))

        ActionManager.register_action(self.new_project_action, Id("NewProject"))
        ActionManager.register_action(self.open_project_action, Id("OpenProject"))
        ActionManager.register_action(self.open_original_image_action, Id("OpenOriginalImage"))
        ActionManager.register_action(self.open_project_as_action, Id("OpenProjectAs"))
        ActionManager.register_action(self.save_project_action, Id("SaveProject"))
        ActionManager.register_action(self.save_project_as_action, Id("SaveProjectAs"))
        ActionManager.register_action(self.save_all_action, Id("SaveAll"))
        ActionManager.register_action(self.close_project_action, Id("CloseProject"))
        ActionManager.register_action(self.close_action, Id("Close"))
        ActionManager.register_action(self.close_all_action, Id("CloseALl"))
        ActionManager.register_action(self.import_action, Id("Import"))
        ActionManager.register_action(self.export_action, Id("Export"))
        ActionManager.register_action(self.project_info_action, Id("ProjectInfo"))
        ActionManager.register_action(self.quit_action, Id("Quit"))
        ActionManager.register_action(self.undo_action, Id("Undo"))
        ActionManager.register_action(self.redo_action, Id("Redo"))
        ActionManager.register_action(self.reference_action, Id("Reference"))
        ActionManager.register_action(self.quick_find_action, Id("QuickFind"))
        ActionManager.register_action(self.quick_replace_action, Id("QuickReplace"))
        ActionManager.register_action(self.quick_find_in_file_action, Id("QuickFindInFile"))
        ActionManager.register_action(self.quick_replace_in_file_action, Id("QuickReplaceInFile"))
        ActionManager.register_action(self.new_mark_action, Id("NewMark"))
        ActionManager.register_action(self.new_mark_from_action, Id("NewMarkFrom"))
        ActionManager.register_action(self.size_action, Id("Size"))
        ActionManager.register_action(self.bmp_action, Id("Bmp"))
        ActionManager.register_action(self.gray_action, Id("Gray"))
        ActionManager.register_action(self.rgb_action, Id("RGB"))
        ActionManager.register_action(self.bright_action, Id("Bright"))
        ActionManager.register_action(self.rotate_180_action, Id("Rotate180"))
        ActionManager.register_action(self.rotate_clockwise90_action, Id("RotateClockwise90"))
        ActionManager.register_action(self.rotate_counterclockwise90_action, Id("RotateCounterClockwise90"))
        ActionManager.register_action(self.rotate_any_action, Id("RotateAny"))
        ActionManager.register_action(self.rectangle_action, Id("Rectangle"))
        ActionManager.register_action(self.polygon_action, Id("Polygon"))
        ActionManager.register_action(self.origin_outline_action, Id("OriginOutline"))
        ActionManager.register_action(self.convex_outline_action, Id("ConvexOutline"))
        ActionManager.register_action(self.polygon_outline_action, Id("PolygonOutline"))
        ActionManager.register_action(self.woodland_outline_action, Id("AiOutline"))
        ActionManager.register_action(self.as_outline_action, Id("AsOutline"))

        ActionManager.register_action(self.add_outline_correction, Id("AddOutlineCorrection"))
        ActionManager.register_action(self.remove_outline_correction, Id("RemoveOutlineCorrection"))

        ActionManager.register_action(self.erosion_area_action, Id("ErosionArea"))
        ActionManager.register_action(self.girth_area_action, Id("GirthArea"))
        ActionManager.register_action(self.cmp_history_action, Id("CmpHistory"))
        ActionManager.register_action(self.help_about_action, Id("HelpAbout"))
        ActionManager.register_action(self.help_help_action, Id("HelpHelp"))

        ActionManager.register_action(self.delete_mark_item_action, Id("DeleteMarkItem"))

        ActionManager.register_action(self.project_dock_action, Id("ProjectDock"))
        ActionManager.register_action(self.property_dock_action, Id("PropertyDock"))
        ActionManager.register_action(self.history_dock_action, Id("HistoryDock"))

    def _restore_data(self):
        settings = QSettings()
        self.window_state_data.recent_files = settings.value("recent_files", [])
        self.window_state_data.recent_projects = settings.value("project_files", [])

        if not self.window_state_data.recent_files:
            self.window_state_data.recent_files = []
        if not self.window_state_data.recent_projects:
            self.window_state_data.recent_projects = []
        # if window_state is not None:
        #     self.restoreState(window_state)
        QTimer.singleShot(0, self._load_initial_file)

    def _load_initial_file(self):
        pass

    def _connect_notify(self):
        """
        统一进行窗口组件事件信号的和槽函数连接
        """

        self.file_menu.aboutToShow.connect(self.update_file_menu)
        self.new_project_action.triggered.connect(self.create_new_project)
        self.open_original_image_action.triggered.connect(self.open_file)
        self.open_project_as_action.triggered.connect(self.open_project_as)
        self.save_project_action.triggered.connect(self.save_project)
        self.open_project_action.triggered.connect(self.open_project)
        self.close_all_action.triggered.connect(self.close_all_file)
        self.quit_action.triggered.connect(self.close)
        self.export_action.triggered.connect(self.export_result)

        self.cmp_history_action.triggered.connect(self.cmp_history)
        self.polygon_outline_action.triggered.connect(self.polygon_outline_detect)
        self.convex_outline_action.triggered.connect(self.polygon_outline_detect)
        self.origin_outline_action.triggered.connect(self.polygon_outline_detect)
        self.woodland_outline_action.triggered.connect(self.polygon_outline_detect)
        self.as_outline_action.triggered.connect(self.polygon_outline_detect)

        self.add_outline_correction.triggered.connect(self.outline_correction)
        self.remove_outline_correction.triggered.connect(self.outline_correction)

        self.project_dock_widget.double_click_mark_item.connect(self.select_pro_or_item)
        self.project_dock_widget.delete_mark_item_signal.connect(self.delete_mark_item)

        self.erosion_area_action.triggered.connect(self.show_marked_erosion)
        self.girth_area_action.triggered.connect(self.show_marked_girth)

        self.project_dock_action.toggled.connect(lambda is_on: self.project_dock_widget.setHidden(not is_on))
        self.property_dock_action.toggled.connect(lambda is_on: self._property_dock.setHidden(not is_on))
        self.history_dock_action.toggled.connect(lambda is_on: self._undo_widget.setHidden(not is_on))
        self.project_dock_widget.close_event_signal.connect(self.project_dock_action.setChecked)
        self._property_dock.close_event_signal.connect(self.property_dock_action.setChecked)
        self._undo_widget.close_event_signal.connect(self.history_dock_action.setChecked)

        self.reference_action.triggered.connect(self.open_preferences_dialog)

    def show_marked_erosion(self):
        current_doc = self.center_tab_widget.currentWidget()
        if isinstance(current_doc, Document):
            project = current_doc.project()
            project_data = count_project_data_area(project)
            pie_widget = PieChart("面积饼图", project_data, self)
            pie_widget.show()

    def show_marked_girth(self):
        current_doc = self.center_tab_widget.currentWidget()
        if isinstance(current_doc, Document):
            project = current_doc.project()
            project_data = count_project_data_perimeter(project)
            pie_widget = PieChart("周长饼图", project_data, self)
            pie_widget.show()

    def select_pro_or_item(self, project: Project, mark_item: MarkItem):
        count = self.center_tab_widget.count()
        for index in range(count):
            document = self.center_tab_widget.widget(index)
            if document.project() == project:
                document.set_current_mark_item(mark_item)
                if document != self.center_tab_widget.currentWidget():
                    self.center_tab_widget.setCurrentWidget(document)

    def delete_mark_item(self, project: Project, mark_item: MarkItem):
        count = self.center_tab_widget.count()
        for index in range(count):
            document = self.center_tab_widget.widget(index)
            if document.project() == project:
                document.delete_mark_item(mark_item)

    def save_project(self):
        current_document = self.center_tab_widget.currentWidget()
        if current_document and isinstance(current_document, Document):
            try:
                current_document.save_project()
            except Exception as e:
                print(e)

    def open_project(self):
        dir_ = os.path.dirname(self.window_state_data.recent_files[0]) \
            if self.window_state_data.recent_files else os.path.dirname(".")
        file_format = "IProject files " + Stream.formats()
        file_name = QFileDialog.getOpenFileName(self, "选择标注项目", dir_, file_format)[0]

        if file_name:
            is_open, index = self.is_open_this(file_name)
            if not is_open:
                message = self.create_document_by_project_path(file_name)
            else:
                message = "项目 %s 已经打开" % file_name
                self.center_tab_widget.setCurrentIndex(index)
            self.statusBar().showMessage(message, 5000)

    def open_project_as(self):
        image_last_dir = os.path.dirname(self.window_state_data.recent_files[0]) \
            if self.window_state_data.recent_files else os.path.dirname(".")

        message = "   "
        open_project_as_dialog = OpenProjectAsDialog(img_last_dir=image_last_dir, parent=self)
        if open_project_as_dialog.exec_():
            project_path, image_path, is_changed_img_path = open_project_as_dialog.get_project_info()
            is_open, index = self.is_open_this(project_path)
            if not is_open:
                message = self.create_document_by_other_img_path(project_path, image_path, is_changed_img_path)
            else:
                message = "项目 %s 已经打开" % project_path
                self.center_tab_widget.setCurrentIndex(index)
        self.statusBar().showMessage(message, 5000)

    def closeEvent(self, event):
        if self._has_editor:
            if self.ok_to_continue():
                self.save_window_state()
            else:
                event.ignore()
        else:
            self.save_window_state()

    def save_window_state(self):
        settings = QSettings()
        # 最近打开文件
        recently_files = QVariant(self.window_state_data.recent_files) \
            if self.window_state_data.recent_files else QVariant()
        recently_projects = QVariant(self.window_state_data.recent_projects) \
            if self.window_state_data.recent_projects else QVariant()
        settings.setValue("recent_files", recently_files)
        settings.setValue("project_files", recently_projects)
        # 主窗口的其他状态
        settings.setValue("main_window/state", QVariant(self.saveState()))

    # 用户关闭窗口前提问
    def ok_to_continue(self):
        tab_num = self.center_tab_widget.count()
        for _ in range(tab_num):
            if not self.close_file(index=0):
                return False
        return True

    def is_save_question(self, file_name):
        tip_text = "要在退出前保存对 图片\"" + os.path.basename(file_name) + "\"的更改吗？"
        reply = QMessageBox.question(
            self, "遥感地图标注 - 未保存提示", tip_text,
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return False
        elif reply == QMessageBox.Yes:
            # 保存文件 待写
            """TODO"""
            return True
        else:
            return True

    def update_file_menu(self):
        self.file_menu.clear()
        self.file_menu.addAction(self.file_menu_actions[0])
        self.file_menu.addAction(self.file_menu_actions[1])
        self.file_menu.addAction(self.file_menu_actions[2])

        self.file_menu.addSeparator()
        recent_files_menu = self.file_menu.addMenu("打开最近的文件(T)...")
        if self.window_state_data.recent_files:
            for i, project_name in enumerate(self.window_state_data.recent_files):
                dir_file_name = os.path.basename(project_name)
                action = create_action(
                    parent=recent_files_menu,
                    text=str(i + 1) + " " + dir_file_name,
                    slot=self._open_file_from_recent)
                action.setData(QVariant(project_name))
                recent_files_menu.addAction(action)
            recent_files_menu.addSeparator()
        remove_action = create_action(
            parent=recent_files_menu,
            text="清空最近打开的文件列表",
            slot=self.remove_recent_files)
        recent_files_menu.addAction(remove_action)

        recent_project_menu = self.file_menu.addMenu("打开最近的项目(P)...")
        if self.window_state_data.recent_projects:
            for i, project_name in enumerate(self.window_state_data.recent_projects):
                dir_file_name = os.path.basename(project_name)
                action = create_action(
                    parent=recent_project_menu,
                    text=str(i + 1) + " " + dir_file_name,
                    slot=self._open_project_from_recent)
                action.setData(QVariant(project_name))
                recent_project_menu.addAction(action)
            recent_project_menu.addSeparator()
        remove_action = create_action(
            parent=recent_files_menu,
            text="清空最近打开的项目列表",
            slot=self.remove_recent_project)
        recent_project_menu.addAction(remove_action)
        self.file_menu.addSeparator()
        add_actions(self.file_menu, self.file_menu_actions[3:])

    def remove_recent_files(self):
        self.window_state_data.recent_files.clear()

    def add_recent_file(self, file_name):
        if file_name:
            if file_name in self.window_state_data.recent_files:
                self.window_state_data.recent_files.remove(file_name)
            self.window_state_data.recent_files.insert(0, file_name)
            while len(self.window_state_data.recent_files) > 9:
                print(self.window_state_data.recent_files.pop())

    def remove_recent_project(self):
        self.window_state_data.recent_projects.clear()

    def add_recent_file_project(self, project_name):
        if project_name:
            if project_name in self.window_state_data.recent_projects:
                self.window_state_data.recent_projects.remove(project_name)
            self.window_state_data.recent_projects.insert(0, project_name)
            while len(self.window_state_data.recent_projects) > 9:
                print(self.window_state_data.recent_projects.pop())

    def open_file(self, file_name=None):
        if file_name is None or isinstance(file_name, bool):
            dir_ = os.path.dirname(self.window_state_data.recent_files[0]) \
                if self.window_state_data.recent_files else os.path.dirname(".")
            # 打开一个 文件选择对口框
            file_format = "Image files " + Stream.support_image_formats()
            file_name = QFileDialog.getOpenFileName(self, "选择遥感图片", dir_, file_format)[0]

        if file_name:
            file_names = []
            for index in range(self.center_tab_widget.count()):
                file_names.append(self.center_tab_widget.widget(index).get_file_name())

            if file_name not in file_names:
                """"""
                # message = self.create_new_tab(file_name)
            else:
                message = "文件 %s 已经打开" % file_name
                self.center_tab_widget.setCurrentIndex(file_names.index(file_name))
            self.statusBar().showMessage(message, 5000)

    def create_new_project(self):
        image_last_dir = os.path.dirname(self.window_state_data.recent_files[0]) \
            if self.window_state_data.recent_files else os.path.dirname(".")
        new_project_dialog = NewProjectDialog(img_last_dir=image_last_dir, parent=self)
        if new_project_dialog.exec_():
            self.setCursor(Qt.BusyCursor)
            project_name, project_dir, image_file, person = new_project_dialog.new_project_info()
            self.create_document(project_name, project_dir, image_file, person)
            self.setCursor(Qt.ArrowCursor)

    def _open_file_from_recent(self):
        sender = self.sender()
        if isinstance(sender, QAction):
            file_name = sender.data()
            self.open_file(file_name)

    def _open_project_from_recent(self):
        sender = self.sender()
        if isinstance(sender, QAction):
            file_name = sender.data()
            if not os.path.exists(file_name):
                QMessageBox.critical(self, "打开最近文件", "找不到项目：" + file_name)
                return
            is_open, index = self.is_open_this(file_name)
            if not is_open:
                self.create_document_by_project_path(file_name)
            else:
                self.center_tab_widget.setCurrentIndex(index)

    def close_file(self, index=None):
        if index is not None and isinstance(index, int):
            tab_widget = self.center_tab_widget.widget(index)
            if tab_widget.modifier():
                if not self.is_save_question(tab_widget.get_file_name()):
                    return False

            self.project_dock_widget.close_project(tab_widget.project())

            self.center_tab_widget.removeTab(index)
            self._undo_group.removeStack(tab_widget.undo_stack())
            if tab_widget.project().contain_browser(self._property_dock.get_browser()):
                self._property_dock.set_browser(None)

            tab_widget.disconnect()
            del tab_widget

        if index and isinstance(index, bool) and self.center_tab_widget.count() != 0:
            current_index = self.center_tab_widget.currentIndex()
            current_widget = self.center_tab_widget.currentWidget()
            if current_widget.is_dirty():
                if self.is_save_question(current_index):
                    self.center_tab_widget.removeTab(current_index)
                    del current_widget
        self.update_close_button_enabled()
        if self.center_tab_widget.count() == 0:
            self._show_no_editor_widget()
        return True

    def close_all_file(self):
        self.ok_to_continue()

    def open_history_project(self):
        dir_ = os.path.dirname(self.window_state_data.recent_files[0]) \
            if self.window_state_data.recent_files else os.path.dirname(".")

        file_format = "Project files (*.mfb)"
        file_names = QFileDialog.getOpenFileNames(self, "选择遥感图片", dir_, file_format)[0]

        if file_names:
            project_format = ProjectFormat()
            project_documents = []
            for file in file_names:
                if not os.path.exists(file):
                    continue
                if file == self.center_tab_widget.currentWidget().get_file_name():
                    continue
                project = ProjectDocument(project_format.read_project(file))
                if not project:
                    continue
                project_documents.append(project)
            return project_documents
        else:
            return None

    def cmp_history(self):
        try:
            current_doc = self.center_tab_widget.currentWidget()
            if current_doc.had_cmp():
                current_doc.about_to_cmp()
            else:
                project_documents = self.open_history_project()
                if not project_documents:
                    return
                current_doc.about_to_cmp(project_documents)
        except Exception as e:
            QMessageBox.critical(self, "打开历史项目", "打开历史记录失败：" + e.__str__())

    def count_area(self, outline_array: tuple, ratio: int) -> float:
        """
        :param outline_array: 轮廓的像素的矩阵
        :param ratio: 图像的分辨率 以米为单位
        :return: float类型的面积
        """
        pass

    def polygon_outline_detect(self):
        current_tab = self.center_tab_widget.currentWidget()
        outline_type = self.sender().data()
        if current_tab and isinstance(current_tab, Document):
            try:
                current_tab.detect_outline(outline_type)
            except Exception as e:
                print(e)

    def outline_correction(self):
        current_tab = self.center_tab_widget.currentWidget()
        correction_option = self.sender().data()
        if current_tab and isinstance(current_tab, Document):
            current_tab.correction_outline(correction_option)

    def adjust_image_size(self):
        current_tab = self.center_tab_widget.currentWidget()
        option_type = self.sender().data()
        if current_tab and isinstance(current_tab, Document):
            current_tab.adjust_size(option_type)

    def gadget_changed(self, gadget: GadgetDockWidgetState):
        if gadget in (GadgetDockWidgetState.RECTANGLE_SELECT_TOOL, GadgetDockWidgetState.ELLIPSE_SELECT_TOOL):
            self.quick_select_toolbar.setHidden(False)
            self.quick_select_toolbar.setEnabled(True)
            self.zoom_toolbar.setHidden(True)
        elif gadget == GadgetDockWidgetState.ZOOM_TOOL:
            self.zoom_toolbar.setHidden(False)
            self.zoom_toolbar.setEnabled(True)
            self.quick_select_toolbar.setHidden(True)
        else:
            self.zoom_toolbar.setEnabled(False)
            self.quick_select_toolbar.setEnabled(False)

    def toolbar_gadget_changed(self):
        self.toolbar_gadget = self.sender().data()
        self.toolbar_gadget_changed_signal.emit(self.toolbar_gadget)

    def current_document_changed(self, index: int):
        current_doc = self.center_tab_widget.currentWidget()
        if current_doc:
            self._undo_widget.set_stack(current_doc.undo_stack())
            self._undo_group.setActiveStack(current_doc.undo_stack())
            self.update_actions(index)

    def undo(self):
        """"""
        # current_tab = self.center_tab_widget.currentWidget()
        # current_tab.undo()

    def redo(self):
        """"""
        # current_tab = self.center_tab_widget.currentWidget()
        # current_tab.redo()

    def export_result(self):
        current_doc = self.center_tab_widget.currentWidget()
        if current_doc and isinstance(current_doc, Document):
            path, file_name = QFileDialog.getSaveFileName(
                self, "导出tif", current_doc.get_project_name(),
                "Images (*.tif)", self.window_state_data.recent_projects[0]
            )
            _progress = Progress()
            _progress.setHidden(True)
            current_doc.export_result(path, _progress)

    def open_preferences_dialog(self):

        self._preferences_dialog = PreferencesDialog(self)
        self._preferences_dialog.setAttribute(Qt.WA_DeleteOnClose)
        self._preferences_dialog.show()
        self._preferences_dialog.activateWindow()
        self._preferences_dialog.raise_()

    # ####################################################################################################

    def is_open_this(self, file_name):
        if self._has_editor:
            file_names = []
            for index in range(self.center_tab_widget.count()):
                file_names.append(self.center_tab_widget.widget(index).get_file_name())
            if file_name in file_names:
                return True, file_names.index(file_name)
            else:
                return False, -1
        else:
            return False, -1

    def update_close_button_enabled(self):
        is_tab_empty = self.center_tab_widget.count() != 0
        self.file_menu_actions[5].setEnabled(is_tab_empty)
        self.file_menu_actions[6].setEnabled(is_tab_empty)
        self.file_menu_actions[7].setEnabled(is_tab_empty)

    def create_document_by_project_path(self, project_path):

        reader_format = ProjectFormat()
        project = reader_format.read_project(project_path)

        if not project:
            return ""
        if not os.path.exists(project.image_path):
            QMessageBox.critical(self, "打开最近文件", "找不到原始图片：" + project_path)
            return ""

        new_doc = Document(
            image_path=project.image_path,
            gadget=self._tools_toolbar.current_tools(),
            toolbar_gadget=self._selection_toolbar.current_selection_option(),
            eraser_size=self._eraser_toolbar.current_eraser_size(),
        )
        new_doc.reader_format = reader_format
        return self.open_document(project, new_doc)

    def create_document_by_other_img_path(self, project_path, image_path, is_change_img_path):
        reader_format = ProjectFormat()
        project = reader_format.read_project(project_path)

        if not project:
            return " "

        if is_change_img_path:
            project.image_path = image_path
            reader_format.save_project(project)

        new_doc = Document(
            image_path=image_path,
            gadget=self._tools_toolbar.current_tools(),
            toolbar_gadget=self._selection_toolbar.current_selection_option(),
            eraser_size=self._eraser_toolbar.current_eraser_size(),
        )
        new_doc.reader_format = reader_format
        return self.open_document(project, new_doc)

    def open_document(self, project:Project, new_doc: Document):

        if not self._has_editor:
            self._show_document_widget()

        self.project_dock_widget.create_project(project)
        new_doc.added_mark_item.connect(self.project_dock_widget.add_mark_item)
        new_doc.selected_mark_item_changed.connect(self.project_dock_widget.selected_mark_changed)
        new_doc.set_project(project)

        self._tools_toolbar.tools_changed.connect(new_doc.change_gadget)
        self._selection_toolbar.selection_option_changed.connect(new_doc.change_toolbar_gadget)
        self._eraser_toolbar.eraser_size_changed.connect(new_doc.eraser_size_changed)
        self.add_document(new_doc)
        return " "

    def create_document(self, project_name, file_mame, image_path, person):
        try:
            new_doc = Document(
                gadget=self._tools_toolbar.current_tools(),
                toolbar_gadget=self._selection_toolbar.current_selection_option(),
                eraser_size=self._eraser_toolbar.current_eraser_size(),
                file_name=file_mame,
                project_name=project_name,
                image_path=image_path,
                person_name=person
            )
            project = new_doc.project()
            self.project_dock_widget.create_project(project)
            new_doc.added_mark_item.connect(self.project_dock_widget.add_mark_item)
            new_doc.selected_mark_item_changed.connect(self.project_dock_widget.selected_mark_changed)

            if not self._has_editor:
                self._show_document_widget()

            self._tools_toolbar.tools_changed.connect(new_doc.change_gadget)
            self._eraser_toolbar.eraser_size_changed.connect(new_doc.eraser_size_changed)
            self._selection_toolbar.selection_option_changed.connect(new_doc.change_toolbar_gadget)

            self.add_document(new_doc)
            return "打开文件\"" + file_mame + "\"成功"

        except FileOpenFailException as e:
            print(e.message)
            return e.message
        except AttributeError as e:
            QMessageBox.critical(self, "创建项目", "创建项目失败：" + e.__str__())
            return " "
        except Exception as e:
            QMessageBox.critical(self, "创建项目", "创建项目失败：" + e.__str__())
            return " "

    def add_document(self, document: Document):
        self._undo_group.addStack(document.undo_stack())
        index = self.center_tab_widget.addTab(document, document.project_name())
        self.center_tab_widget.setTabToolTip(index, document.project().project_full_path())
        document.undo_stack().indexChanged.connect(self.update_actions)
        document.undo_stack().cleanChanged.connect(self.update_actions)
        self.add_recent_file_project(document.project().project_full_path())
        self.set_current_document(document)
        self._undo_widget.set_stack(document.undo_stack())
        self._undo_group.setActiveStack(document.undo_stack())
        self._property_dock.set_browser(document.project().browser)

    def set_current_document(self, document: Document):
        self.center_tab_widget.setCurrentWidget(document)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("LRSM Ltd.")
    app.setOrganizationDomain("lrsm.eu")
    app.setApplicationName("LRSMSingleVersion")
    form = MainWindow()
    form.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    cache_size_in_kb = 700 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)  # 将缓存设置为700000千字节（684Mb左右）
    main()
