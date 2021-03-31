#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time

from utils.Item import Item


class TimeItem(Item):

    def __init__(self, time_delay, index):
        self.time_delay = time_delay
        self.start_time = time.time()
        self.index = index

    def allow_rotate(self, label, rect):
        if time.time() - self.start_time > self.time_delay:
            return True
        return False

    def reset(self):
        self.start_time = time.time()

    def __str__(self):
        return "[TimeItem] time delay:{}--start time:{}". \
            format(self.time_delay, self.start_time)


if __name__ == '__main__':
    now = time.time()
    time.sleep(1)
    print(time.time() - now)
    print(type(time.time() - now))
