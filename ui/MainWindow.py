#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import time
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QHBoxLayout, QLabel,
                             QMainWindow, QMessageBox, QStatusBar, QVBoxLayout,
                             QWidget)

from ui.CountWidget import CountWidget
from ui.HeaderWidget import HeaderWidget
from ui.HistoryListView import HistoryListView
from ui.LogWidget import LogWidget
from ui.SequenceActionWidget import SequenceActionWidget
from ui.VideoWidget import VideoWidget
from utils.ActionItem import ActionItem
from utils.ArgsHelper import ArgsHelper
from utils.DeleteFileThread import DeleteFileThread
from utils.DetectTensorRT import DetectTensorRT
from utils.GPIOThread import GPIOThread
from utils.Rectangle import Rectangle
from utils.SaveVideoThread import SaveVideoThread

"""
TO DO LIST
"""

canRestart = True


def restart(twice):
    """
    Restart the PyQt Application.
    :param twice:
    :return: None
    """
    os.execl(sys.executable, sys.executable, *[sys.argv[0], "-t", twice])


class MainWindow(QMainWindow):

    def __init__(self, config_path, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.draw_list = []
        self.headerWidget = HeaderWidget(config_path, "AI智能监控01")
        self.videoWidget = VideoWidget()
        self.historyWidget = HistoryListView()
        self.sequenceActionWidget = SequenceActionWidget(config_path)
        self.logWidget = LogWidget()
        self.countWidget = CountWidget()
        self.statusBar = QStatusBar()

        self.config_path = config_path
        self.args = self.load_config()

        self.thread = None
        self.gpio_thread = None
        self.delete_file_thread = None
        self.saveVideoThread = None
        self.deleteFileThread = None

        self.init_ui()
        self.init_thread()

    def init_ui(self):
        self.statusBar.addPermanentWidget(QLabel("艾聚达信息技术（苏州）有限公司"))

        self.headerWidget.restartPushButton.clicked.connect(self.restartApplication)

        bottomLayout = QHBoxLayout(spacing=0)
        bottomLayout.setContentsMargins(0, 0, 0, 0)
        bottomLayout.addWidget(self.countWidget)
        bottomLayout.addWidget(self.logWidget)

        leftLayout = QVBoxLayout(spacing=0)
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.addWidget(self.videoWidget)
        leftLayout.addWidget(self.sequenceActionWidget)
        leftLayout.addLayout(bottomLayout)

        layout_ = QHBoxLayout(spacing=0)
        layout_.setContentsMargins(0, 0, 0, 0)
        layout_.addLayout(leftLayout)
        layout_.addWidget(self.historyWidget)

        layout = QVBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.headerWidget)
        layout.addLayout(layout_)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        """status bar"""
        self.setStatusBar(self.statusBar)

        self.setWindowTitle("GISM2020 MainUI")
        self.setWindowIcon(QIcon(QPixmap('icon/logo.png')))

        self.resize(QSize(1280, 720))
        self.setAttribute(Qt.WA_StyledBackground)

        self.setObjectName("MainWindow")
        self.center()

    def resizeEvent(self, QResizeEvent):
        """
        Keep video widget at a 16:9 ratio.
        :param QResizeEvent:
        :return: None
        """
        base = self.width() // 25
        self.videoWidget.setFixedSize(QSize(16 * base, 9 * base))

    def center(self):
        """
        Make the window show in the middle of the screen.
        :return: None
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def restartApplication(self):
        """
        Restart application.
        :return: None
        """
        result = QMessageBox.question(self, "提示", "是否重新启动程式?", QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            try:
                self.thread.cam.release()
                self.thread.quit()
            except Exception as e:
                print(e)
            time.sleep(1)
            self.close()
            global canRestart
            canRestart = True
        else:
            pass

    def load_config(self):
        """
        Load application configuration.
        :return: parameter
        """
        args = None
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()

            model_path = root.find('model').find('modelpath').text
            model_input_size = root.find('model').find('size').text
            names_file = root.find('model').find('labelsfile').text
            thresh = float(root.find('model').find('thresh').text)
            # print("================================")
            # print(thresh)
            # print(type(thresh))
            category_num = int(root.find('model').find('category_num').text)

            camera_mode = root.find('camera').find('mode').text
            camera_id = int(root.find('camera').find('camera_id').text)
            camera_ip = root.find('camera').find('ip').text
            camera_input_width = int(root.find('camera').find('width').text)
            camera_input_height = int(root.find('camera').find('height').text)

            enable_remote_cv = bool(int(root.find('remotecv').find('enable').text))

            enable_gpio_output = bool(int(root.find('output').find('enable').text))
            gpio_output_mode = root.find('output').find('mode').text
            gpio_output_time = float(root.find('output').find('time').text)
            gpio_output_pin = int(root.find('output').find('pin').text)

            enable_video_save = bool(int(root.find('video').find('enable').text))
            only_save_ng_video = bool(int(root.find('video').find('only_ng').text))
            max_save_video_count = int(root.find('video').find('max_save_count').text)

            enable_auto_start = bool(int(root.find('app').find('auto_start').text))
            application_title = root.find('app').find('application_title').text

            time_delay = int(root.find('detect_items').find('time_delay').text)

            self.headerWidget.titleLabel.setText(application_title)

            item_list = []
            for action in root.find('detect_items').findall('item'):
                index = int(action.find('index').text)
                category = action.find('category').text
                frames = int(action.find('frames').text)
                time = float(action.find('time').text)
                thresh_ = float(action.find('thresh').text)
                coordinate = action.find('coordinate').text
                minx = int(coordinate.split(',')[0])
                miny = int(coordinate.split(',')[1])
                maxx = int(coordinate.split(',')[2])
                maxy = int(coordinate.split(',')[3])
                rect = Rectangle((minx, miny), (maxx, maxy))
                self.draw_list.append(rect)
                item = ActionItem(index=index, category=category, confirm_frames=frames, confirm_time=time, \
                                  thresh=thresh_, coordinate=rect)
                item_list.append(item)

            if camera_mode == 'USB':
                args = ArgsHelper(image=None, video=None, video_looping=False, rtsp=None, rtsp_latency=200,
                                  usb=camera_id, onboard=None, copy_frame=False, do_resize=False,

                                  model_path=model_path, yolo_dim=model_input_size, names_file=names_file,
                                  thresh=thresh, category_num=category_num,

                                  camera_mode=camera_mode, camera_id=camera_id, camera_ip=camera_ip,
                                  width=camera_input_width, height=camera_input_height,

                                  enable_remote_cv=enable_remote_cv,

                                  enable_gpio_output=enable_gpio_output, gpio_output_mode=gpio_output_mode,
                                  gpio_output_time=gpio_output_time, gpio_output_pin=gpio_output_pin,

                                  enable_video_save=enable_video_save, only_save_ng_video=only_save_ng_video,
                                  max_save_video_count=max_save_video_count,

                                  enable_auto_start=enable_auto_start, application_title=application_title,

                                  item_list=item_list,

                                  time_delay=time_delay)
            elif camera_mode == 'RTSP':
                args = ArgsHelper(image=None, video=None, video_looping=False, rtsp=camera_ip, rtsp_latency=200,
                                  usb=None, onboard=None, copy_frame=False, do_resize=False,

                                  model_path=model_path, yolo_dim=model_input_size, names_file=names_file,
                                  thresh=thresh, category_num=category_num,

                                  camera_mode=camera_mode, camera_id=camera_id, camera_ip=camera_ip,
                                  width=camera_input_width, height=camera_input_height,

                                  enable_remote_cv=enable_remote_cv,

                                  enable_gpio_output=enable_gpio_output, gpio_output_mode=gpio_output_mode,
                                  gpio_output_time=gpio_output_time, gpio_output_pin=gpio_output_pin,

                                  enable_video_save=enable_video_save, only_save_ng_video=only_save_ng_video,
                                  max_save_video_count=max_save_video_count,

                                  enable_auto_start=enable_auto_start, application_title=application_title,

                                  item_list=item_list,

                                  time_delay=time_delay)
        except Exception as e:
            print(e)
        return args

    def showMessage(self, string):
        """
        Show message.
        :param string: string
        :return: None
        """
        self.statusBar.showMessage(string)

    def closeEvent(self, event):
        """
        Close event.
        :param event: event
        :return: None
        """
        global canRestart
        canRestart = False
        try:
            self.thread.cam.release()
            self.thread.quit()
            self.saveVideoThread.quit()
            self.deleteFileThread.quit()
        except Exception as e:
            print(e)

    def init_thread(self):
        try:
            self.thread = DetectTensorRT(self.args)
            self.saveVideoThread = SaveVideoThread()
            self.deleteFileThread = DeleteFileThread("./video/", self.args.max_save_video_count)
            self.gpio_thread = GPIOThread(args=self.args)
            self.thread.draw_list = self.draw_list
            self.thread.image_Signal.connect(self.videoWidget.handleDisplay)
            self.thread.partial_result_Signal.connect(self.handle_partial_result)
            self.thread.history_Signal.connect(self.historyWidget.addItem)
            self.thread.log_Signal.connect(self.logWidget.addLog)

            """for video saving"""
            self.thread.start_save_task_signal.connect(self.saveVideoThread.start_save_task)
            self.thread.end_save_task_signal.connect(self.saveVideoThread.end_save_task)
            self.thread.write_frame_to_video_writer_signal.connect(self.saveVideoThread.write_frame_to_video_writer)
            self.thread.gpio_signal.connect(self.gpio_thread.custom_output)
            self.thread.num_signal.connect(self.countWidget.set_value)
            self.thread.start()
            self.deleteFileThread.start()
        except Exception as e:
            print(e)
            self.thread.cam.release()
            self.thread.quit()
            self.saveVideoThread.quit()
            self.deleteFileThread.quit()

    def handle_partial_result(self, result):
        for i in range(len(result)):
            # print("Result[i].get_result(): " + str(result[i].get_result()))
            if result[i].get_result():  # True
                self.sequenceActionWidget.widget_list[i].set_backgroundcolor('green')
            elif result[i].get_result() is None:  # False
                # print(result)
                self.sequenceActionWidget.widget_list[i].set_backgroundcolor('#778899')
            elif result[i].get_result() is False:
                self.sequenceActionWidget.widget_list[i].set_backgroundcolor('#778899')
                time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow("../appconfig/appconfig.xml")
    win.show()
    sys.exit(app.exec_())
