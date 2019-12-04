# -*- coding: utf-8 -*-
# @Time    : 2019/7/20 12:58
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Utils.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

import math
import numpy as np
from PyQt5.QtGui import QGuiApplication, QPainterPath
from PyQt5.QtCore import QPoint

scale = 1.0
default_dpi_scale = 1.0
def_dpi_scale = lambda: QGuiApplication.primaryScreen().logicalDotsPerInchX() / 96.0 \
    if QGuiApplication.primaryScreen() else 1.0


def get_default_dpi_scale():
    global default_dpi_scale
    default_dpi_scale = def_dpi_scale()
    return default_dpi_scale


def dpi_scaled_from_float(value: float):
    global scale
    scale = get_default_dpi_scale()
    return scale * value


origin = QPoint(0, 0)
refvec = QPoint(0, 1)


def compare(point1: QPoint, point2: QPoint):
    d1 = math.atan2(point1.y() - 2, point1.x() - 2)
    d2 = math.atan2(point2.y() - 2, point2.x() - 2)
    return d1 < d2


def clockwiseangle_and_distance(point):
    return (math.atan2(point.y(), point.x()) * 360 / 2 / np.pi + 360) % 360
    # # Vector between point and the origin: v = p - o
    # vector = QPoint(point.x()-origin.x(), point.y()-origin.y())
    # # Length of vector: ||v||
    # lenvector = math.hypot(vector.x(), vector.y())
    # # If length is zero there is no angle
    # if lenvector == 0:
    #     return -math.pi, 0
    # # Normalize vector: v/||v||
    # normalized = QPoint(vector.x()/lenvector, vector.y()/lenvector)
    # dotprod  = normalized.x()*refvec.x() + normalized.y()*refvec.y()     # x1*x2 + y1*y2
    # diffprod = refvec.y()*normalized.x() - refvec.x()*normalized.y()     # x1*y2 - y1*x2
    # angle = math.atan2(diffprod, dotprod)
    # # Negative angles represent counter-clockwise angles so we need to subtract them
    # # from 2*pi (360 degrees)
    # if angle < 0:
    #     return 2*math.pi+angle, lenvector
    # # I return first the angle because that's the primary sorting criterium
    # # but if two vectors have the same angle then the shorter distance should come first.
    # return angle, lenvector




# 获取基准点的下标,基准点是p[k]
def get_leftbottompoint(p):
    k = 0
    for i in range(1, len(p)):
        if p[i][1] < p[k][1] or (p[i][1] == p[k][1] and p[i][0] < p[k][0]):
            k = i
    return k


# 叉乘计算方法
def multiply(p1, p2, p0):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


# 获取极角，通过求反正切得出，考虑pi/2的情况
def get_arc(p1, p0):
    # 兼容sort_points_tan的考虑
    if (p1[0] - p0[0]) == 0:
        if (p1[1] - p0[1]) == 0:
            return -1
        else:
            return math.pi / 2
    tan = float((p1[1] - p0[1])) / float((p1[0] - p0[0]))
    arc = math.atan(tan)
    if arc >= 0:
        return arc
    else:
        return math.pi + arc


# 对极角进行排序,排序结果list不包含基准点
def sort_points_tan(p, pk):
    p2 = []
    for i in range(0, len(p)):
        p2.append({"index": i, "arc": get_arc(p[i], pk)})
    # print('排序前:',p2)
    p2.sort(key=lambda k: (k.get('arc')))
    # print('排序后:',p2)
    p_out = []
    for i in range(0, len(p2)):
        p_out.append(p[p2[i]["index"]])
    return p_out


def convex_hull(p):
    if len(p) <= 3:
        return p
    p = points_to_list(p)
    p = list(set(p))
    # print('全部点:',p)
    k = get_leftbottompoint(p)
    pk = p[k]
    p.remove(p[k])
    # print('排序前去除基准点的所有点:',p,'基准点:',pk)

    p_sort = sort_points_tan(p, pk)  # 按与基准点连线和x轴正向的夹角排序后的点坐标
    # print('其余点与基准点夹角排序:',p_sort)
    p_result = [pk, p_sort[0]]

    for i in range(1, len(p_sort)):
        #####################################
        # 叉乘为正,向前递归删点;叉乘为负,序列追加新点
        while multiply(p_result[-2], p_sort[i], p_result[-1]) > 0:
            p_result.pop()
        p_result.append(p_sort[i])
    p_result = list_to_point(p_result)
    return p_result  # 测试


def points_to_list(points):
    result = []
    for point in points:
        result.append((point.x(), point.y()))
    return result


def list_to_point(points):
    result = []
    for point in points:
        result.append(QPoint(int(point[0]), int(point[1])))
    return result


def list_to_path(points):
    result = QPainterPath()
    result.moveTo(QPoint(int(points[0][0]), int(points[0][1])))
    for point in points[1:]:
        result.lineTo(QPoint(int(point[0]), int(point[1])))
    result.closeSubpath()
    return result


def path_to_list(path: QPainterPath):
    result = []
    # path_len = int(path.length())

    for i in range(path.elementCount()):
        element = path.elementAt(i)
        result.append((element.x, element.y))
        # point = path.pointAtPercent(path.percentAtLength(i))
        # result.append([point.x(), point.y()])

    return result


def sorted_points(points: list) -> list:
    return sorted(points, key=lambda point: (math.atan2(point.y(), point.x()) * 360 / 2 / np.pi + 360) % 360)


if __name__ == '__main__':
    test_data = [(220, -100), (0, 0), (-40, -170), (240, 50), (-160, 150), (-210, -150)]
    print(test_data)

    result1 = convex_hull(test_data)
    print(result1)
