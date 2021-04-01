# -*- coding: utf-8 -*-

import sqlite3
import sys

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QPushButton, QLabel, QSplitter, \
    QHeaderView, QMessageBox, QDialog, QDateEdit, QTableWidget, QAbstractItemView, QTableWidgetItem


class DataGrid(QDialog):
    def __init__(self, *args, **kwargs):
        super(DataGrid, self).__init__(*args, **kwargs)
        self.setWindowTitle("查询")
        self.resize(750, 500)
        self.initUI()
        self.totalList = []

    def initUI(self):
        # 操作布局
        operatorLayout = QHBoxLayout()
        self.dateLabel = QLabel("选择日期")
        self.dateLabel.setFixedWidth(120)
        self.dateEdit = QDateEdit(QDate.currentDate())
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.dateEdit.setMaximumDate(QDate.currentDate().addDays(0))
        self.queryDataButton = QPushButton("查询数据")
        self.clearButton = QPushButton("清空")

        self.queryDataButton.clicked.connect(self.queryDataTrigger)
        self.queryDataButton.setEnabled(True)
        self.clearButton.clicked.connect(self.clearTrigger)
        self.clearButton.setEnabled(False)
        operatorLayout.addWidget(self.dateLabel)
        operatorLayout.addWidget(self.dateEdit)
        operatorLayout.addWidget(self.queryDataButton)
        operatorLayout.addWidget(self.clearButton)
        operatorLayout.addWidget(QSplitter())
        # 状态布局
        statusLayout = QHBoxLayout()
        self.totalRecordLabel = QLabel()
        self.totalRecordLabel.setFixedWidth(70)
        statusLayout.addWidget(QSplitter())
        statusLayout.addWidget(self.totalRecordLabel)
        # 设置表格属性
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["开始时间", "结束时间", "判断结果"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 创建界面
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(operatorLayout)
        mainLayout.addWidget(self.tableWidget)
        mainLayout.addLayout(statusLayout)
        self.setLayout(mainLayout)

    def queryDataTrigger(self):
        try:
            queryDate = self.dateEdit.date().toString("yyyy-MM-dd")
            conn = sqlite3.connect("db/" + queryDate + ".db")
            c = conn.cursor()
            c.execute('select * from result')
            while True:
                row = c.fetchone()
                if not row:
                    break
                templist = [row[1], row[2], row[3]]
                self.totalList.append(templist)
            c.close()
            conn.close()

            self.tableWidget.setRowCount(len(self.totalList))
            for i in range(0, len(self.totalList)):
                for j in range(0, 3):
                    item = QTableWidgetItem(self.totalList[i][j])
                    self.tableWidget.setItem(i, j, item)

            self.totalRecordLabel.setText("总数: " + str(len(self.totalList)))
            self.queryDataButton.setEnabled(False)
            self.clearButton.setEnabled(True)
        except Exception as e:
            print(e)
            QMessageBox.information(self, "Error", "没有相关数据", QMessageBox.Yes, QMessageBox.Yes)

    def clearTrigger(self):
        self.totalList.clear()
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
        self.queryDataButton.setEnabled(True)
        self.clearButton.setEnabled(False)
        self.totalRecordLabel.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DataGrid()
    win.show()
    sys.exit(app.exec_())
