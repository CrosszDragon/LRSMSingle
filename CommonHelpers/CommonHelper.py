from PyQt5.QtWidgets import QAction, QAbstractButton, QMenu
from PyQt5.QtGui import QTransform, QIcon, QImage
from PyQt5 import QtGui
import numpy as np


def add_menu(text, target, object_name=None, tip=None, slot=None, signal=None) -> QMenu:
    new_menu = target.addMenu(text)
    if object_name:
        new_menu.setObjectName(object_name)
    if tip:
        new_menu.setToolTip(tip)
    if slot and signal:
        if signal == "aboutToShow":
            # 这里还要判断 slot是否可调用
            new_menu.aboutToShow.connect(slot)
    return new_menu


def add_actions(target, actions):
    for action in actions:
        if action:
            target.addAction(action)
        else:
            target.addSeparator()


def create_action(parent=None, text="", shortcut=None, slot=None, tip=None,
                  icon=None, checkable=False, signal="triggered", image=None):
    new_action = QAction(text, parent)
    if icon:
        new_action.setIcon(QIcon(icon))
    if shortcut:
        new_action.setShortcut(shortcut)
    if tip:
        new_action.setToolTip(tip)
        new_action.setStatusTip(tip)
    if slot and callable(slot):
        if signal == "triggered":
            new_action.triggered.connect(slot)
        elif signal == "toggled":
            new_action.toggled.connect(slot)
    if checkable:
        new_action.setCheckable(True)
    if image:
        new_action.setIcon(QIcon(image))
    return new_action


def set_widgets(target, widgets):
    for widget in widgets:
        target.setWidget(widget)


def join_group(target, actions):
    for index, action in enumerate(actions):
        if action and isinstance(action, QAction):
            target.addAction(action)
        elif action and isinstance(action, QAbstractButton):
            target.addButton(action, index)


def print_transform(text: str, transform:QTransform = QTransform()):
    print(text)
    print(transform.m11(), " ", end="")
    print(transform.m12(), " ", end="")
    print(transform.m13(), " ", end="")
    print(" ")
    print(transform.m21(), " ", end="")
    print(transform.m22(), " ", end="")
    print(transform.m23(), " ", end="")
    print(" ")
    print(transform.m31(), " ", end="")
    print(transform.m32(), " ", end="")
    print(transform.m33(), " ", end="")
    print(" ")


def remove_object_by_objects(src_list, objects):
    if isinstance(src_list, list):
        for obj in objects:
            if obj in src_list:
                src_list.remove(obj)
    return src_list


def remove_object_by_indexes(src_list, indexes):
    if isinstance(src_list, list):
        if isinstance(indexes, list):
            indexes = reversed(sorted(indexes))
            for index in indexes:
                if 0 <= index < len(src_list):
                    src_list.pop(index)
        elif isinstance(indexes, int):
            if 0 <= indexes < len(src_list):
                src_list.pop(indexes)
    return src_list


def counter(start_at=1):
    count_num = start_at
    while True:
        val = (yield count_num)
        if val is not None:
            count_num = val
        else:
            count_num += 1


def adjust_pen_width(standard_width, scale):
    return standard_width / scale


def qimage2numpy(qimage: QImage):
    """Convert QImage to numpy.ndarray.  The dtype defaults to uint8
    for QImage.Format_Indexed8 or `bgra_dtype` (i.e. a record array)
    for 32bit color images.  You can pass a different dtype to use, or
    'array' to get a 3D uint8 array for color images."""
    result_shape = (qimage.height(), qimage.width())
    temp_shape = (qimage.height(), int(qimage.bytesPerLine() * 8 / qimage.depth()))
    if qimage.format() in (QImage.Format_ARGB32_Premultiplied,
                           QImage.Format_ARGB32,
                           QImage.Format_RGB32):
        dtype = np.uint8
        result_shape += (4,)
        temp_shape += (4,)
    elif qimage.format() == QtGui.QImage.Format_Indexed8:
        dtype = np.uint8
    else:
        raise ValueError("qimage2numpy only supports 32bit and 8bit images")
        # FIXME: raise error if alignment does not match
    buf = qimage.bits().asstring(qimage.byteCount())
    result = np.frombuffer(buf, dtype).reshape(temp_shape)
    if result_shape != temp_shape:
        result = result[:, :result_shape[1]]
    if qimage.format() == QImage.Format_RGB32 and dtype == np.uint8:
        result = result[..., :3]
    return result


def string_list_to_int(data: str):
    return list(map(int, data[1:-1].split(",")))

# def create_name(num_counter, pre_name)->str:


def bound(min_val, value, max_val):
    """
    如果value >= max_val return mac_val
    如果value <= min_val return min_val
    否则 return value

    :param min_val: 最小值
    :param value: 被测值
    :param max_val: 最大值
    """

    return max(min_val, min(max_val, value))


def gray_from_r_g_b(r, g, b):
    """convert R, G, B to gray 0...255"""
    return (r * 11 + g * 16 + b * 5) / 32


def gray_from_rgb(rgb):
    return gray_from_r_g_b(red_from_rgb(rgb), green_from_rgb(rgb), blue_from_rgb(rgb))


def red_from_rgb(rgb):
    return (rgb >> 16) & 0xff


def green_from_rgb(rgb):
    return (rgb >> 8) & 0xff


def blue_from_rgb(rgb):
    return rgb & 0xff
