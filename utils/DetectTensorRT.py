# !/usr/bin/python3
# -*- coding: UTF-8 -*-
import cgitb
import copy
import cv2
import datetime
import os
import sqlite3
import sys
import time

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer

import numpy as np
import pycuda.autoinit
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from optparse import OptionParser

from utils.ArgsHelper import ArgsHelper
from utils.CircleQueue import CircleQueue
from utils.ModelOutputItem import ModelOutputItem
from utils.Rectangle import Rectangle
from utils.camera import Camera
from utils.custom_classes import get_cls_dict
from utils.display import show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO

from utils.Result import Result
from utils.TimeItem import TimeItem
import logging

_width = '1280'
_height = '720'
global_image = np.ndarray(())


def restart(twice):
    """
    Restart the PyQt Application.
    :param twice:
    :return: None
    """
    os.execl(sys.executable, sys.executable, *[sys.argv[0], "-t", twice])


class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.number_frames = 0
        self.fps = 30
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width=' + _width + ',height=' + _height + ',framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96'.format(self.fps)

    def on_need_data(self, src, length):
        global global_image
        data = global_image.tostring()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        buf.fill(0, data)
        buf.duration = self.duration
        timestamp = self.number_frames * self.duration
        buf.pts = buf.dts = int(timestamp)
        buf.offset = timestamp
        self.number_frames += 1
        retval = src.emit('push-buffer', buf)

        if retval != Gst.FlowReturn.OK:
            print(retval)

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.set_address = '0.0.0.0'
        self.set_service = '8554'
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.get_mount_points().add_factory("/test", self.factory)
        self.attach(None)


class DetectTensorRT(QThread):
    image_Signal = pyqtSignal(np.ndarray)
    history_Signal = pyqtSignal(np.ndarray, str, str, str)
    log_Signal = pyqtSignal(str, str)
    gpio_signal = pyqtSignal()
    partial_result_Signal = pyqtSignal(Result)
    start_save_task_signal = pyqtSignal(str, int, int)
    end_save_task_signal = pyqtSignal(bool, bool)
    write_frame_to_video_writer_signal = pyqtSignal(np.ndarray)
    num_signal = pyqtSignal(int, int, int, float)

    def __init__(self, args, parent=None):
        super(DetectTensorRT, self).__init__(parent)
        self.args = args

        """for tensorrt_demos"""
        self.cam = None
        self.trt_yolo = None
        self.conf_th = args.thresh
        self.vis = None

        """for Item"""
        self.item_list = args.item_list
        self.item_dict = {item.category: item for item in self.item_list}
        self.cls_dict = None

        self.gpio_flag = False

        self.enable_video_save = args.enable_video_save
        self.enable_remote_cv = args.enable_remote_cv

        """for CircleQueue"""
        self.actionQueue = CircleQueue()
        self.current_action = None
        self.stop_action = None
        self.time_delay = None
        self.allow_close = False
        self.allow_time_dalay = False

        """for Results"""
        self.draw_list = None
        self.results = None

        self.logger = logging.getLogger("utils.DetectTensorRT")
        # self.logger.info("create an instance from utils.DetectTensorRT")

        """thread lock"""
        self._mutex = QMutex()

        self._thread_lock = QMutex()
        self._cond = QWaitCondition()
        self._isPause = False

        self.ok_num = 0
        self.ng_num = 0
    
    def resume(self):
        self._cond.wakeAll()
        print(str(datetime.datetime.now()) + " resume the detect thread")
    
    
    
    def pause_ng(self):
        self._isPause = False
        # self.logger.info(str(datetime.datetime.now()) + " resume the detect thread")

    def load_action(self):
        """enqueue the action to the CircleQueue"""
        for action in self.args.item_list:
            self.actionQueue.enqueue(action)

        """current action"""
        self.current_action = copy.deepcopy(self.actionQueue.first())
        self.logger.info("[Func] load_action - current action: \t" + str(self.current_action))

        """time action, play the role of time delay."""
        length = len(self.actionQueue)
        time_action = TimeItem(self.args.time_delay, length)
        self.actionQueue.enqueue(time_action)
        self.logger.info("[Func] load_action - time action: \t" + str(time_action))

        """rotate the CircleQueue, to reach the last element of the CircleQueue, to get the stop action."""
        for _ in range(len(self.actionQueue) - 2):
            self.actionQueue.rotate()
        """stop action"""
        self.stop_action = copy.deepcopy(self.actionQueue.first())
        self.logger.info("[Func] load_action - stop action: \t" + str(self.stop_action))

        """time daley action"""
        self.actionQueue.rotate()
        self.time_delay = copy.deepcopy(self.actionQueue.first())
        self.logger.info("[Func] load_action - time delay: \t" + str(self.time_delay))
        """return the head of the CircleQueue"""
        self.actionQueue.rotate()
        """represent the result of each circle."""
        self.results = Result(len(self.actionQueue) - 1)
        self.logger.info("[Func] load_action - results: \t" + str(self.results))

    def load_model(self):
        if self.args.category_num <= 0:
            raise SystemExit('ERROR: bad category_num (%d)!' % self.args.category_num)
        # print("===============================")
        # print(self.args.model_path)
        if not os.path.isfile(self.args.model_path):
            raise SystemExit('ERROR: model file %s not found!' % self.args.model_path)
        self.cam = Camera(self.args)
        if not self.cam.isOpened():
            # raise SystemExit('ERROR: failed to open camera!')
            self.logger.info("[Func] load_model - ERROR: failed to open camera, "
                             "try to restart the application to connect the camera/.")
            self.release_and_restart()
        self.cls_dict = get_cls_dict(self.args.names_file)
        yolo_dim = self.args.yolo_dim.split('*')[-1]
        if 'x' in yolo_dim:
            dim_split = yolo_dim.split('x')
            if len(dim_split) != 2:
                self.logger.info("[Func] load_model, ERROR: bad yolo_dim (%s), the application will be terminated.!"
                                 % yolo_dim)
                raise SystemExit('ERROR: bad yolo_dim (%s)!' % yolo_dim)
            w, h = int(dim_split[0]), int(dim_split[1])
        else:
            h = w = int(yolo_dim)
        if h % 32 != 0 or w % 32 != 0:
            self.logger.info("[Func] load_model, ERROR: bad yolo_dim (%s), the application will be terminated.!"
                             % yolo_dim)
            raise SystemExit('ERROR: bad yolo_dim (%s)!' % yolo_dim)
        self.trt_yolo = TrtYOLO(self.args.model_path, (h, w), self.args.category_num, cuda_ctx=pycuda.autoinit.context)
        self.vis = BBoxVisualization(self.cls_dict)

    def release_and_restart(self):
        self.cam.release()
        time.sleep(1)
        """program restart section"""
        parser = OptionParser(usage="usage:%prog [optinos] filepath")
        parser.add_option("-t", "--twice", type="int",
                          dest="twice", default=1, help="运行次数")
        options, _ = parser.parse_args()
        cgitb.enable(1, None, 5, '')

        restart(str(options.twice + 1))

    def partial_result(self, index, result, time, label):
        self.results.set_node_result(index, result, time, label)
        """emit a signal that will display the state of partial result."""
        self.partial_result_Signal.emit(self.results)

    def start_work(self, width, height, current_time):
        self.logger.info("******************************************************************************************")
        self.logger.info("[Func] start_work - Start of a work circle")

        """save circle video or not?"""
        if self.enable_video_save:
            self.start_save_task_signal.emit(current_time, width, height)

        """reset the results(nodes and start time, end time)"""
        self.results.reset_result()
        """new start time"""
        self.results.set_start_time(current_time)
        # print(self.results.get_start_time())
        # self.logger.info("[Func] start_work - after reset results - results: \t" + str(self.results))

        """emit the signal to main ui."""
        self.partial_result_Signal.emit(self.results)

    def end_work(self):
        self.allow_close = False
        self.allow_time_dalay = False
        """reset the CircleQueue"""
        for i in range(len(self.actionQueue)):
            self.actionQueue.rotate()
            if self.actionQueue.first().index == 0:
                """update the current action."""
                self.current_action = copy.deepcopy(self.actionQueue.first())
                break
        """reset the stop action."""
        self.time_delay.reset()
        self.stop_action.reset()
        # self.logger.info("[Func] end_work - after reset stop action - stop action: \t" + str(self.stop_action))
        # self.logger.info("[Func] end_work - after reset stop action - time delay: \t" + str(self.time_delay))

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.results.set_end_time(current_time)

        # database
        start_time = self.results.get_start_time()
        end_time = self.results.get_end_time()
        _ = "OK" if self.results.get_result() else "NG"
        self.insert_into_db(start_time, end_time, _)

        """if the result of the circle is OK or NG?"""
        if self.results.get_result():
            self.ok_num += 1
            self.num_signal.emit(self.ok_num, self.ng_num, self.ok_num + self.ng_num,
                                 round(self.ok_num / (self.ok_num + self.ng_num), 2))
            self.log_Signal.emit(current_time, "OK")
            """save circle video."""
            if self.enable_video_save:
                self.end_save_task_signal.emit(True, self.args.only_save_ng_video)
        else:
            self.ng_num += 1
            self.num_signal.emit(self.ok_num, self.ng_num, self.ok_num + self.ng_num,
                                 round(self.ok_num / (self.ok_num + self.ng_num), 2))
            self.log_Signal.emit(current_time, "NG")
            """do not save the video."""
            if not self.enable_video_save:
                self.end_save_task_signal.emit(False, self.args.only_save_ng_video)
            """GPIO output."""
            self.gpio_signal.emit()
        self.logger.info("[Func] end_work - Results: \t" + str(self.results))
        """reset the results."""
        self.results.reset_result()
        # self.logger.info("[Func] end_work - after reset results - results: \t" + str(self.results))
        """emit the signal to main ui."""
        self.partial_result_Signal.emit(self.results)
        self.logger.info("[Func] end_work - End of a work cycle")

    def loop_and_detect(self):
        SAVE_INTERVAL = 0
        detect_labels = [item.category for item in self.item_list]  # all labels to be detected
        fps = 0.0
        tic = time.time()  # to calculate the fps
        img = self.cam.read()
        if img is not None:
            cv2.imwrite("icon/template.jpg", img)
        while True:
            # self._thread_lock.lock()
            if self._isPause:
                continue
            # self.logger.info("[Func] loop_and_detect - Start a image detect circle")
            img = self.cam.read()
            if img is None:
                break
            
            stop_flag = True  # to assert the timeout function can be carried out

            boxes, confs, clss = self.trt_yolo.detect(img, self.conf_th)  # model output results

            # filter labels
            if len(boxes) > 0:
                current_labels = [self.cls_dict[i] for i in clss]  # all current Tags，str
                index = [i for i in range(len(current_labels)) if current_labels[i] in detect_labels]
                boxes = [list(boxes[i]) for i in index]
                confs = [confs[i] for i in index]
                clss = [clss[i] for i in index]

            # transform this to ModelOutputItem
            model_output_list = [ModelOutputItem(box=boxes[i], confidence=confs[i], cls=clss[i], cls_dict=self.cls_dict)
                                 for i in range(len(boxes))]

            # self.logger.info("[Func] loop_and_detect - start analysis the model output result")

            # it is assumed that the detection label is not repeated,
            # but the model output label can be repeated
            for modelOutputItem in model_output_list:
                label = modelOutputItem.label
                box = modelOutputItem.box
                conf = modelOutputItem.confidence
                cls = modelOutputItem.cls
                ####################### self.logger.info("[Func] loop_and_detect - ModelOutputItem: \t" + str(modelOutputItem))

                """to calculate the relationship of the current output and the setting."""
                rect = Rectangle((box[0], box[1]), (box[2], box[3]))

                if self.current_action.allow_rotate(label, rect):
                    self.partial_result(self.current_action.index, True, self.current_action.get_time(),
                                        self.current_action.category)
                    """emit history image to main window"""
                    history_image = self.vis.draw_bboxes(img, [box], [conf], [cls])
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.history_Signal.emit(history_image, label, str(box), current_time)
                    # end time
                    if self.current_action.index == (len(self.actionQueue) - 2):
                        # self.logger.info("[Func] loop_and_detect - do end_work")
                        # self.logger.info("[Func] loop_and_detect - current ModelOutputItem: \n" + str(modelOutputItem))
                        self.end_work()  # in func end_work, the CircleQueue will be reset correctly.
                    else:
                        # just rotate the action circle queue with one step
                        # self.logger.info("[Func] loop_and_detect - rotate the CircleQueue")
                        # self.logger.info("[Func] loop_and_detect - current ModelOutputItem: \n" + str(modelOutputItem))
                        self.actionQueue.rotate()

                    # update current action
                    self.current_action = copy.deepcopy(self.actionQueue.first())
                    # self.logger.info("[Func] loop_and_detect - current action: \n" + str(self.current_action))

                    # time.sleep(0.5)
                    if self.current_action.index == 0:
                        # self.logger.info("[Func] loop_and_detect - do start_work")
                        self.start_work(self.args.width, self.args.height, current_time)

                    # allow close the circle
                    if self.current_action.index == 1:
                        self.allow_close = True
                        self.allow_time_dalay = True
                        self.stop_action.reset()
                        self.time_delay.reset()
                        # self.logger.info("[Func] loop_and_detect - change allow_close to: " + str(self.allow_close))

                    if self.current_action.index == len(self.actionQueue) - 2:
                        self.allow_close = False
                        self.stop_action.reset()

                stop_flag = False
                if self.allow_close:
                    if self.stop_action.allow_rotate(label, rect):

                        # self.allow_close = False

                        # self.logger.info("[Func] loop_and_detect - change allow_close to: " + str(self.allow_close))

                        history_image = self.vis.draw_bboxes(img, [box], [conf], [cls])
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.history_Signal.emit(history_image, "End early", "[None, None, None, None]", current_time)

                        for node in self.results:
                            if node.get_result() is None:
                                node.set_result(False)
                        # self.logger.info(
                        #     "[Func] loop_and_detect - reset the remain node in results: \n" + str(self.results))
                        self.logger.info("[Func] loop_and_detect - End early - do end_work")
                        self.end_work()
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.start_work(self.args.width, self.args.height, current_time)
                if self.allow_time_dalay:
                    if self.time_delay.allow_rotate(label, rect):

                        # self.allow_close = False

                        # self.logger.info("[Func] loop_and_detect - change allow_close to: " + str(self.allow_close))

                        history_image = self.vis.draw_bboxes(img, [box], [conf], [cls])
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.history_Signal.emit(history_image, "Timeout", "[None, None, None, None]", current_time)

                        for node in self.results:
                            if node.get_result() is None:
                                node.set_result(False)
                        # self.logger.info(
                        #     "[Func] loop_and_detect - reset the remain node in results: \n" + str(self.results))
                        self.logger.info("[Func] loop_and_detect - Time out - do end_work")
                        self.end_work()
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.start_work(self.args.width, self.args.height, current_time)

            if stop_flag:
                if self.allow_time_dalay:
                    if self.time_delay.allow_rotate(label, rect):
                        # self.allow_close = False
                        # self.logger.info("[Func] loop_and_detect - change allow_close to: " + str(self.allow_close))
                        history_image = self.vis.draw_bboxes(img, [box], [conf], [cls])
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.history_Signal.emit(history_image, "Timeout", "[None, None, None, None]", current_time)

                        # set the remain node in the result
                        for node in self.results:
                            if node.get_result() is None:
                                node.set_result(False)
                        # self.logger.info(
                        #     "[Func] loop_and_detect - reset the remain node in results: \n" + str(self.results))
                        self.logger.info("[Func] loop_and_detect - Time out - do end_work")
                        self.end_work()
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.start_work(self.args.width, self.args.height, current_time)

            img = self.vis.draw_bboxes(img, boxes, confs, clss)

            

            # for rect in self.draw_list:
            #     cv2.rectangle(img, (rect.minx, rect.miny), (rect.maxx, rect.maxy), (255, 89, 2), 2)

            img = show_fps(img, fps)
            self.image_Signal.emit(img)

            if self.enable_remote_cv:
                global global_image
                global_image = copy.deepcopy(img)

            if self.enable_video_save and SAVE_INTERVAL % 2 == 0:
            # if self.enable_video_save:
                self.write_frame_to_video_writer_signal.emit(copy.deepcopy(img))
                self._isPause = True
                # self._cond.wait(self._thread_lock)  # pause the thread
                # self.logger.info(str(datetime.datetime.now()) + " pause the detect thread")
            # update the SAVE_INTERVAL
            SAVE_INTERVAL += 1
            if SAVE_INTERVAL == 1000:
                SAVE_INTERVAL = 0
            toc = time.time()
            curr_fps = 1.0 / (toc - tic)
            # 计算fps数的指数衰减平均值
            fps = curr_fps if fps == 0.0 else (fps * 0.95 + curr_fps * 0.05)
            tic = toc
            # self._thread_lock.unlock()

    def insert_into_db(self, start_time, end_time, result):
        self._mutex.lock()
        try:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect("db/" + current_date + ".db")
            c = conn.cursor()
            c.execute('''create table if not exists result(
                id integer primary key autoincrement,
                start time text,
                end time text,
                result text
            )
            ''')
            sql_str = []
            sql_str.append(start_time)
            sql_str.append(end_time)
            sql_str.append(result)
            temp = tuple(sql_str)
            c.execute('insert into result values (null, ?, ?, ?)', temp)
            conn.commit()
            c.close()
            conn.close()
        finally:
            self._mutex.unlock()

    def run(self):
        try:
            self.load_action()
            self.load_model()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.start_work(self.args.width, self.args.height, current_time)
            self.loop_and_detect()
        finally:
            self.cam.release()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    args = ArgsHelper(image=None, video=None, video_looping=False, rtsp=None, rtsp_latency=200, usb=1, onboard=None,
                      copy_frame=False, do_resize=False, width=640, height=480, category_num=80,
                      model='yolov4-tiny-416')
    thread1 = DetectTensorRT(args)
    thread1.start()
    sys.exit(app.exec_())
