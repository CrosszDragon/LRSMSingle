# -*- coding: utf-8 -*-
# @Time    : 2019/7/9 14:08
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : DisplayProjectData.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPointF
from PyQt5.QtChart import *      #QChartView, QLineSeries, QChart, QValueAxis

import sys
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diagram_pra.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtChart import QChartView
from ThreeChart.use_polygonal_chart import *
from ThreeChart.use_histogram import *
from ThreeChart.use_pie_chart import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.setWindowTitle("图表显示")

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.status = self.statusBar()
        self.status.showMessage("完成", 5000)
        self.setStatusBar(self.statusbar)

        self.layout = QVBoxLayout()

        self.pushButton_pochart = QPushButton("折线图", self)
        self.pushButton_pochart.setGeometry(QtCore.QRect(30, 40, 75, 23))
        self.pushButton_pochart.setObjectName("pushButton_pochart")
        self.layout.addWidget(self.pushButton_pochart)

        self.pushButton_pochart1 = QPushButton("柱状图", self)
        self.pushButton_pochart1.setGeometry(QtCore.QRect(30, 80, 75, 23))
        self.pushButton_pochart1.setObjectName("pushButton_pochart")
        self.layout.addWidget(self.pushButton_pochart1)

        self.pushButton_pochart2 = QPushButton("饼状图", self)
        self.pushButton_pochart2.setGeometry(QtCore.QRect(30, 120, 75, 23))
        self.pushButton_pochart2.setObjectName("pushButton_pie")
        self.layout.addWidget(self.pushButton_pochart2)

        self.label = QLabel("输入年份", self)
        self.label.setGeometry(QtCore.QRect(120, 40, 80, 30))
        self.label.setObjectName("label")
        # layout.addWidget(QLabel("输入年份", self))
        self.layout.addWidget(self.label)

        self.combobox1 = QComboBox(self, minimumWidth=200)
        self.combobox1.setGeometry(QtCore.QRect(220, 40, 80, 30))
        self.combobox1.setObjectName("comboBox")
        self.layout.addWidget(self.combobox1)
        self.layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.init_combobox1()   # 初始化下拉列表
        self.combobox1.setCurrentIndex(0)    # 设置下拉列表默认值
        self.combobox1.activated.connect(self.pie_chart)

        self.init_chart()
        # self.layout.addWidget(self.charView1)

        # main_frame = QWidget()
        # self.setCentralWidget(main_frame)
        # main_frame.setLayout(layout)

        self.pushButton_pochart.clicked.connect(self.polygonal_chart)
        self.pushButton_pochart1.clicked.connect(self.histogram)
        self.pushButton_pochart2.clicked.connect(self.pie_chart)

        self.setLayout(self.layout)

    # 初始化下拉列表可选内容
    def init_combobox1(self):
        self.years = [2015, 2016, 2017, 2018, 2019]
        for i in range(len(self.years)):
            self.combobox1.addItem(str(self.years[i]))
        self.combobox1.setCurrentIndex(-1)

    # 返回下拉列表选中的文本内容：年份
    def get_selected_year(self):
        y = self.combobox1.currentText()
        selected_year = int(y)
        return selected_year

    def init_chart(self):
        # self.chart = QChart()
        # self.charView1 = QChartView(self.chart, self)
        self.charView1 = QChartView(self)  # 定义charView1，父窗体类型为 Window
        self.charView1.setGeometry(10, 160, 360, 400)  # 设置charView1位置、大小
        # charView1.resize(800, 600)
        self.charView1.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        # self.charView1.chart().setBackgroundVisible(True)
        # self.charView1.chart().removeAllSeries()
        self.layout.addWidget(self.charView1)

        self.charView2 = QChartView(self)
        self.charView2.setGeometry(375, 160, 360, 400)
        self.charView2.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(self.charView2)

    """
    def clear_chart(self):
        series = QLineSeries()
        point1 = QPoint(0, 0)
        p = [point1]
        series.append(p)
        self.charView1.chart().addSeries(series)    # 添加折线
        self.charView1.show()
    """

    def polygonal_chart(self):
        char_view = self.charView1
        # char_view.Series["yyzq.net"].Points.Clear();
        # self.layout.removeWidget(char_view)
        self.init_chart()

        years_ = [2015, 2016, 2017, 2018, 2019]
        areas1 = [1000, 250, 600, 750, 800]
        areas2 = [300, 780, 650, 440, 881]
        areas3 = [666, 321, 486, 777, 105]
        areas4 = [555, 213, 482, 641, 954]
        areas_ = [areas1, areas2, areas3, areas4]
        types_ = ["mountain", "woods", "lake", "building area"]

        p = PolygonalChart()
        # p.create_polygonal_chart(years_, girth_, types_)
        p.create_polygonal_chart(years_, areas_, types_, char_view)

    def histogram(self):
        years_ = [1, 2, 3, 4, 5, 6]
        areas_ = [[141, 400, 700, 460], [120, 50, 340, 55], [141, 400, 700, 460], [120, 50, 340, 55],
                  [120, 50, 340, 55], [141, 400, 700, 460]]
        types_ = ["mountain", "woods", "lake", "building area"]
        a = QApplication(sys.argv)
        demo = Histogram(years_, areas_, types_)  # , self.charView1
        demo.show()
        sys.exit(a.exec_())
        # time.sleep(5)

    def pie_chart(self):
        char_view = self.charView2
        # self.layout.removeWidget(char_view)
        # self.clear_chart()
        self.init_chart()

        years_ = [2015, 2016, 2017, 2018, 2019]
        areas1 = [1000, 250, 600, 750, 800]
        areas2 = [300, 780, 650, 440, 881]
        areas3 = [666, 321, 486, 777, 105]
        areas4 = [555, 213, 482, 641, 954]
        areas_ = [areas1, areas2, areas3, areas4]
        types_ = ["mountain", "woods", "lake", "building area"]

        pi = PieChart(years_, areas_, types_,)
        year = self.get_selected_year()
        pi.create_pie_chart(year, char_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("黑体")
    point_size = font.pointSize()
    font.setPixelSize(point_size * 90 / 72)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

'''
1.QChartView : 是一个可以显示图表（chart）的独立部件。
2.QChart : 用于创建图表。
3.series : 存储的一系列坐标；

4.QValueAxis : 继承自QAbstractAxis,用于对坐标轴进行操作。
流程: 坐标附加到series然后使用addSeries方法把series载入ChartView。
'''
