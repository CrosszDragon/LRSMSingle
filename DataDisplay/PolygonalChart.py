# -*- coding: utf-8 -*-
# @Time    : 2019/7/9 14:20
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : PolygonalChart.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

import sys


class PolygonalChart:

    def __init__(self, years=list(), areas=list(), types=list()):
        self.years = years
        self.areas = areas
        self.types = types

    '''定义x轴及其相关属性'''
    def set_x_aix(self, years: []) -> QValueAxis:     #x轴坐标——年份
        x_aix = QValueAxis()
        x_aix.setRange(years[0], years[-1])
        x_aix.setLabelFormat('%d')
        x_aix.setGridLineVisible(True)
        x_aix.setTickCount(len(years))
        x_aix.setMinorTickCount(5)        #每两个月一个小分级

        return x_aix

    '''定义y轴及其相关属性'''
    def set_y_aix(self, areas: []) -> QValueAxis:     #y轴坐标——面积
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
    def create_lines(self, series: QLineSeries, years: [], areas: []) -> QLineSeries:

        #创建曲线  series
        point_dict_list = {}
        for i in range(0, len(years)):    #定义折线坐标点
            x = years[i]
            y = areas[i]
            points = "point_" + str(i)
            point_dict_list[points] = QPoint(x, y)

        point_list = []
        for point in point_dict_list:    #定义折线点清单
            point_list.append(point_dict_list[point])

        series.append(point_list)

        return series

    '''根据不同类型创建不同折线'''
    def create_lines_to_types(self, types: []) -> dict:
        dict1 = {}
        for i in range(0, len(types)):
            lines = "series_" + str(i)
            dict1[lines] = QLineSeries()        #实例化QLineSeries,创建曲线
            dict1[lines].setName(types[i])

        return dict1

    '''创建折线图'''

    def create_polygonal_chart(self, years: [], areas: [], types: []):
        app = QApplication(sys.argv)
        char_view = QChartView()
        char_view.setGeometry(100, 100, 1000, 600)
        char_view.setRenderHint(QPainter.Antialiasing)

        dict1 = self.create_lines_to_types(types)
        for i in range(0, len(types)):
            lines = "series_" + str(i)
            series = self.create_lines(dict1[lines], years, areas[i])
            series.setUseOpenGL(True)
            type_ = dict1[lines].name()
            for type_ in types:
                char_view.chart().addSeries(series)

        char_view.chart().createDefaultAxes()
        char_view.chart().setAxisX(self.set_x_aix(years))  # 设置x,y轴属性
        char_view.chart().setAxisY(self.set_y_aix(areas))

        char_view.chart().setTitle("各地物类型面积变化折线图")
        char_view.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    #app = QApplication(sys.argv)

    p = PolygonalChart()
