import struct
from enum import IntEnum


class GadgetDockWidgetState(IntEnum):

    NONE_TOOL = 0
    RECTANGLE_SELECT_TOOL = 1
    ELLIPSE_SELECT_TOOL = 2
    ZOOM_TOOL = 3
    GRIP_TONGS_TOOL = 4
    ROTATE_ZOOM = 5
    MOVE_TOOL = 6


class ToolbarState(IntEnum):

    NONE_SELECTED = 0
    NEW_SELECTION = 1
    ADD_TO_SELECTION = 2
    SUB_FROM_SELECTION = 3
    AND_WITH_SELECTION = 4
    CLICK_ZOOM_IN = 5
    CLICK_ZOOM_OUT = 6


class OptionTool(IntEnum):
    """一些用于辅助标注的工具的标识参数"""
    NONE_RES = -1
    MOVE_TOOL = 1
    QUICK_SELECT_TOOL = 2
    RECT_QUICK_SELECT_TOOL = 3
    ELLIPSE_QUICK_SELECT_TOOL = 4
    GRIP_TOOL = 5
    GRIP_TONGS = 6
    GRIP_ROTATE = 7
    ZOOM_TOOL = 8


def counter(start_at=0):
    count_num = start_at
    while True:
        val = (yield count_num)
        if val is not None:
            count_num = val
        else:
            count_num += 1


PEN_STANDARD_WIDTH = 1.4
