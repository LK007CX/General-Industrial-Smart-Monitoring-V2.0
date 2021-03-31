#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os

import cv2
from PyQt5.QtCore import QThread

"""
TO DO LIST
dynamic save video fps
"""


class SaveVideoThread(QThread):
    """
    Save video to the local disk storage.
    """

    def __init__(self, *args, **kwargs):
        super(SaveVideoThread, self).__init__(*args, **kwargs)
        self.out = None
        self.save_string = ''

    def start_save_task(self, save_string, width, height):
        """
        Start the save video task.
        :param save_string: where you want to save the video
        :param width: video width
        :param height: video height
        :return: None
        """
        self.save_string = save_string
        print("Video: Start to save work circle video.")
        print("Video: The video will save to：\t\t\t" + self.save_string)
        self.out = cv2.VideoWriter(self.save_string, cv2.VideoWriter_fourcc(*"DIVX"), 25, (width, height))

    def end_save_task(self, result, only_save_ng_video):
        """
        End the save video task.
        :param result: True or False
        :param only_save_ng_video: only save ng video
        :return: None
        """
        if self.out is not None:
            self.out.release()
            self.out = None
        try:
            if result:
                if only_save_ng_video:
                    os.remove(self.save_string)
                    print("Video: Work circle is OK, the video has been deleted。\n")
            else:
                print("Video: Work circle is NG, the video has been saved to " + str(self.save_string) + ".")
        except Exception as e:
            print(e)

    def write_frame_to_video_writer(self, image):
        """
        Write frame to the video writer in order to save the video to the local disk storage.
        :param image: current image emitted from the detect thread
        :return: None
        """

        if self.out is not None:
            self.out.write(image)
