#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication

from ui.TempWidget import TempWidget

StyleSheet = """
#okLabel {
    background-color: red;
}
#ngLabel {
    background-color: red;
}
#percentLabel {
    background-color: red;
}
#totalLabel {
    background-color: red;
}
"""


class CountWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(CountWidget, self).__init__(*args, **kwargs)
        self._okLabel = TempWidget("0", "合格数", "#556B2F", objectName="okLabel")
        self._ngLabel = TempWidget("0", "不合格数", "FireBrick", objectName="ngLabel")
        self._percentLabel = TempWidget("0", "良率", "orangered", objectName="percentLabel")
        self._totalLabel = TempWidget("0", "总数", "steelblue", objectName="totalLabel")

        self._init_ui()

    def _init_ui(self):
        self._okLabel.setMinimumSize(QSize(100, 50))
        self._ngLabel.setMinimumSize(QSize(100, 50))
        self._percentLabel.setMinimumSize(QSize(100, 50))
        self._totalLabel.setMinimumSize(QSize(100, 50))

        topLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()
        topLayout.addWidget(self._okLabel)
        topLayout.addWidget(self._ngLabel)
        bottomLayout.addWidget(self._totalLabel)
        bottomLayout.addWidget(self._percentLabel)
        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName("CountWidget")
        self.setStyleSheet(StyleSheet)

    def set_value(self, ok_num, ng_num, total_num, percent):
        self._okLabel.set_val(ok_num)
        self._ngLabel.set_val(ng_num)
        self._totalLabel.set_val(total_num)
        self._percentLabel.set_val(percent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CountWidget()
    win.show()
    sys.exit(app.exec_())
