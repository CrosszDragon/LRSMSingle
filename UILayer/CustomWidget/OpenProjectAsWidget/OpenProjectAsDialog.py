# -*- coding: utf-8 -*-
# @Time    : 2019/7/24 13:26
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : OpenProjectAsDialog.py
# @Project : LSRMSingle
# @Software: PyCharm

import os
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFileDialog
from PyQt5.QtCore import Qt
from UILayer.CustomWidget.OpenProjectAsWidget.OpenProjectAsDialogUi import UiOpenProjectAsDialog
from IOFormat.MarkFile import Stream


class OpenProjectAsDialog(QDialog, UiOpenProjectAsDialog):

    def __init__(self, pro_last_dir="./", img_last_dir="./", parent=None):
        QDialog.__init__(self, parent)
        self._setupUi(self)

        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        self.setWindowTitle("打开项目为")
        self.setFixedSize(530, 180)

        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")

        self._pro_last_dir = pro_last_dir
        self._img_last_dir = img_last_dir

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.project_location_edit.textChanged.connect(self._set_ok_btn_enabled)
        self.image_location_edit.textChanged.connect(self._set_ok_btn_enabled)

        self.project_location_btn.clicked.connect(self._select_project)
        self.image_location_btn.clicked.connect(self._select_image)

    def get_project_info(self):
        return self.project_location_edit.text(), self.image_location_edit.text(), \
               self.change_img_location_checkbox.isChecked()

    def _set_ok_btn_enabled(self):

        project_file = self.project_location_edit.text()
        image_file = self.image_location_edit.text()

        enable = os.path.exists(project_file) and os.path.exists(image_file) and \
            Stream.support_format_with(os.path.splitext(os.path.basename(project_file))[-1]) and \
            Stream.support_image_format_with(os.path.splitext(os.path.basename(image_file))[-1])

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def _select_project(self):
        project_format = "Project files " + Stream.formats()
        project_file = QFileDialog.getOpenFileName(self, "选择项目", self._pro_last_dir, project_format)[0]
        self.project_location_edit.setText(project_file)

    def _select_image(self):
        file_format = "Image files " + Stream.support_image_formats()
        image_file = QFileDialog.getOpenFileName(self, "选择原始图片", self._img_last_dir, file_format)[0]
        self.image_location_edit.setText(image_file)
