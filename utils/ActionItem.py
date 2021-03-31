#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from datetime import datetime

from utils.Item import Item


class ActionItem(Item):
    __slots__ = 'index', 'category', 'confirm_frames', 'confirm_time', 'thresh', \
                'label_list', 'time_list', 'coordinate', 'done'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            self.label_list = []
            self.time_list = []
            self.done = False

    def reset(self):
        self.label_list = []
        self.time_list = []
        self.done = False

    def allow_rotate(self, label, rect):
        """
        A function that indicate whether the action is done.
        :param label: label
        :param rect: rect
        :return: True or False
        """
        if not self.intersect(rect, self.coordinate):
            # print("不在ROI区域")
            return False
        if (len(self.label_list) == self.confirm_frames) and (self.done != True):
            if self.confirm_time == 0:
                self.done = True
                print("Action " + "Index: " + str(self.index) + " Label: " + str(self.category) + ", has been done.")
                return True
            if self.confirm_frames == 1:
                self.done = True
                print("Action " + "Index: " + str(self.index) + " Label: " + str(self.category) + ", has been done.")
                return True
            if (len(self.time_list) > 1) and (self.time_list[-1] - self.time_list[0]).seconds > self.confirm_time:
                self.done = True
                print("Action " + "Index: " + str(self.index) + " Label: " + str(self.category) + ", has been done.")
                return True
        if label == self.category:
            if len(self.label_list) < self.confirm_frames:
                self.label_list.append(label)
            self.time_list.append(datetime.now())
        return False

    def intersect(self, box1, box2):
        """
        Whether the box1 and box2 is related.
        :param box1: box1
        :param box2: box2
        :return: True or False
        """
        middle_x = abs(box1.minx + box1.maxx - box2.minx - box2.maxx)
        x = abs(box1.minx - box1.maxx) + abs(box2.minx - box2.maxx)
        middle_y = abs(box1.miny + box1.maxy - box2.miny - box2.maxy)
        y = abs(box1.miny - box1.maxy) + abs(box2.miny - box2.maxy)
        if middle_x <= x and middle_y <= y:
            return True
        else:
            return False

    def __str__(self):
        return "[ActionItem] index:{}--category:{}--confirm frames:{}--confirm time:{}--thresh:{}".\
                 format(self.index, self.category, self.confirm_frames, self.confirm_time, self.thresh)