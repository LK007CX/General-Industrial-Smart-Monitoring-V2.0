#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class ResultNode:
    def __init__(self, index, result):
        self._index = index
        self._result = result  # True, False, None

    def set_result(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def __str__(self):
        # return "FF"
        return str(self._result)


if __name__ == '__main__':
    node = ResultNode(1, True)
    print(node)
