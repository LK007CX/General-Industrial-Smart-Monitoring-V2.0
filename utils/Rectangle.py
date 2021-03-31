#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Rectangle:
    def __init__(self, pt1, pt2):
        self.minx = pt1[0]
        self.miny = pt1[1]
        self.maxx = pt2[0]
        self.maxy = pt2[1]

    def setValue(self, pt1, pt2):
        self.minx = pt1[0]
        self.miny = pt1[1]
        self.maxx = pt2[0]
        self.maxy = pt2[1]

    def getValue(self):
        return 0
