#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QListView, QHBoxLayout

from ui.LogItemWidget import LogItemWidget
from ui.SortFilterProxyModel import SortFilterProxyModel

"""
TO DO LIST
"""


class LogWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(LogWidget, self).__init__(*args, **kwargs)

        self.logListView = QListView()
        self.dmodel = QStandardItemModel(self.logListView)
        self.fmodel = SortFilterProxyModel(self.logListView)
        self.init_ui()
        # self.test_data()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.fmodel.setSourceModel(self.dmodel)
        self.logListView.setModel(self.fmodel)
        layout = QHBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.logListView)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_StyledBackground)

    def test_data(self):
        """
        Test data.
        :return: None
        """
        for i in range(50):
            times = time.time()
            self.addLog(str(times), '历史记录信息')

    def addLog(self, log_time, log):
        """
        Add log.
        :param log_time:
        :param log:
        :return: None
        """
        if self.logListView.model().rowCount() == 20:
            self.logListView.model().removeRow(19)

        times = time.time()
        value = '{}'.format(times)
        item = QStandardItem(value)
        item.setForeground(QColor("#19232D"))
        self.dmodel.appendRow(item)
        index = self.fmodel.mapFromSource(item.index())
        widget = LogItemWidget(log_time, log, item)
        item.setSizeHint(widget.sizeHint())
        self.logListView.setIndexWidget(index, widget)
        self.fmodel.sort(0, Qt.DescendingOrder)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LogWidget()
    win.show()
    sys.exit(app.exec_())
