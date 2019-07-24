# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 16:00
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Id.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm


class Id:
    """这个类还要改善"""

    def __init__(self, name: str):
        self._id = id(name)
        self._name = name

    @property
    def id(self):
        return self._id

    def name(self) -> str:
        return self._name

    def to_string(self) -> str:
        return "ID: " + str(self._id) + " " + self._name

    def __str__(self):
        return self.to_string()

    def __eq__(self, other):
        return self._id == other.id

    def __ne__(self, other):
        return self._id != other.id

    def __hash__(self):
        return self._id


if __name__ == '__main__':
    from IOFormat.MarkFile import ProjectFormat
    reader_format = ProjectFormat()

    project = reader_format.read_project("D:/海秀镇轮廓标注.mfb")

    mark_items = project.get_mark_items()

    id1 = Id(mark_items[0].item_name)
    id2 = Id(mark_items[1].item_name)
    id3 = Id(mark_items[2].item_name)
    id4 = Id(mark_items[3].item_name)

    print(id1, mark_items[0].item_name)
    print(id2, mark_items[1].item_name)
    print(id3, mark_items[2].item_name)
    print(id4, mark_items[3].item_name)
