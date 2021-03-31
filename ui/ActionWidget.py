#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

import cv2
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QComboBox, QDoubleSpinBox, \
    QSpinBox, QToolButton, QHBoxLayout, QApplication, QLabel

"""
TO DO LIST
"""


class ItemWidget(QWidget):
    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, class_list, template_image_path, item, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)

        self.class_list = class_list
        self._item = item  # keep a reference to the list item object
        self.img = cv2.imread(template_image_path, cv2.IMREAD_ANYCOLOR)

        self.indexLabel = QLabel("0")
        self.classComboBox = QComboBox(objectName='classComboBox')  # 检测类别
        self.framesSpinBox = QSpinBox(objectName='confirmFrames')  # 确认帧数
        self.timeDoubleSpinBox = QDoubleSpinBox(objectName='confirmTime')  # 确认时间
        self.threshDoubleSpinBox = QDoubleSpinBox(objectName='threshDoubleSpinBox')  # 置信度
        self.coordinateLabel = QLabel("[None, None] [None, None]", objectName="coordinateLabel")
        self.ROIToolButton = QToolButton(objectName="ROIToolButton")
        self.deleteToolButton = QToolButton(objectName='deleteToolButton')  # 删除按钮

        self.minx = None
        self.miny = None

        self.maxx = None
        self.maxy = None

        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """initialize data"""
        self.classComboBox.addItems(self.class_list)

        """set icon for button"""
        self.ROIToolButton.setIcon(QIcon(QPixmap('icon/roi.png')))
        self.deleteToolButton.setIcon(QIcon(QPixmap('icon/delete.png')))

        """icon size"""
        self.ROIToolButton.setIconSize(QSize(20, 20))
        self.deleteToolButton.setIconSize(QSize(20, 20))

        """slots"""
        self.deleteToolButton.clicked.connect(self.doDeleteItem)
        self.ROIToolButton.clicked.connect(self.editROI)

        """fixed size"""
        self.indexLabel.setFixedWidth(50)
        self.classComboBox.setFixedWidth(100)
        self.framesSpinBox.setFixedWidth(100)
        self.timeDoubleSpinBox.setFixedWidth(100)
        self.threshDoubleSpinBox.setFixedWidth(100)
        self.coordinateLabel.setFixedWidth(200)
        self.ROIToolButton.setFixedWidth(50)
        self.deleteToolButton.setFixedWidth(50)

        """data limit"""
        self.framesSpinBox.setMinimum(1)
        self.framesSpinBox.setMaximum(30)
        self.timeDoubleSpinBox.setMinimum(0.05)
        self.timeDoubleSpinBox.setMaximum(30)
        self.timeDoubleSpinBox.setSingleStep(0.05)
        self.threshDoubleSpinBox.setMinimum(0.1)
        self.threshDoubleSpinBox.setMaximum(1.0)
        self.threshDoubleSpinBox.setSingleStep(0.05)

        """alignment"""
        self.indexLabel.setAlignment(Qt.AlignCenter)
        self.coordinateLabel.setAlignment(Qt.AlignCenter)

        """layout"""
        layout = QHBoxLayout()
        layout.addWidget(self.indexLabel)
        layout.addWidget(self.classComboBox)
        layout.addWidget(self.framesSpinBox)
        layout.addWidget(self.timeDoubleSpinBox)
        layout.addWidget(self.threshDoubleSpinBox)
        layout.addWidget(self.coordinateLabel)
        layout.addWidget(self.ROIToolButton)
        layout.addWidget(self.deleteToolButton)
        self.setLayout(layout)

    def doDeleteItem(self):
        """
        Slot function for delete item.
        :return: None
        """
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        """
        Determine the height of the item.
        :return: None
        """
        return QSize(200, 40)

    def editROI(self):
        """
        Edit ROI for detection.
        :return: None
        """
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.onMouseAction)
        cv2.imshow('image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def onMouseAction(self, event, x, y, flags, param):
        """
        CV mouse action.
        :param event:
        :param x:
        :param y:
        :param flags:
        :param param:
        :return: None
        """
        global position1, position2

        image = self.img.copy()

        if event == cv2.EVENT_LBUTTONDOWN:  # press the left key
            position1 = (x, y)  # get the coordinates of the mouse (starting position)

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:  # hold down the left button and drag it
            cv2.rectangle(image, position1, (x, y), (0, 255, 0), 3)  # draw a rectangular selection box
            cv2.imshow('image', image)

        elif event == cv2.EVENT_LBUTTONUP:  # release the left button
            position2 = (x, y)  # get the final position of the mouse
            cv2.rectangle(image, position1, position2, (0, 0, 255), 3)  # draw the final rectangle
            cv2.imshow('image', image)
            self.coordinateLabel.setText(
                "[" + str(position1[0]) + ", " + str(position1[1]) + "]" + " [" + str(position2[0]) + ", " + str(
                    position2[1]) + "]")
            self.minx = position1[0]
            self.miny = position1[1]

            self.maxx = position2[0]
            self.maxy = position2[1]

            # cv2.destroyAllWindows()

    def setIndex(self, index):
        """
        Set the item index.
        :param index: the item index in the QListWidget
        :return: None
        """
        self.indexLabel.setText(str(index))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_list_ = ['person', 'ok', 'ng']
    output_pin_list_ = ['12', '14', '16', '18']
    item_ = QListWidgetItem()
    win = ItemWidget(class_list_, '../icon/cap.png', item_)
    win.show()
    sys.exit(app.exec_())
