# -*- coding: utf-8 -*-
# @Time    : 2019/6/30 19:56
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : DocumentManager.py
# @Project : LSRMSingalVersion2
# @Software: PyCharm

from PyQt5.QtWidgets import QUndoGroup, QWidget, QStackedLayout, QTabBar, QVBoxLayout
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QPoint

from NoEditorWidget.noEditorWidget import NoEditorWidget
import MapEditor as Editors
from Document import Document


class DocumentManager(QObject):
    """
     单例模式， 维护所有的项目及其变化并负责界面的布局，工具栏，undo_group
    """

    current_document_changed = pyqtSignal(Document)
    document_close_requested = pyqtSignal(int)

    __instance = None

    def __init__(self, parent=None):
        if not DocumentManager.__instance:
            QObject.__init__(self, parent)

            self._widget = QWidget()
            self._no_editor_widget = NoEditorWidget(self._widget)
            self._tab_bar = QTabBar(self._widget)
            self._undo_group = QUndoGroup(self)
            self._map_editor = None
            self._editor_for_type = {}

            self._tab_bar.setExpanding(False)
            self._tab_bar.setDocumentMode(True)
            self._tab_bar.setTabsClosable(True)
            self._tab_bar.setMovable(True)
            self._tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)

            vertical_layout = QVBoxLayout(self._widget)
            vertical_layout.addWidget(self._tab_bar)
            vertical_layout.setSpacing(0)

            self._editor_stack = QStackedLayout()
            self._editor_stack.addWidget(self._no_editor_widget)
            vertical_layout.addLayout(self._editor_stack)

            self._notify_connect()
            self._tab_bar.installEventFilter(self)
            DocumentManager.__instance = self

        else:
            raise SyntaxError("该类是个单例类，请同函数instance()获取其实例")

    @staticmethod
    def instance():
        if DocumentManager.__instance is None:
            DocumentManager.__instance = DocumentManager()
        return DocumentManager.__instance

    def __del__(self):
        self._tab_bar.removeEventFilter(self)
        del self._widget

    def _notify_connect(self):
        self._tab_bar.currentChanged.connect(self.__current_index_changed)
        self._tab_bar.tabCloseRequested.connect(self.document_close_requested)
        self._tab_bar.tabMoved.connect(self.__document_tab_moved)

        self._tab_bar.customContextMenuRequested.connect(self.__tab_context_menu_requested)

    def __tab_context_menu_requested(self, pos: QPoint):
        """TODO"""

    def __document_tab_moved(self, from_index: int, to_index: int):
        """TODO"""

    def __current_index_changed(self, index: int):
        """TODO"""

    def set_editor(self, document_type: Document.DocumentType, editor):
        if document_type not in self._editor_for_type:
            self._editor_for_type[document_type] = editor
            self._editor_stack.addWidget(editor.editor_widget())

            if isinstance(editor, Editors.MapEditor):
                self._map_editor = editor

    def editor(self, document_type: Document.DocumentType):
        try:
            return self._editor_for_type[document_type]
        except KeyError:
            return None

    def widget(self) -> QWidget:
        return self._widget

    @staticmethod
    def save_file():
        """TODO"""

    @property
    def undo_group(self) -> QUndoGroup:
        return self._undo_group
