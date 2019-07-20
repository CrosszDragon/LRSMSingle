# -*- coding: utf-8 -*-
# @Time    : 2019/7/17 19:44
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : App.py
# @Project : LSRMSingalVersion3
# @Software: PyCharm

import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from UILayer.MainWindowPk.MainWindow import MainWindow, QPixmapCache


def main():
    cache_size_in_kb = 700 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)  # 将缓存设置为700000千字节（684Mb左右）

    app = QApplication(sys.argv)
    app.setOrganizationName("LRSM Ltd.")
    app.setOrganizationDomain("lrsm.eu")
    app.setApplicationName("LRSMSingleVersion")

    app.setStyle(QStyleFactory.create(QStyleFactory.keys()[-1]))

    form = MainWindow()
    form.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
