# -*- coding: utf-8 -*-
# @Time    : 2019/7/20 16:24
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : PreferencesDialog.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QEvent

from WindowStyle.Preferences import ApplicationStyle, Preferences
from UILayer.CustomWidget.PreferencesWidget.preferencesUi import UiPreferencesDialog


class PreferencesDialog(QDialog, UiPreferencesDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self._setupUi(self)
        self.setWindowTitle("首选项")

        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

        self.style_combobox.addItems(["本机", "Fusion", "lrsm"])
        self.style_combobox.setItemData(0, ApplicationStyle.SystemDefaultStyle)
        self.style_combobox.setItemData(1, ApplicationStyle.FusionStyle)
        self.style_combobox.setItemData(2, ApplicationStyle.FusionStyle)

        self._from_preferences()
        self._notify_connect()
        self.resize(self.sizeHint())

    def _notify_connect(self):
        preferences = Preferences.instance()
        self.style_combobox.currentIndexChanged.connect(self._style_changed)
        self.base_color_btn.color_changed_signal.connect(preferences.set_base_color)
        self.selection_color_btn.color_changed_signal.connect(preferences.set_selection_color)
        self.buttonBox.clicked.connect(self.close)

    def changeEvent(self, event: QEvent):
        QDialog.changeEvent(self, event)

        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)

    def _from_preferences(self):
        preferences = Preferences.instance()
        style_index = self.style_combobox.findData(preferences.application_style())
        style_index = 1 if style_index == -1 else style_index

        self.style_combobox.setCurrentIndex(style_index)
        self.base_color_btn.color = preferences.base_color()
        self.selection_color_btn.color = preferences.selection_color()

        is_system_style = preferences.application_style() == ApplicationStyle.SystemDefaultStyle
        self.base_color_btn.setEnabled(not is_system_style)
        self.label_5.setEnabled(not is_system_style)
        self.selection_color_btn.setEnabled(not is_system_style)
        self.label_6.setEnabled(not is_system_style)

    def _style_changed(self):
        preferences = Preferences.instance()

        current_style = self.style_combobox.currentData()
        preferences.set_application_style(current_style)

        is_system_style = preferences.application_style() == ApplicationStyle.SystemDefaultStyle
        self.base_color_btn.setEnabled(not is_system_style)
        self.label_5.setEnabled(not is_system_style)
        self.selection_color_btn.setEnabled(not is_system_style)
        self.label_6.setEnabled(not is_system_style)
