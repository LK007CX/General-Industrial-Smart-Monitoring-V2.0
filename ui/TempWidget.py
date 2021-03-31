#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication


class TempWidget(QWidget):
    def __init__(self, num, desc, color, *args, **kwargs):
        super(TempWidget, self).__init__(*args, **kwargs)
        self._numLabel = QLabel(num, objectName='numLabel')
        self._descLabel = QLabel(desc, objectName='descLabel')
        self._color = color
        self._init_ui()

    def _init_ui(self):
        self._numLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self._descLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self._numLabel.setStyleSheet('''color:white; font-size: 20px; font-family: "MicroSoft YaHei";''')
        self._descLabel.setStyleSheet('''color:white; font-size: 20px; font-family: "MicroSoft YaHei";''')
        layout = QVBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._numLabel)
        layout.addWidget(self._descLabel)
        self.setLayout(layout)

        # self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName("TempWidget")
        StyleSheet = '''QWidget {background-color: ''' + str(self._color) + ''';}'''
        self.setStyleSheet(StyleSheet)

    def set_val(self, val):
        self._numLabel.setText(val)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TempWidget("O", "合格数", "red")
    win.show()
    sys.exit(app.exec_())
