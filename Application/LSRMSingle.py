# -*- coding: utf-8 -*-
# @Time    : 2019/7/17 19:44
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : LSRMSingle.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

import sys
# import time
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
from Application import ImagesRes  # 这个必要，要初始化资源
from PyQt5.QtWidgets import QApplication, QStyleFactory  # , QSplashScreen
from UILayer.MainWindowPk.MainWindow import MainWindow, QPixmapCache


def main():
    cache_size_in_kb = 700 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)  # 将缓存设置为700000千字节（684Mb左右）

    app = QApplication(sys.argv)

    # setup_app_form = QSplashScreen(QPixmap(":/ApplicationLoadImg2.png").scaled(800, 500))
    # setup_app_form.show()
    # setup_app_form.showMessage("正在努力加载数据...", Qt.AlignHCenter | Qt.AlignBottom, Qt.darkYellow)
    # time.sleep(12.)

    app.setOrganizationName("LRSM Ltd.")
    app.setOrganizationDomain("lrsm.eu")
    app.setApplicationName("LRSMSingleVersion")
    app.setStyle(QStyleFactory.create(QStyleFactory.keys()[-1]))

    form = MainWindow()
    form.showMaximized()

    # setup_app_form.finish(form)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
