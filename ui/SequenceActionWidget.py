#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout

from ui.SequenceActionItemWidget import SequenceActionItemWidget

"""
TO DO LIST
"""


class SequenceActionWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(SequenceActionWidget, self).__init__(*args, **kwargs)
        self.label = QLabel("ggggg")

        self.config_path = config_path
        self.widget_list = []
        self.load_config()

    def init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground)

    def load_config(self):
        layout = QHBoxLayout()
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            # self.template_image_path = root.find('detect_items').find('template_image').tex
            for action in root.find('detect_items').findall('item'):
                index = action.find('index').text
                category = action.find('category').text

                widget = SequenceActionItemWidget(index, category)
                self.widget_list.append(widget)
                # widget.setStyleSheet('''background-color: red;''')

                layout.addWidget(widget)
        except FileNotFoundError as e:
            print("No config file was found.")
        except Exception as e:
            print(e)
        layout.addStretch()
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SequenceActionWidget('../appconfig/appconfig.xml')
    win.show()
    sys.exit(app.exec_())
