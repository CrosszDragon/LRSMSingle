# -*- coding: utf-8 -*-
# @Time    : 2019/7/9 14:21
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : PieChart.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPen, QPainter
from PyQt5.QtChart import QPieSeries, QChartView


class PieChart(QDialog):

    def __init__(self, title: str, project_data, parent=None):
        super(PieChart, self).__init__(parent)
        self.setWindowTitle(title)
        self._layout = QVBoxLayout(self)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self._create_pie_chart(project_data)

    '''定义饼状图并获取各区间信息'''
    def get_data(self, mark_data):
        pie_series = QPieSeries()  # 定义PieSeries
        total_area = 0
        for j in range(len(mark_data)):
            total_area += mark_data[j][1]
        for j in range(len(mark_data)):
            percentage = mark_data[j][1] / total_area * 100
            str1 = "{:.1f}%".format(percentage) + mark_data[j][0]
            pie_series.append(str1, mark_data[j][1])
        return pie_series

    '''绘制饼状图各区间'''
    def set_slice(self, pie_series: QPieSeries, mark_data) -> QPieSeries:
        for i in range(len(mark_data)):
            slice_ = pie_series.slices()[i]   # 地道饼图的某一个元素切片
            slice_.setLabelVisible()   # 设置各区域文本标签
            slice_.setPen(QPen(Qt.darkGreen, 0))            # 设置画笔类型——边界线颜色
            slice_.setBrush(mark_data[i][2])       # 设置笔刷——区域颜色
        return pie_series

    '''绘制饼状图并显示'''
    def _create_pie_chart(self, project_data: tuple):
        font = QFont("黑体")
        point_size = font.pointSize()
        font.setPixelSize(point_size * 90 / 72)

        self.char_view = QChartView(self)     # 将父窗体设置为空，设置为独立窗口
        self.char_view.setFont(font)
        self.char_view.setGeometry(100, 100, 800, 600)     # 设置窗口位置和大小
        self.char_view.setRenderHint(QPainter.Antialiasing)    # 消除锯齿

        pie = self.get_data(project_data)    # 获取区域种类及占比信息

        pie_series = self.set_slice(pie, project_data)          # 绘制饼状图各区间
        self.char_view.chart().addSeries(pie_series)     # 将饼状图添加至charView中
        self.char_view.chart().setTitle("各类型地物占比")    # 设置标题
        self.char_view.chart().legend().hide()
        self._layout.addWidget(self.char_view)

    def closeEvent(self, QCloseEvent):
        del self._layout
        del self.char_view
        del self


if __name__ == '__main__':

    years_ = [2015, 2016, 2017, 2018, 2019]
    areas1 = [1000, 250, 600, 750, 800, 100]
    areas2 = [300, 780, 650, 440, 881, 800]
    areas3 = [666, 321, 486, 777, 105, 100]
    areas4 = [555, 213, 482, 641, 954, 1000]
    areas5 = [555, 213, 482, 641, 954, 100]
    areas_ = [areas1, areas2, areas3, areas4, areas5]
    types_ = ["mountain", "woods", "lake", "building area", "傻逼"]
