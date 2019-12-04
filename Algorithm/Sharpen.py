# -*- encoding: utf-8 -*-
# @File    : Sharpen.py
# @Time    : 2019/12/3 20:25
# @Author  : 一叶星羽
# @Email   : h0670131005@gmail.com
# @Software: PyCharm


import numpy as np
from scipy import interpolate
from CommonHelpers.Utils import path_to_list, list_to_path


def curve_sharpening(points, kind="linear"):
    x, y = [], []
    for ln in points:
        x.append(ln[0])
        y.append(ln[1])
    x = np.array(x)
    y = np.array(y)

    x_new = np.linspace(x.max(), x.min(), 200)
    func = interpolate.interp1d(x, y, kind=kind)
    y_new = func(x_new)
    new_points = [(x1, y1) for x1 in x_new for y1 in y_new]
    return new_points


def curve_sharpen_path(path, kind):
    print("element: ", path.elementCount())
    points = path_to_list(path)
    print(len(points))
    print(points)
    result = curve_sharpening(points, kind)
    print("------------------------- 锐化结束 ----------------------")
    return list_to_path(result)


if __name__ == '__main__':
    curve_sharpening([(1, 2), (2, 3), (3, 5)])
