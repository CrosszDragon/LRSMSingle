# -*- coding: utf-8 -*-
# @Time    : 2019/7/1 19:15
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : NoEditorWidgetUi.py
# @Project : LSRMSingalVersion2
# @Software: PyCharm


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NoEditorWidget(object):
    def setupUi(self, noEditorWidget):
        noEditorWidget.setObjectName("NoEditorWidget")
        noEditorWidget.setWindowModality(QtCore.Qt.NonModal)
        noEditorWidget.resize(405, 401)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(noEditorWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.title = QtWidgets.QLabel(noEditorWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.open_project_btn = QtWidgets.QPushButton(noEditorWidget)
        self.open_project_btn.setObjectName("open_project_btn")
        self.horizontalLayout.addWidget(self.open_project_btn)
        self.open_image_btn = QtWidgets.QPushButton(noEditorWidget)
        self.open_image_btn.setObjectName("open_image_btn")
        self.horizontalLayout.addWidget(self.open_image_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.new_project_button = QtWidgets.QPushButton(noEditorWidget)
        self.new_project_button.setObjectName("new_project_button")
        self.verticalLayout_2.addWidget(self.new_project_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)

        self.retranslateUi(noEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(noEditorWidget)

    def retranslateUi(self, NoEditorWidget):
        _translate = QtCore.QCoreApplication.translate
        NoEditorWidget.setWindowTitle(_translate("NoEditorWidget", "Form"))
        self.title.setText(_translate("NoEditorWidget", "没有打开的文件"))
        self.open_project_btn.setText(_translate("NoEditorWidget", "打开项目..."))
        self.open_image_btn.setText(_translate("NoEditorWidget", "打开图片..."))
        self.new_project_button.setText(_translate("NoEditorWidget", "新建项目"))
