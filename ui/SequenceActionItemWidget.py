#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication


class SequenceActionItemWidget(QWidget):

    def __init__(self, index, label, *args, **kwargs):
        super(SequenceActionItemWidget, self).__init__(*args, **kwargs)
        self.indexLabel = QLabel(index)
        self.actionNameLabel = QLabel(label)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.indexLabel)
        layout.addWidget(self.actionNameLabel)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_StyledBackground)

    def set_backgroundcolor(self, color):
        self.setStyleSheet('''QWidget {background-color: ''' + color + '''; border-radius: 10px;}''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SequenceActionItemWidget()
    win.show()
    sys.exit(app.exec_())
