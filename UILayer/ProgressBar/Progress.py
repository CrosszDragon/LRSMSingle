# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 9:03
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : Progress.py
# @Project : UndoFrameWork
# @Software: PyCharm

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from UILayer.ProgressBar.ProgressDialog import Ui_Dialog


class Progress(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(Progress, self).__init__(parent)
        Ui_Dialog.setupUi(self, self)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def set_value(self, value):
        self.progressBar.setValue(value)

    def test(self):
        _x = 2000
        _y = 1500
        t = _x * _y
        last = now = 0
        for x in range(0, _x):
            for y in range(0, _y):
                now = int((x * y) / t * 100)
                if now > last:
                    last = now
                    print(now)
                    self.set_value(now)
                    QApplication.processEvents()
        self.set_value(100)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    progress = Progress()
    progress.setToolTip("正在导出， 请闹心等待")
    progress.show()
    progress.test()
    sys.exit(app.exec_())
