#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QTabWidget, QDesktopWidget, QApplication

from ui.ActionSettingsWidget import ActionSettingsWidget
from ui.ApplicationSettingsWidget import ApplicationSettingWidget
from ui.CameraSettingsWidget import CameraSettingsWidget
from ui.ModelSettingsWidget import ModelSettingsWidget
from ui.OutputSettingsWidget import OutputSettingsWidget
from ui.RemoteCVSettingsWidget import RemoteCVSettingsWidget
from ui.VideoSaveSettingsWidget import VideoSaveSettingsWidget

"""
TO DO LIST
"""


class SystemSettingsTabWidget(QTabWidget):
    def __init__(self, config_path, *args, **kwargs):
        super(SystemSettingsTabWidget, self).__init__(*args, **kwargs)
        output_pin_list_ = ['15', '16', '18', '19']
        self.cameraSettingsTab = CameraSettingsWidget(config_path)
        self.actionSettingsWidget = ActionSettingsWidget(config_path)
        self.modelSettinsTab = ModelSettingsWidget(config_path)
        # self.dataUploadTab = DataUploadSettingsWidget(config_path)
        self.remoteCVTab = RemoteCVSettingsWidget(config_path)
        self.applicationSettingsTab = ApplicationSettingWidget(config_path)
        self.videoSaveSettingsWidget = VideoSaveSettingsWidget(config_path)
        self.outputSettingsWidget = OutputSettingsWidget(config_path, output_pin_list_)

        self.init_ui()
        self.center()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.addTab(self.cameraSettingsTab, "相机参数设置")
        self.addTab(self.outputSettingsWidget, "输出信号设置")
        self.addTab(self.videoSaveSettingsWidget, "视频存储设置")
        self.addTab(self.actionSettingsWidget, "动作顺序配置")
        self.addTab(self.modelSettinsTab, "模型参数设置")
        # self.addTab(self.dataUploadTab, "数据上报设置")
        self.addTab(self.remoteCVTab, "远程视频推送")
        self.addTab(self.applicationSettingsTab, "系统参数设置")
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon(QPixmap('icon/logo.png')))
        self.setAttribute(Qt.WA_StyledBackground)

    def center(self):
        screen = QDesktopWidget().screenGeometry()

        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SystemSettingsTabWidget("../appconfig/appconfig.xml")
    win.show()
    sys.exit(app.exec_())
