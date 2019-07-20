# -*- coding: utf-8 -*-
# @Time    : 2019/7/9 11:26
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : calculation.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

import cv2
import numpy as np
from PyQt5.QtGui import QPainterPath
from Documents.MarkData import Project, MarkItem
from UILayer.CustomWidget.PropertyManager.PropertyBrowser import MarkItemBrowser


def count_area(outline_path: QPainterPath, ratio: int = 1) -> float:
    """
    :param outline_path: 轮廓的像素的矩阵
    :param ratio: 图像的分辨率 以米为单位
    :return: float类型的面积
    """
    fills = outline_path.toFillPolygons()
    j = 0
    counter = []
    for j in range(len(fills)):
        fill = fills[j]
        print(fill)
        i = 0
        counter.append([])
        counter[j] = []
        for i in range(fill.__len__()):
            x = int(fill.value(i).x())
            y = int(fill.value(i).y())
            counter[j].append([x, y])
            i = i + 1
        counter[j] = np.array(counter[j], dtype='int32')
        j = j + 1
    totalarea = 0.0
    i = 0
    for j in counter:
        area = cv2.contourArea(counter[i])
        totalarea = area * ratio + totalarea
        i = i + 1
    return totalarea


def count_perimeter(outline_path: QPainterPath, ratio: int = 1) -> float:
    """
    :param outline_path: 轮廓的像素的矩阵
    :param ratio: 图像的分辨率 以米为单位
    :return: float类型的面积
    """
    percent = QPainterPath.percentAtLength(outline_path, 1000)
    length = 1000 / percent * ratio
    return length


def count_mark_item_area(mark_item: MarkItem):
    area_counted = count_area(mark_item.get_outline())
    type = mark_item.mark_type
    type_list = MarkItemBrowser.my_list
    type_0_2 = MarkItemBrowser.my_list_2
    my_list_list = MarkItemBrowser.my_list_list
    if type[0] == 0 and type[1] == 2:
        type_string = type_0_2[type[2]]
    elif type[0] == 5 or type[0] == 6 or type[0] == 7:
        type_string = type_list[type[0]]
    else:
        type_linshi = my_list_list[type[0]]
        type_string = type_linshi[type[1]]
    return [type_string, area_counted, mark_item.color]


def count_project_data_area(project: Project):
    """"""
    area = []
    for mark_item in project.get_mark_items():

        mark_item_area = count_mark_item_area(mark_item)
        had_type = [_type[0] for _type in area]

        if mark_item_area[0] in had_type:
            index = had_type.index(mark_item_area[0])
            data = area[index][1] + mark_item_area[1]
            area[index][1] = data
        else:
            area.append(mark_item_area)
    return tuple(area)


def count_mark_item_perimeter(mark_item: MarkItem):
    area_counted = count_perimeter(mark_item.get_outline())
    type = mark_item.mark_type
    type_list = MarkItemBrowser.my_list
    type_0_2 = MarkItemBrowser.my_list_2
    my_list_list = MarkItemBrowser.my_list_list
    if type[0] == 0 and type[1] == 2:
        type_string = type_0_2[type[2]]
    elif type[0] == 5 or type[0] == 6 or type[0] == 7:
        type_string = type_list[type[0]]
    else:
        type_linshi = my_list_list[type[0]]
        type_string = type_linshi[type[1]]
    return [type_string, area_counted, mark_item.color]


def count_project_data_perimeter(project: Project):
    """"""
    perimeter = []
    for mark_item in project.get_mark_items():
        mark_item_area = count_mark_item_perimeter(mark_item)
        had_type = [_type[0] for _type in perimeter]

        if mark_item_area[0] in had_type:
            index = had_type.index(mark_item_area[0])
            data = perimeter[index][1] + mark_item_area[1]
            perimeter[index][1] = data
        else:
            perimeter.append(mark_item_area)
    return tuple(perimeter)


def get_projects_area_data(projects: [Project], years: list):
    """"""
    project_data = []
    data_dict = {}
    for project in projects:
        project_data.append(count_project_data_area(project))

    for data in project_data:
        for mark_data in data:
            if mark_data[0] in data_dict:
                data_dict[mark_data[0]][0].append(mark_data[1])
            else:
                data_dict[mark_data[0]] = [[mark_data[1]], years, mark_data[2]]

    result = []
    for key in data_dict.keys():
        if len(data_dict[key][0]) < len(years):
            data_dict[key][0].extend([0] * (len(years) - len(data_dict[key][0])))
        print(key, ":  ", data_dict[key])
        result.append([key, data_dict[key][0], years, data_dict[key][2]])

    return result


