#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
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
        fixed_width = 150
        min_height = 75
        max_height = 90
        self._okLabel.setFixedWidth(fixed_width)
        self._okLabel.setMinimumHeight(min_height)
        self._okLabel.setMaximumHeight(max_height)

        self._ngLabel.setFixedWidth(fixed_width)
        self._ngLabel.setMinimumHeight(min_height)
        self._ngLabel.setMaximumHeight(max_height)

        self._percentLabel.setFixedWidth(fixed_width)
        self._percentLabel.setMinimumHeight(min_height)
        self._percentLabel.setMaximumHeight(max_height)

        self._totalLabel.setFixedWidth(fixed_width)
        self._totalLabel.setMinimumHeight(min_height)
        self._totalLabel.setMaximumHeight(max_height)

        topLayout = QHBoxLayout(spacing=2)
        topLayout.setContentsMargins(0, 0, 0, 0)
        bottomLayout = QHBoxLayout(spacing=2)
        bottomLayout.setContentsMargins(0, 0, 0, 0)
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
        self._okLabel.set_val(str(ok_num))
        self._ngLabel.set_val(str(ng_num))
        self._totalLabel.set_val(str(total_num))
        self._percentLabel.set_val(str(percent))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CountWidget()
    win.show()
    sys.exit(app.exec_())
