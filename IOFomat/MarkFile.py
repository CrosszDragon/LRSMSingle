# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 21:17
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : MarkFile.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtCore import *
from PyQt5.QtGui import QColor, QPainterPath, QImage, QPainter
from Documents.MarkData import Project, MarkItem
from PIL import Image
from CommonHelpers.CommonHelper import qimage2numpy


class Stream(QDataStream):
    MAGIC_NUMBER = 0x3051E
    FILE_VERSION = 100

    def __init__(self, file: QFile):
        super(QDataStream, self).__init__(file)

    @staticmethod
    def formats():
        return "*.mfb *.mib"

    def __lshift__(self, other):
        if isinstance(other, str):
            self.writeQString(other)
        elif isinstance(other, int):
            self.writeInt(other)
        elif isinstance(other, bool):
            self.writeBool(other)
        elif isinstance(other, float):
            self.writeFloat(other)
        elif isinstance(other, bytes):
            self.writeBytes(other)
        elif isinstance(other, (list, tuple)):
            self.writeQVariantList(other)
        elif isinstance(other, dict):
            self.writeQVariantMap(other)
        else:
            QDataStream.__lshift__(self, other)
        print("load info: ", other)
        return self

    def __rshift__(self, other):
        if isinstance(other, str):
            other = self.readQString()
            print(other)
        elif isinstance(other, int):
            other = self.readInt()
        elif isinstance(other, bool):
            other = self.readBool()
        elif isinstance(other, float):
            other = self.readFloat()
        elif isinstance(other, bytes):
            other = self.readBytes()
        elif isinstance(other, (list, tuple)):
            other = self.readQVariantList()
        elif isinstance(other, dict):
            other = self.readQVariantMap()
        else:
            QDataStream.__rshift__(self, other)

        return other


class ProjectFormat(object):

    def save_project(self, project: Project):
        project_data = project.get_project_data()
        error_message = "保存项目： " + project.project_full_path() + "失败！\n"
        file = None
        try:
            file = QFile(project.project_full_path())
            if not file.open(QIODevice.WriteOnly):
                raise (IOError, str(file.errorString()))

            stream = Stream(file)
            stream.writeInt32(Stream.MAGIC_NUMBER)
            stream.writeInt32(Stream.FILE_VERSION)
            stream.setVersion(QDataStream.Qt_5_1)

            stream << project_data[0]
            stream << project_data[1]
            stream << project_data[2]
            stream << project_data[3]
            for data in project_data[4:]:
                for d in data:
                    stream << d

        except IOError as e:
            print(type(e))
            return False, error_message + str(e)
        except Exception as e:
            print("****************************: ", e)
        finally:
            if file:
                file.close()
            return True, error_message

    def read_project(self, project_path) -> Project:
        file = None
        project = None
        try:
            file = QFile(project_path)

            if not file.open(QIODevice.ReadOnly):
                raise (IOError, str(file.errorString()))

            stream = Stream(file)
            magic = stream.readInt32()
            if magic != Stream.MAGIC_NUMBER:
                raise (IOError, "unrecognized file type")

            version = stream.readInt32()
            if version < Stream.FILE_VERSION:
                raise (IOError, "old and unreadable file format")
            elif version > Stream.FILE_VERSION:
                raise (IOError, "new and unreadable file format")
            stream.setVersion(QDataStream.Qt_5_1)

            project_path = stream >> ""
            project_name = stream >> ""
            project_image = stream >> ""
            project_persons = stream >> []
            project_data = [project_path, project_name, project_image, project_persons]

            while not stream.atEnd():
                item_name = stream >> ""
                persons = stream >> []
                mark_type = stream >> []
                mark_color = stream >> QColor()
                visible = stream >> True
                locked = stream >> False
                fill = stream >> False
                outline_path = stream >> QPainterPath()
                mark_item = [item_name, persons, mark_type, mark_color, visible, locked, fill, outline_path]
                # mark_item = stream >> []
                project_data.append(mark_item)

            file.close()
            return self.get_project_from_project_data(project_data)
        except Exception as e:
            print("打开项目：", project_path, " 失败！：", e)
        finally:
            if file and isinstance(file, QIODevice) and file.isOpen():
                file.close()

    def get_project_from_project_data(self, project_data) -> Project:
        project = Project(
            file_name=project_data[0],
            project_name=project_data[1],
            image_path=project_data[2],
            person_name=project_data[3]
        )

        for item_data in project_data[4:]:
            item = MarkItem.from_list_mark_data_to_item(item_data)
            project.add_mark_item(item)
        return project

    def export_result(self, path, project: Project, size: QSize, parent):
        tif_result = QImage(size, QImage.Format_RGB32)
        mark_items = project.get_mark_items()

        painter = QPainter()
        painter.begin(tif_result)
        for mark_item in mark_items:
            painter.fillPath(mark_item.get_outline(), mark_item.color)
        painter.end()
        tif_result_array = qimage2numpy(tif_result)
        Image.fromarray(tif_result_array).save(path)


if __name__ == '__main__':
    """TODO"""
