#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QHBoxLayout, QApplication, QPushButton


class LogItemWidget(QWidget):
    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, time, log, item, *args, **kwargs):
        super(LogItemWidget, self).__init__(*args, **kwargs)

        self._item = item

        self.timeLabel = QPushButton(time, objectName="timeLabel")
        self.logLabel = QPushButton(log, objectName="logLabel")

        self.init_ui()

    def init_ui(self):
        self.timeLabel.setDisabled(True)
        self.logLabel.setDisabled(True)
        """layout"""
        layout = QHBoxLayout(spacing=0)
        layout.setContentsMargins(3, 0, 0, 0)
        layout.addWidget(self.timeLabel)
        layout.addWidget(self.logLabel)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_StyledBackground)

    def doDeleteItem(self):
        """
        Delete item.
        :return: None
        """
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        """
        Determine the height of the item.
        :return: None
        """
        return QSize(200, 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    item_ = QListWidgetItem()
    win = LogItemWidget("time", "log", item_)
    win.show()
    sys.exit(app.exec_())
