#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication, QVBoxLayout, QSpinBox, QPushButton, \
    QSplitter

from ui.SwitchButton import SwitchButton

"""
TO DO LIST
"""


class VideoSaveSettingsWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(VideoSaveSettingsWidget, self).__init__(*args, **kwargs)

        self.config_path = config_path

        self.enableLabel = QLabel("启用视频保存")
        self.enableSwitchButton = SwitchButton()
        self.enableWidget = QWidget()

        self.onlyNGLabel = QLabel("只保存NG视频")
        self.onlyNGSwitchButton = SwitchButton()
        self.onlyNGWidget = QWidget()

        self.maxSaveCountLabel = QLabel("最大存储数量")
        self.maxSaveCountSpinBox = QSpinBox()

        self.saveVideoWidth = QLabel("存储视频分辨率")

        self.savePushButton = QPushButton("保存")

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """initialize data"""

        """slots"""
        self.savePushButton.clicked.connect(self.saveAction)

        """data limit"""
        self.maxSaveCountSpinBox.setMinimum(10)
        self.maxSaveCountSpinBox.setMaximum(500)
        self.maxSaveCountSpinBox.setSingleStep(10)

        """size"""
        width = 200
        self.enableSwitchButton.setFixedSize(QSize(40, 24))
        self.onlyNGSwitchButton.setFixedSize(QSize(40, 24))
        self.enableWidget.setFixedWidth(width)
        self.onlyNGWidget.setFixedWidth(width)
        self.enableLabel.setFixedWidth(width)
        self.onlyNGLabel.setFixedWidth(width)
        self.maxSaveCountLabel.setFixedWidth(width)
        self.maxSaveCountSpinBox.setFixedWidth(width)

        """enable widget"""
        enableLayout = QHBoxLayout(spacing=0)
        enableLayout.setContentsMargins(0, 0, 0, 0)
        enableLayout.addWidget(QLabel())
        enableLayout.addWidget(self.enableSwitchButton)
        self.enableWidget.setLayout(enableLayout)

        """only NG widget"""
        onlyNGLayout = QHBoxLayout(spacing=0)
        onlyNGLayout.setContentsMargins(0, 0, 0, 0)
        onlyNGLayout.addWidget(QLabel())
        onlyNGLayout.addWidget(self.onlyNGSwitchButton)
        self.onlyNGWidget.setLayout(onlyNGLayout)

        """top layout"""
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.enableLabel)
        topLayout.addWidget(self.enableWidget)

        """only NG layout"""
        onlyNGLayout_ = QHBoxLayout()
        onlyNGLayout_.addWidget(self.onlyNGLabel)
        onlyNGLayout_.addWidget(self.onlyNGWidget)

        """max save count layout"""
        maxSaveCountLayout = QHBoxLayout()
        maxSaveCountLayout.addWidget(self.maxSaveCountLabel)
        maxSaveCountLayout.addWidget(self.maxSaveCountSpinBox)

        """layout"""
        layout = QVBoxLayout()
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addLayout(topLayout)
        layout.addWidget(QLabel())
        layout.addLayout(onlyNGLayout_)
        layout.addWidget(QLabel())
        layout.addLayout(maxSaveCountLayout)
        layout.addWidget(QLabel())
        layout.addWidget(self.savePushButton, 0, Qt.AlignCenter)
        layout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(layout)

    def load_config(self):
        """
        Load application configuration.
        :return: None
        """
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            enable = root.find('video').find('enable').text
            only_ng = root.find('video').find('only_ng').text
            max_save_count = root.find('video').find('max_save_count').text

            enable = bool(int(enable))
            self.enableSwitchButton.setChecked(enable)

            only_ng = bool(int(only_ng))
            self.onlyNGSwitchButton.setChecked(only_ng)
            self.maxSaveCountSpinBox.setValue(int(max_save_count))
        except Exception as e:
            """Here will emit a signal."""
            print(e)

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            enable = self.enableSwitchButton.checked
            only_ng = self.onlyNGSwitchButton.checked
            root.find('video').find('enable').text = "1" if enable else "0"
            root.find('video').find('only_ng').text = "1" if only_ng else "0"
            root.find('video').find('max_save_count').text = str(self.maxSaveCountSpinBox.value())
            tree.write(self.config_path)
        except Exception as e:
            """Here will emit a signal."""
            print(e)

    def showEvent(self, QShowEvent):
        """
        Reload application configuration when widget show again.
        :param QShowEvent: ignore this
        :return: None
        """
        self.load_config()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = VideoSaveSettingsWidget("../appconfig/appconfig.xml")
    win.show()
    sys.exit(app.exec_())
