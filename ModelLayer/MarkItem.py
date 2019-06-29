# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 16:06
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MarkItem.py
# @Project : pyqt5_project
# @Software: PyCharm

from ModelLayer.AbstractMarkItem import AbstractMarkItem
from CommonHelper.CommonHelper import counter


class MarkItem(AbstractMarkItem):
    """ 描述 """

    __name_num_count = counter(1)

    def __init__(self, name=None):
        super(MarkItem, self).__init__(name)
        self._mark_item_coor=[]     #标记项坐标信息
        self._mark_people="未填写标记人"
        self._mark_land_type = None     #标记项地物类型
        self._mark_area_name="未填写区域名"     #标记项所代表的实际建筑名
        self._perimeter=-1            #周长
        self._area = -1                 #面积
        self._mark_time = None         #标记时间

        """markers表示多个标记人列表，暂时未用到"""
        self._markers = []
        self._create_mark_item_name()

    def _create_mark_item_name(self):
        if self._name is None:
            num = next(MarkItem.__name_num_count)
            name = "新建标注项" + str(num)
            self.set_name(name)

    def set_item_coor(self, item_coor: list):
        self._mark_item_coor = list(item_coor)   #拷贝形参内容，避免影响实参信息

    def get_item_coor(self):
        return tuple(self._mark_item_coor)

    def set_mark_people(self,people_name:str):
        self._mark_people=people_name

    def get_mark_people(self):
        return self._mark_people

    def set_mark_area_name(self, area_name: str):
        self._mark_area_name = area_name

    def get_mark_area_name(self):
        return self._mark_area_name

    def set_mark_land_type(self, mark_type):
        self._mark_land_type = mark_type

    def get_mark_land_type(self):
        return self._mark_land_type

    def set_girth(self, girth):
        self._girth = girth

    def get_perimeter(self):
        return self._perimeter

    def count_perimeter(self, count_algorithm):
        if callable(count_algorithm):
            self._perimeter = count_algorithm(self._outline_array)

    def set_area(self, area):
        self._area = area

    def get_area(self):
        return self._area

    def count_area(self, count_algorithm):
        if callable(count_algorithm):
            self._area = count_algorithm(self._outline_array)

    def set_mark_time(self, mark_time):
        self._mark_time = mark_time

    def get_mark_time(self):
        return self._mark_time

    """marker表示多个标记人的列表,暂时为填写功能"""
    def add_marker(self, marker):
        self._markers.append(marker)

    def add_markers(self, markers: list):
        self._markers.extend(markers)

    def remove_marker_by_name(self, marker):
        self._markers.remove(marker)

    def remove_marker_by_index(self, index):
        self._markers.pop(index)
    """end-markers"""

    def get_mark_item_data(self):
        """TODO 返回一个JSON数据"""
