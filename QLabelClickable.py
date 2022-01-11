from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class QLabelClickable(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
