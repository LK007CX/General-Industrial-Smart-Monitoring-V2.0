#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, \
    QPushButton, QHBoxLayout, QVBoxLayout, \
    QSplitter, QApplication, QDoubleSpinBox

from ui.SwitchButton import SwitchButton


class OutputSettingsWidget(QWidget):
    def __init__(self, config_path, output_pin_list, *args, **kwargs):
        super(OutputSettingsWidget, self).__init__(*args, **kwargs)
        self.output_pin_list = output_pin_list
        self.output_mode_list = ["低脉冲", "高脉冲"]

        self.config_path = config_path

        self.enableLabel = QLabel("启用输出")
        self.enableSwitchButton = SwitchButton()

        self.outputModeLabel = QLabel("输出模式")
        self.outputModeComboBox = QComboBox()

        self.outputTimeLabel = QLabel("输出时间")
        self.outputTimeDoubleSpinBox = QDoubleSpinBox()

        self.outputPinLabel = QLabel("输出引脚")
        self.outputPinComboBox = QComboBox()

        self.savePushButton = QPushButton("保存")
        self.enableWidget = QWidget()
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """slot"""
        self.savePushButton.clicked.connect(self.saveAction)

        """initialize data"""
        self.outputModeComboBox.addItems(self.output_mode_list)
        self.outputPinComboBox.addItems(self.output_pin_list)

        """data limit"""
        self.outputTimeDoubleSpinBox.setMinimum(0.05)
        self.outputTimeDoubleSpinBox.setMaximum(5)
        self.outputTimeDoubleSpinBox.setSingleStep(0.05)

        """size"""
        width = 200
        self.outputModeLabel.setFixedWidth(width)
        self.outputModeComboBox.setFixedWidth(width)
        self.outputTimeLabel.setFixedWidth(width)
        self.outputTimeDoubleSpinBox.setFixedWidth(width)
        self.outputPinLabel.setFixedWidth(width)
        self.outputPinComboBox.setFixedWidth(width)

        self.enableLabel.setFixedWidth(width)
        self.enableSwitchButton.setFixedSize(QSize(40, 24))
        self.enableWidget.setFixedWidth(width)

        """enable widget"""
        enableLayout = QHBoxLayout(spacing=0)
        enableLayout.setContentsMargins(0, 0, 0, 0)
        enableLayout.addWidget(QLabel())
        enableLayout.addWidget(self.enableSwitchButton)
        self.enableWidget.setLayout(enableLayout)

        """top layout"""
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.enableLabel)
        topLayout.addWidget(self.enableWidget)

        """output mode layout"""
        outputModeLayout = QHBoxLayout()
        outputModeLayout.addWidget(self.outputModeLabel)
        outputModeLayout.addWidget(self.outputModeComboBox)

        """output time layout"""
        outputTimeLayout = QHBoxLayout()
        outputTimeLayout.addWidget(self.outputTimeLabel)
        outputTimeLayout.addWidget(self.outputTimeDoubleSpinBox)

        """output pin layout"""
        outputPinLayout = QHBoxLayout()
        outputPinLayout.addWidget(self.outputPinLabel)
        outputPinLayout.addWidget(self.outputPinComboBox)

        """layout"""
        layout = QVBoxLayout()
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addLayout(topLayout)
        layout.addWidget(QLabel())
        layout.addLayout(outputModeLayout)
        layout.addWidget(QLabel())
        layout.addLayout(outputTimeLayout)
        layout.addWidget(QLabel())
        layout.addLayout(outputPinLayout)
        layout.addWidget(QLabel())
        layout.addWidget(self.savePushButton, 0, Qt.AlignCenter)
        layout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(layout)

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            enable = self.enableSwitchButton.checked
            root.find('output').find('enable').text = "1" if enable else "0"
            root.find('output').find('mode').text = 'low' if self.outputModeComboBox.currentText() == "低脉冲" else 'high'
            root.find('output').find('time').text = str(self.outputTimeDoubleSpinBox.value())
            root.find('output').find('pin').text = self.outputPinComboBox.currentText()
            tree.write(self.config_path)
        except Exception as e:
            """Here will emit a signal."""
            print(e)

    def load_config(self):
        """
        Load application configuration.
        :return: None
        """
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()

            enable = root.find('output').find('enable').text
            mode = root.find('output').find('mode').text
            time = root.find('output').find('time').text
            pin = root.find('output').find('pin').text

            enable = bool(int(enable))
            self.enableSwitchButton.setChecked(enable)
            if mode == "low":
                self.outputModeComboBox.setCurrentText("低脉冲")
            else:
                self.outputModeComboBox.setCurrentText("高脉冲")
            self.outputTimeDoubleSpinBox.setValue(float(time))
            self.outputPinComboBox.setCurrentText(pin)
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
    output_pin_list_ = ['13', '15', '16', '18']

    app = QApplication(sys.argv)
    win = OutputSettingsWidget("../appconfig/appconfig.xml", output_pin_list_)
    win.show()
    sys.exit(app.exec_())
