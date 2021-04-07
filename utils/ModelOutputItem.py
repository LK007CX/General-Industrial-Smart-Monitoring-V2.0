# -*- coding: utf-8 -*-
# /usr/bin/python3


class ModelOutputItem:
    __slots__ = 'box', 'confidence', 'cls', 'label', 'cls_dict'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        self.label = self.cls_dict[self.cls]

    def __str__(self):
        return '[ModelOutputItem] box:{}--confidence:{}--cls:{}--label:{}'.format(self.box, self.confidence, self.cls,
                                                                                  self.label)
