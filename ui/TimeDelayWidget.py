#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QApplication, QSpinBox


class TimeDelayWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(TimeDelayWidget, self).__init__(*args, **kwargs)
        self.timeDelayLabel = QLabel("设置超时时间(s)")
        self.timeDelaySpinBox = QSpinBox()
        self.init_ui()

    def init_ui(self):
        self.timeDelayLabel.setFixedWidth(100)
        self.timeDelaySpinBox.setFixedWidth(100)
        self.timeDelaySpinBox.setMinimum(0)
        self.timeDelaySpinBox.setMaximum(300)
        self.timeDelaySpinBox.setSingleStep(1)
        layout = QHBoxLayout()
        layout.addWidget(self.timeDelayLabel)
        layout.addStretch()
        layout.addWidget(self.timeDelaySpinBox)
        self.setLayout(layout)

    # def load_config(self):
    #     tree = ET.parse(self.config_path)
    #     root = tree.getroot()
    #     time_delay = root.find("detect_items").find("time_delay").text
    #     self.timeDelayComboBox.setCurrentText(time_delay)
    #
    # def showEvent(self, event):
    #     self.load_config()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TimeDelayWidget()
    win.show()
    sys.exit(app.exec_())
