# -*- coding: utf-8 -*-
# @Time    : 2019/7/9 14:20
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : PolygonalChart.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm
import sys

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtChart import QChartView, QLineSeries, QValueAxis


class PolygonalChart(QDialog):

    def __init__(self, title: str, project_data, parent=None):
        super(PolygonalChart, self).__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        self._layout = QVBoxLayout(self)
        self._create_polygonal_chart(project_data)

    '''定义x轴及其相关属性'''
    def set_x_aix(self, years: []) -> QValueAxis:     # x轴坐标——年份
        x_aix = QValueAxis()
        x_aix.setRange(years[0], years[-1])
        x_aix.setLabelFormat('%d')
        x_aix.setGridLineVisible(True)
        x_aix.setTickCount(len(years))
        x_aix.setMinorTickCount(5)        # 每两个月一个小分级

        return x_aix

    '''定义y轴及其相关属性'''
    def set_y_aix(self, areas: []) -> QValueAxis:     # y轴坐标——面积
        ma = []
        for i in range(0, len(areas)):
            m = max(areas[i])
            ma.append(m)
        bound = max(ma)

        y_aix = QValueAxis()
        y_aix.setRange(0, int(bound))
        y_aix.setLabelFormat('%d')
        y_aix.setGridLineVisible(True)
        y_aix.setTickCount(11)
        y_aix.setMinorTickCount(4)

        return y_aix

    '''创建折线：确定各折点坐标并连接'''
    def create_lines(self, series: QLineSeries, years: [], areas: []) -> QLineSeries:   #

        # 创建曲线  series
        point_dict_list = {}
        for i in range(0, len(years)):    # 定义折线坐标点
            x = years[i]
            y = areas[i]
            points = "point_" + str(i)
            point_dict_list[points] = QPoint(x, y)

        point_list = []
        for point in point_dict_list:    # 定义折线点清单
            point_list.append(point_dict_list[point])

        series.append(point_list)

        return series

    '''根据不同类型创建不同折线'''
    def create_lines_to_types(self, types: []) -> dict:
        dict1 = {}
        for i in range(0, len(types)):
            lines = "series_" + str(i)
            dict1[lines] = QLineSeries()        # 实例化QLineSeries,创建曲线
            dict1[lines].setName(types[i])

        return dict1

    '''创建折线图'''

    def _create_polygonal_chart(self, mark_data):
        self.char_view = QChartView(self)
        self.char_view.setRenderHint(QPainter.Antialiasing)

        types = [a[0] for a in mark_data]
        # t = mark_data[0]
        years = [b[2] for b in mark_data]
        # y = mark_data[2]
        areas = [c[1] for c in mark_data]
        # a = mark_data[1]
        dict1 = self.create_lines_to_types(types)
        for i in range(0, len(types)):
            lines = "series_" + str(i)
            series = self.create_lines(dict1[lines], years[i], areas[i])
            series.setUseOpenGL(True)
            type_ = dict1[lines].name()
            for type_ in types:
                self.char_view.chart().addSeries(series)

        self.char_view.chart().createDefaultAxes()
        self.char_view.chart().setAxisX(self.set_x_aix(years[0]))  # 设置x,y轴属性
        self.char_view.chart().setAxisY(self.set_y_aix(areas))

        self.char_view.chart().setTitle("各地物类型面积变化折线图")
        self._layout.addWidget(self.char_view)
        # self.char_view.show()

    def closeEvent(self, QCloseEvent):
        del self._layout
        del self.char_view
        del self


if __name__ == '__main__':
    app = QApplication(sys.argv)
    years_ = [2015, 2016, 2017, 2018, 2019]

    areas1 = [1000, 250, 600, 750, 800]
    areas2 = [300, 780, 650, 440, 881]
    areas3 = [666, 321, 486, 777, 105]
    areas4 = [555, 213, 482, 641, 954]
    areas_ = [areas1, areas2, areas3, areas4]

    types_ = ["mountain", "woods", "lake", "building area"]
    colors_ = [Qt.yellow, Qt.black, Qt.darkBlue, Qt.gray]
    project_data = [["mountain", areas1, years_, Qt.yellow],
                    ["woods", areas2, years_, Qt.black],
                    ["lake", areas3, years_, Qt.darkBlue],
                    ["building area", areas4, years_, Qt.gray]]

    p = PolygonalChart("折线图", project_data)
    p.show()
    # p.create_polygonal_chart(project_data)
    sys.exit(app.exec_())