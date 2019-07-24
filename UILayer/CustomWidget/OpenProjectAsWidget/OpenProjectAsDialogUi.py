# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OpenProjectAsDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class UiOpenProjectAsDialog(object):
    def _setupUi(self, OpenProjectAsDialog):
        OpenProjectAsDialog.setObjectName("OpenProjectAsDialog")
        OpenProjectAsDialog.resize(530, 181)
        self.verticalLayout = QtWidgets.QVBoxLayout(OpenProjectAsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(OpenProjectAsDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.image_location_btn = QtWidgets.QPushButton(OpenProjectAsDialog)
        self.image_location_btn.setObjectName("image_location_btn")
        self.gridLayout.addWidget(self.image_location_btn, 1, 3, 1, 1)
        self.project_location_edit = QtWidgets.QLineEdit(OpenProjectAsDialog)
        self.project_location_edit.setObjectName("project_location_edit")
        self.gridLayout.addWidget(self.project_location_edit, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(OpenProjectAsDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.project_location_btn = QtWidgets.QPushButton(OpenProjectAsDialog)
        self.project_location_btn.setObjectName("project_location_btn")
        self.gridLayout.addWidget(self.project_location_btn, 0, 3, 1, 1)
        self.image_location_edit = QtWidgets.QLineEdit(OpenProjectAsDialog)
        self.image_location_edit.setObjectName("image_location_edit")
        self.gridLayout.addWidget(self.image_location_edit, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.change_img_location_checkbox = QtWidgets.QCheckBox(OpenProjectAsDialog)
        self.change_img_location_checkbox.setObjectName("change_img_location_checkbox")
        self.verticalLayout.addWidget(self.change_img_location_checkbox)
        self.buttonBox = QtWidgets.QDialogButtonBox(OpenProjectAsDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(OpenProjectAsDialog)
        QtCore.QMetaObject.connectSlotsByName(OpenProjectAsDialog)

    def retranslateUi(self, OpenProjectAsDialog):
        _translate = QtCore.QCoreApplication.translate
        OpenProjectAsDialog.setWindowTitle(_translate("OpenProjectAsDialog", "Dialog"))
        self.label.setText(_translate("OpenProjectAsDialog", "项目路径："))
        self.image_location_btn.setText(_translate("OpenProjectAsDialog", "浏览..."))
        self.label_2.setText(_translate("OpenProjectAsDialog", "图片路径："))
        self.project_location_btn.setText(_translate("OpenProjectAsDialog", "浏览..."))
        self.change_img_location_checkbox.setText(_translate("OpenProjectAsDialog", "以该图片路径作为项目原始图片的路径"))


