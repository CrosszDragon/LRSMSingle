from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import pyqtSignal


class DockWidget(QDockWidget):

    close_event_signal = pyqtSignal(bool)

    def __init__(self, widget_title, parent=None):
        super(DockWidget, self).__init__(widget_title, parent)

    def closeEvent(self, event) -> None:
        self.close_event_signal.emit(False)
