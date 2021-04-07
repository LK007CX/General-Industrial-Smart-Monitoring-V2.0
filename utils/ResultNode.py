#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class ResultNode:
    def __init__(self, index, result, time, label):
        self._index = index
        self._result = result  # True, False, None
        self._time = time
        self._label = label

    def set_result(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_time(self, time):
        self._time = time

    def get_time(self):
        return self._time

    def set_label(self, label):
        self._label = label

    def get_label(self):
        return self._label

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def __str__(self):
        return "[ResultNode] index:{}--label:{}--result:{}--time:{} ". \
            format(str(self._index), str(self._label), str(self._result), str(self._time))


if __name__ == '__main__':
    node = ResultNode(1, True)
    print(node)
