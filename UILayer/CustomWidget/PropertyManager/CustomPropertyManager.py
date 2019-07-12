# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 23:53
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : CustomPropertyManager.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

from lib.QtProperty.qtpropertymanager import *


class MyColorPropertyManagerPrivate:
    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()


class CustomColorPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QColor)

    def __init__(self, parent=None):
        super(CustomColorPropertyManager, self).__init__(parent)

        self.d_ptr = MyColorPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    def __del__(self):
        self.clear()
        del self.d_ptr

    def value(self, property):
        return self.d_ptr.m_values.get(property, QColor())

    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        return ''

    def valueIcon(self, property):
        if not property in self.d_ptr.m_values.keys():
            return QIcon()
        return QtPropertyBrowserUtils.brushValueIcon(QBrush(self.d_ptr.m_values[property]))

    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        if (self.d_ptr.m_values[property] == val):
            return

        self.d_ptr.m_values[property] = val

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, val)

    def initializeProperty(self, property):
        val = QColor()
        self.d_ptr.m_values[property] = val

    def uninitializeProperty(self, property):

        # self.d_ptr.m_propertyToA.remove(property)
        self.d_ptr.m_values.remove(property)
