# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NoEditorWidgetUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets
from Manager.ActionManager import ActionManager
from Manager.Id import Id
from UILayer.MainWindowPk.NoEditorWidget.NoEditorWidgetUi import Ui_NoEditorWidget


class NoEditorWidget(QtWidgets.QWidget, Ui_NoEditorWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        super(NoEditorWidget, self).setupUi(self)

        self.new_project_button.clicked.connect(ActionManager.action(Id("NewProject")).trigger)
        self.open_project_btn.clicked.connect(ActionManager.action(Id("OpenProject")).trigger)
        # self.open_image_btn.clicked.connect(ActionManager.action(Id("OpenOriginalImage")).trigger)

        self.open_image_btn.setEnabled(False)


if __name__ == '__main__':
    import sys

    ActionManager.instance()
    app = QtWidgets.QApplication(sys.argv)
    no_editor_widget = NoEditorWidget()
    no_editor_widget.showMaximized()
    app.exec_()
