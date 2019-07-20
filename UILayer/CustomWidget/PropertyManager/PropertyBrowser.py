# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 23:56
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : PropertyBrowser.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor
from lib.QtProperty.qttreepropertybrowser import QtTreePropertyBrowser
from lib.QtProperty.qtpropertymanager import QtStringPropertyManager, QtGroupPropertyManager, \
    QtBoolPropertyManager, QtDatePropertyManager, QtProperty
from lib.QtProperty.qteditorfactory import QtEnumEditorFactory, QtEnumPropertyManager, \
    QList, QtLineEditFactory, QtCheckBoxFactory
from PyQt5.QtWidgets import QDockWidget

from UILayer.CustomWidget.PropertyManager.CustomColorEditorFactory import CustomColorEditorFactory
from UILayer.CustomWidget.PropertyManager.CustomPropertyManager import CustomColorPropertyManager


class MarkItemBrowser(QtTreePropertyBrowser):
    my_list = ['耕地', '园地', '林地', '草地', '居民点及工矿', '交通用地', '水域及水利设施用地', '未利用地', '其他土地']
    my_list_0 = ['水田', '水浇地', '旱地']
    my_list_1 = ['果园', '茶园', '其他园地']
    my_list_2 = ['林地', '灌木林地', '疏林地', '幼林地', '其他林地']
    my_list_3 = ['高覆盖草地', '中高覆盖草地', '中覆盖草地', '中低覆盖草地', '低覆盖草地']
    my_list_4 = ['城镇居民点', '农村居民点', '独立工矿用地', '商服及公共用地', '特殊用地']
    my_list_5 = []
    my_list_6 = []
    my_list_7 = []
    my_list_8 = ['盐碱地', '沙地', '沼泽地', '裸岩', '裸土']
    my_list_0_0 = []
    my_list_0_1 = []
    my_list_0_2 = ['梯坪地', '坡耕地']
    my_list_1_0 = []
    my_list_1_1 = []
    my_list_1_2 = []
    my_list_2_0 = []
    my_list_2_1 = []
    my_list_2_2 = []
    my_list_2_3 = []
    my_list_2_4 = []
    my_list_3_0 = []
    my_list_3_1 = []
    my_list_3_2 = []
    my_list_3_3 = []
    my_list_3_4 = []
    my_list_4_0 = []
    my_list_4_1 = []
    my_list_4_2 = []
    my_list_4_3 = []
    my_list_4_4 = []
    my_list_8_0 = []
    my_list_8_1 = []
    my_list_8_2 = []
    my_list_8_3 = []
    my_list_8_4 = []
    remarks_3_0 = '覆盖度大于75%'
    remarks_3_1 = '覆盖度60%～75%'
    remarks_3_2 = '覆盖度45%～60%'
    remarks_3_3 = '覆盖度30%～45%'
    remarks_3_4 = '覆盖度小于30%'
    remarks_7 = '荒地'
    operate = ['无', '添加人员']
    my_list_list = (my_list_0, my_list_1, my_list_2, my_list_3, my_list_4, my_list_5, my_list_6, my_list_7, my_list_8)
    color_qss = QColor()
    color_dictionary = {my_list_0[0]:QColor.fromHsv(0, 255, 255),
                        my_list_0[1]:QColor.fromHsv(12, 255, 255),
                        my_list_0_2[0]:QColor.fromHsv(24, 255, 255),
                        my_list_0_2[1]: QColor.fromHsv(36, 255, 255),
                        my_list_1[0]:QColor.fromHsv(48, 255, 255),
                        my_list_1[1]:QColor.fromHsv(60, 255, 255),
                        my_list_1[2]:QColor.fromHsv(72, 255, 255),
                        my_list_2[0]:QColor.fromHsv(84, 255, 255),
                        my_list_2[1]:QColor.fromHsv(96, 255, 255),
                        my_list_2[2]:QColor.fromHsv(108, 255, 255),
                        my_list_2[3]:QColor.fromHsv(120, 255, 255),
                        my_list_2[4]:QColor.fromHsv(132, 255, 255),
                        my_list_3[0]:QColor.fromHsv(144, 255, 255),
                        my_list_3[1]:QColor.fromHsv(156, 255, 255),
                        my_list_3[2]:QColor.fromHsv(168, 255, 255),
                        my_list_3[3]:QColor.fromHsv(180, 255, 255),
                        my_list_3[4]:QColor.fromHsv(192, 255, 255),
                        my_list_4[0]:QColor.fromHsv(204, 255, 255),
                        my_list_4[1]:QColor.fromHsv(216, 255, 255),
                        my_list_4[2]:QColor.fromHsv(228, 255, 255),
                        my_list_4[3]:QColor.fromHsv(240, 255, 255),
                        my_list_4[4]:QColor.fromHsv(252, 255, 255),
                        my_list[5]:QColor.fromHsv(264, 255, 255),
                        my_list[6]:QColor.fromHsv(276, 255, 255),
                        my_list[7]:QColor.fromHsv(288, 255, 255),
                        my_list_8[0]:QColor.fromHsv(300, 255, 255),
                        my_list_8[1]:QColor.fromHsv(312, 255, 255),
                        my_list_8[2]:QColor.fromHsv(324, 255, 255),
                        my_list_8[3]:QColor.fromHsv(336, 255, 255),
                        my_list_8[4]:QColor.fromHsv(348, 255, 255)}

    def __init__(self, mark_item, parent=None):
        QtTreePropertyBrowser.__init__(self, parent)

        self.__mark_item = mark_item

        self.mark_name_manager = QtStringPropertyManager(self)
        self.project_name = self.mark_name_manager.addProperty('项目名称')

        self.person_name_group_manager = QtGroupPropertyManager(self)
        self.person_name_group = self.person_name_group_manager.addProperty('项目标注人')
        self.person_name_manager = QtStringPropertyManager(self)
        self.person_name_add_manager = QtEnumPropertyManager(self)
        self.person_name_add = self.person_name_add_manager.addProperty('操作')

        self.date_manager = QtDatePropertyManager(self)
        self.my_date = self.date_manager.addProperty('标注时间')

        self.enum_manager = QtEnumPropertyManager(self)
        self.type = self.enum_manager.addProperty('地物类型')

        self.enum_manager1 = QtEnumPropertyManager(self)
        self.type_1 = self.enum_manager1.addProperty('一级类名称')

        self.enum_manager2 = QtEnumPropertyManager(self)
        self.type_2 = self.enum_manager2.addProperty('二级类名称')

        self.enum_manager3 = QtEnumPropertyManager(self)
        self.type_3 = self.enum_manager3.addProperty('三级类名称')
        self.enum_manager3.valueChangedSignal.connect(self.mark_type_changed)

        self.manager = QtStringPropertyManager(self)
        self.marks_widget = self.manager.addProperty('备注')

        self.color_test_manager = CustomColorPropertyManager(self)
        self.color_test = self.color_test_manager.addProperty('标注颜色')

        self.visibility_manager = QtBoolPropertyManager(self)
        self.visibility = self.visibility_manager.addProperty('可见性')
        self.visibility_manager.valueChangedSignal.connect(self.visible_changed)

        self.lockablility_manager = QtBoolPropertyManager(self)
        self.lockablility = self.lockablility_manager.addProperty('锁定')
        self.lockablility_manager.valueChangedSignal.connect(self.locked_changed)

        self.fill_manager = QtBoolPropertyManager(self)
        self.fill = self.fill_manager.addProperty('填充')
        self.fill_manager.valueChangedSignal.connect(self.fill_changed)
        self.fill_manager.setValue(self.fill, self.__mark_item.fill)

        self.__create_project_name(self.__mark_item.item_name)
        self.__create_person_name(self.__mark_item.get_person_names())
        # self.__create_date(self.__mark_item.date)
        self.__create_type(self.__mark_item.mark_type)
        self.__create_visibility(self.__mark_item.visible)
        self.__create_lockability(self.__mark_item.locked)
        self.__create_property_browser(self)

    def qss_setting(self, Qcolor:QColor):
        color_rgb = Qcolor.getRgb()
        color_r = color_rgb[0]
        color_g = color_rgb[1]
        color_b = color_rgb[2]
        string = 'QComboBox{color:rgb('+str(color_r) + ',' + str(color_g) + ',' + str(color_b) + ');}'
        print(string)
        self.setStyleSheet(string)

    # def color_changed(self, item, color: QColor):
    #     self.__mark_item.color = self.color_qss

    def __create_project_name(self, data_project_name):
        self.mark_name_manager.setValue(self.project_name, data_project_name)
        self.mark_name_manager.editor_finished_signal.connect(self.mark_item_name_changed)
        self.__mark_item.mark_item_name_changed.connect(
            lambda _, new_name: self.mark_name_manager.setValue(self.project_name, new_name)
        )

    def __create_person_name(self, data_person_name):
        for i in data_person_name:
            self.person_name = self.person_name_manager.addProperty('标注人员')
            self.person_name_manager.setValue(self.person_name, i)
            self.person_name_group.addSubProperty(self.person_name)

        operate = QList(self.operate)
        self.person_name_add_manager.setEnumNames(self.person_name_add, operate)
        self.person_name_add_manager.setValue(self.person_name_add, 0)

        self.person_name_add_manager.valueChangedSignal.connect(self.__function_person_name_add)

        self.person_name_group.addSubProperty(self.person_name_add)
        self.person_name_manager.editor_finished_signal.connect(self.__person_name_changed)

    def __create_date(self, data_date):
        self.date_manager.setValue(self.my_date, data_date)

    def __create_type(self, data_type):
        types = QList(self.my_list)
        self.enum_manager.setEnumNames(self.type, types)
        self.enum_manager.setValue(self.type, data_type[0])
        self.enum_manager.valueChangedSignal.connect(self.__enum_changed)

        types_1 = QList(self.my_list)
        self.enum_manager1.setEnumNames(self.type_1, types_1)
        self.enum_manager1.setValue(self.type_1, data_type[0])
        self.type.addSubProperty(self.type_1)
        self.enum_manager1.valueChangedSignal.connect(self.__enum_changed)

        types_2 = QList(self.my_list_0)
        self.enum_manager2.setEnumNames(self.type_2, types_2)
        self.enum_manager2.setValue(self.type_2, data_type[1])
        self.type.addSubProperty(self.type_2)
        self.enum_manager2.valueChangedSignal.connect(self.__enum_changed_2)

        types_3 = QList(self.my_list_1_0)
        self.enum_manager3.setEnumNames(self.type_3, types_3)
        self.enum_manager3.setValue(self.type_3, data_type[2])
        self.type.addSubProperty(self.type_3)
        self.enum_manager3.valueChangedSignal.connect(self.__enum_changed_3)

        if len(data_type) > 3:
            self.manager.setValue(self.marks_widget, data_type[3])
            self.type.addSubProperty(self.marks_widget)

        self.color_test_manager.setValue(self.color_test, self.__mark_item.color)
        self.type.addSubProperty(self.color_test)

    def __create_visibility(self, visibility):
        self.visibility_manager.setValue(self.visibility, visibility)

    def __create_lockability(self, lockability):
        self.lockablility_manager.setValue(self.lockablility, lockability)

    def __create_property_browser(self, browser: QtTreePropertyBrowser):
        enum_fictory = QtEnumEditorFactory()
        string_fictory = QtLineEditFactory()
        bool_fictory = QtCheckBoxFactory()
        color_test_fictory = CustomColorEditorFactory()

        browser.setFactoryForManager(self.mark_name_manager, string_fictory)
        browser.setFactoryForManager(self.person_name_manager, string_fictory)
        browser.setFactoryForManager(self.person_name_add_manager, enum_fictory)
        browser.setFactoryForManager(self.enum_manager, enum_fictory)
        browser.setFactoryForManager(self.enum_manager1, enum_fictory)
        browser.setFactoryForManager(self.enum_manager2, enum_fictory)
        browser.setFactoryForManager(self.enum_manager3, enum_fictory)
        browser.setFactoryForManager(self.color_test_manager, color_test_fictory)
        browser.setFactoryForManager(self.visibility_manager, bool_fictory)
        browser.setFactoryForManager(self.lockablility_manager, bool_fictory)
        browser.setFactoryForManager(self.fill_manager, bool_fictory)

        browser.addProperty(self.project_name)
        browser.addProperty(self.person_name_group)
        browser.addProperty(self.my_date)
        browser.addProperty(self.type)
        browser.addProperty(self.visibility)
        browser.addProperty(self.lockablility)
        browser.addProperty(self.fill)

    def mark_item_name_changed(self, _property, value):
        self.__mark_item.item_name = value

    def __enum_changed(self, item, value):
        if item == self.type:
            self.enum_manager1.setValue(self.type_1, value)
        else:
            self.enum_manager.setValue(self.type, value)

        if value == 0:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_0))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList(self.my_list_0_0))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, '')
        elif value == 1:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_1))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList(self.my_list_1_0))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, '')
        elif value == 2:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_2))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList(self.my_list_2_0))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, '')
        elif value == 3:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_3))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList(self.my_list_3_0))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, self.remarks_3_0)
        elif value == 4:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_4))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList(self.my_list_4_0))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, '')
        elif value == 5:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_5))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList([]))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, '')
            self.color_qss = self.color_dictionary[self.my_list[5]]
            self.color_test_manager.setValue(self.color_test, self.color_qss)
        elif value == 6:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_6))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList([]))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, '')
            self.color_qss = self.color_dictionary[self.my_list[6]]
            self.color_test_manager.setValue(self.color_test, self.color_qss)
        elif value == 7:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_7))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList([]))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, self.remarks_7)
            self.color_qss = self.color_dictionary[self.my_list[7]]
            self.color_test_manager.setValue(self.color_test, self.color_qss)
        elif value == 8:
            self.enum_manager2.setEnumNames(self.type_2, QList(self.my_list_8))
            self.enum_manager2.setValue(self.type_2, 0)
            self.enum_manager3.setEnumNames(self.type_3, QList(self.my_list_8_0))
            self.enum_manager3.setValue(self.type_3, 0)
            self.manager.setObjectName('')
            self.manager.setValue(self.marks_widget, '')

        self.mark_type_changed()

    def __enum_changed_2(self, item, value):
        now = self.enum_manager1.value(self.type_1)
        print(now)
        print(value)
        if now == 0:
            if value == 0:
                self.enum_manager3.setEnumNames(self.type_3, QList([]))
                self.enum_manager3.setValue(self.type_3, 0)
                self.color_qss = self.color_dictionary[self.my_list_0[0]]
                self.color_test_manager.setValue(self.color_test, self.color_qss)
            elif value == 1:
                self.enum_manager3.setEnumNames(self.type_3, QList([]))
                self.enum_manager3.setValue(self.type_3, 0)
                self.color_qss = self.color_dictionary[self.my_list_0[1]]
                self.color_test_manager.setValue(self.color_test, self.color_qss)
            elif value == 2:
                self.enum_manager3.setEnumNames(self.type_3, QList(self.my_list_0_2))
                self.enum_manager3.setValue(self.type_3, 0)
        elif now == 3:
            if value == 0:
                self.manager.setValue(self.marks_widget, self.remarks_3_0)
                self.color_qss = self.color_dictionary[self.my_list_3[0]]
                self.color_test_manager.setValue(self.color_test, self.color_qss)
            elif value == 1:
                self.manager.setValue(self.marks_widget, self.remarks_3_1)
                self.color_qss = self.color_dictionary[self.my_list_3[1]]
                self.color_test_manager.setValue(self.color_test, self.color_qss)
            elif value == 2:
                self.manager.setValue(self.marks_widget, self.remarks_3_2)
                self.color_qss = self.color_dictionary[self.my_list_3[2]]
                self.color_test_manager.setValue(self.color_test, self.color_qss)
            elif value == 3:
                self.manager.setValue(self.marks_widget, self.remarks_3_3)
                self.color_qss = self.color_dictionary[self.my_list_3[3]]
                self.color_test_manager.setValue(self.color_test, self.color_qss)
            elif value == 4:
                self.manager.setValue(self.marks_widget, self.remarks_3_4)
                self.color_qss = self.color_dictionary[self.my_list_3[4]]
                self.color_test_manager.setValue(self.color_test, self.color_qss)
        elif now ==5 or now == 6 or now == 7:
            pass
        else:
            self.enum_manager3.setEnumNames(self.type_3, QList([]))
            self.enum_manager3.setValue(self.type_3, 0)
            linshi = self.my_list_list[now]
            self.color_qss = self.color_dictionary[linshi[value]]
            self.color_test_manager.setValue(self.color_test, self.color_qss)

        self.mark_type_changed()

    def __enum_changed_3(self, item, value):
        type1 = self.enum_manager1.value(self.type_1)
        type2 = self.enum_manager2.value(self.type_2)
        self.color_qss = self.color_dictionary[self.my_list_0_2[value]]
        self.color_test_manager.setValue(self.color_test, self.color_qss)
        self.mark_type_changed()

    def visible_changed(self, item, value):
        self.__mark_item.visible = value

    def locked_changed(self, item, value):
        self.__mark_item.locked = value

    def fill_changed(self, item, value):
        self.__mark_item.fill = value

    def mark_type_changed(self):

        make_type = [self.enum_manager.value(self.type), self.enum_manager2.value(self.type_2),
                     self.enum_manager3.value(self.type_3), self.manager.value(self.marks_widget)]
        self.__mark_item.set_mark_type(tuple(make_type))
        self.__mark_item.color = self.color_qss

    def __person_name_changed(self, item: QtProperty, value):

        if item.hasValue() and len(value) > 0:
            return
        else:
            self.person_name_group.removeSubProperty(item)

    def __function_person_name_add(self, item, value):
        if value == 1:
            self.person_name_group.removeSubProperty(self.person_name_add)

            self.person_name = self.person_name_manager.addProperty('标注人员')
            self.person_name_manager.setObjectName('')
            self.person_name_manager.setValue(self.person_name, '')
            self.person_name_group.addSubProperty(self.person_name)

            self.person_name_add_manager.setValue(self.person_name_add, 0)
            self.person_name_group.addSubProperty(self.person_name_add)

    @property
    def item_name(self):
        project_name = self.mark_name_manager.value(self.project_name)
        return project_name

    @property
    def person_names(self):
        person_name_group = self.person_name_group.subProperties()
        person_name = []
        for i in person_name_group:
            person_name.append(self.person_name_manager.value(i))
        return person_name

    @property
    def date(self):
        date = QDate.currentDate()
        return date

    @property
    def item_color(self):
        color = self.color_manager.value(self.color)
        return color

    @property
    def mark_type(self):
        type = []
        type_1 = self.enum_manager1.value(self.type_1)
        type.append(type_1)
        type_2 = self.enum_manager2.value(self.type_2)
        type.append(type_2)
        type_3 = self.enum_manager3.value(self.type_3)
        type.append(type_3)
        remarks = self.manager.value(self.marks_widget)
        type.append(remarks)
        return type

    @property
    def visible(self):
        return self.visibility

    @property
    def locked(self):
        return self.lockablility

    def list_detection_1(self, now):
        string = 'self.my_list_'+str(now)
        return string

    def list_detection_2(self, now, value):
        string = 'self.my_list_'+str(now)+'_'+str(value)
        return string


class ProjectBrowser(QtTreePropertyBrowser):
    operate = ['无', '添加人员']

    def __init__(self, project):
        QtTreePropertyBrowser.__init__(self, parent=None)

        self.__project = project

        self.project_name_manager = QtStringPropertyManager(self)
        self.project_name = self.project_name_manager.addProperty('项目名称')
        self.project_name_manager.editor_finished_signal.connect(self.project_name_chnanged)

        self.person_names_manager = QtGroupPropertyManager(self)
        self.person_name_group = self.person_names_manager.addProperty('参与人员')
        self.person_name_manager = QtStringPropertyManager(self)
        self.person_name = self.person_name_manager.addProperty('姓名')
        self.person_name_add_manager = QtEnumPropertyManager(self)
        self.person_name_add = self.person_name_add_manager.addProperty('操作')

        # self.area_manager = QtStringPropertyManager(self)
        # self.my_area = self.area_manager.addProperty('区域')

        self.visibility_manager = QtBoolPropertyManager(self)
        self.visibility = self.visibility_manager.addProperty('可见性')

        self.lockablility_manager = QtBoolPropertyManager(self)
        self.lockablility = self.lockablility_manager.addProperty('锁定')

        self.__create_project_name(self.__project.project_name)
        self.__create_person_name(self.__project.persons)
        # self.__create_area(self.__project.area)
        self.__create_visibility(self.__project.visible)
        self.__create_lockability(self.__project.locked)
        self.__create_blowser(self)

    def project_name_chnanged(self, item, value):
        self.__project.project_name = value

    def __create_project_name(self, project_name):
        self.project_name_manager.setValue(self.project_name, project_name)
        # self.project_name_manager.editor_finished_signal.connect()

    def __create_person_name(self, person_name):
        for i in person_name:
            self.person_name = self.person_name_manager.addProperty('姓名')
            self.person_name_manager.setValue(self.person_name, i)
            self.person_name_group.addSubProperty(self.person_name)

        operate = QList(self.operate)
        self.person_name_add_manager.setEnumNames(self.person_name_add, operate)
        self.person_name_add_manager.setValue(self.person_name_add, 0)
        self.person_name_add_manager.valueChangedSignal.connect(self.__function_person_name_add)
        self.person_name_group.addSubProperty(self.person_name_add)

        self.person_name_manager.valueChangedSignal.connect(self.__person_name_changed)

    def __create_area(self, area):
        self.area_manager.setValue(self.my_area, area)

    def __create_visibility(self, visibility):
        self.visibility_manager.setValue(self.visibility, visibility)

    def __create_lockability(self, lockability):
        self.lockablility_manager.setValue(self.lockablility, lockability)

    def __create_blowser(self, browser: QtTreePropertyBrowser):
        string_fictory = QtLineEditFactory()
        enum_fictory = QtEnumEditorFactory()
        bool_fictory = QtCheckBoxFactory()

        browser.setFactoryForManager(self.project_name_manager, string_fictory)
        browser.setFactoryForManager(self.person_name_manager, string_fictory)
        browser.setFactoryForManager(self.person_name_add_manager, enum_fictory)
        # browser.setFactoryForManager(self.area_manager, string_fictory)
        browser.setFactoryForManager(self.visibility_manager, bool_fictory)
        browser.setFactoryForManager(self.lockablility_manager, bool_fictory)

        browser.addProperty(self.project_name)
        browser.addProperty(self.person_name_group)
        # browser.addProperty(self.my_area)
        browser.addProperty(self.visibility)
        browser.addProperty(self.lockablility)

    def __person_name_changed(self, item, value):
        if item.hasValue() and len(value) > 0:
            return
        else:
            self.person_name_group.removeSubProperty(item)

    def __function_person_name_add(self, item, value):
        if value == 1:
            self.person_name_group.removeSubProperty(self.person_name_add)

            self.person_name = self.person_name_manager.addProperty('标注人员')
            self.person_name_manager.setObjectName('')
            self.person_name_manager.setValue(self.person_name, '')
            self.person_name_group.addSubProperty(self.person_name)

            self.person_name_add_manager.setValue(self.person_name_add, 0)
            self.person_name_group.addSubProperty(self.person_name_add)

    @property
    def item_name(self):
        return self.__i

    @property
    def person_names(self):
        person_names = self.person_name_group.subProperties()
        person_name = []
        for i in person_names:
            person_name.append(self.person_name_manager.value(i))
        return person_name

    @property
    def area(self):
        return self.area

    @property
    def visible(self):
        return self.visibility

    @property
    def locked(self):
        return self.lockablility


class PropertyBrowser(QDockWidget):
    def __init__(self, parent=None, browser: QtTreePropertyBrowser = None):
        QDockWidget.__init__(self, parent=parent)
        parent.addDockWidget(Qt.RightDockWidgetArea, self)
        self.setWindowTitle("属性")
        self.setWidget(browser)
        browser.show()
