# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 23:43
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : CustomColorEditorFactory.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import pyqtSignal
from lib.QtProperty.qteditorfactory import EditorFactoryPrivate, QtPropertyBrowserUtils, \
    registerEditorFactory, QtAbstractEditorFactory


class MyColorEditWidget(QWidget):
    valueChangedSignal = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super(MyColorEditWidget, self).__init__(parent)

        self.m_color = QColor()
        self.m_pixmapLabel = QLabel()
        self.m_pixmapLabel.setPixmap(QtPropertyBrowserUtils.brushValuePixmap(QBrush(self.m_color)))

    def setValue(self, c):
        if (self.m_color != c):
            self.m_color = c
            self.m_pixmapLabel.setPixmap(QtPropertyBrowserUtils.brushValuePixmap(QBrush(c)))


class MyColorEditorFactoryPrivate(EditorFactoryPrivate):

    def __init__(self):
        super(MyColorEditorFactoryPrivate, self).__init__()
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.setValue(value)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return


registerEditorFactory(MyColorEditorFactoryPrivate, MyColorEditWidget)


class CustomColorEditorFactory(QtAbstractEditorFactory):

    def __init__(self, parent=None):
        super(CustomColorEditorFactory, self).__init__(parent)

        self.d_ptr = MyColorEditorFactoryPrivate()
        self.d_ptr.q_ptr = self

    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)

    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setValue(manager.value(property))
        editor.valueChangedSignal.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
