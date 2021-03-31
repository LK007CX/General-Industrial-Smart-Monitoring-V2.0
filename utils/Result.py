#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from utils.ResultNode import ResultNode


class Result:

    def __init__(self, length):
        self._result_list = [None] * length
        self.init(length)

    def __len__(self):
        return len(self._result_list)

    def __getitem__(self, k):
        return self._result_list[k]

    def __str__(self):
        string = []
        for i in range(len(self)):
            node = self._result_list[i]
            string.append(str(node))
        return str(string)

    def init(self, length):
        for i in range(length):
            node = ResultNode(i, None)
            self._result_list[i] = node

    def set_node_result(self, index, result):
        self._result_list[index].set_result(result)

    def reset_result(self):
        for i in range(len(self)):
            self._result_list[i].set_result(None)

    def get_result(self):
        """
        Get result of a work circle.
        :return: True or False
        """
        for i in range(len(self)):
            if self._result_list[i].get_result() is None:
                return False
            if not self._result_list[i].get_result():
                return False
        return True


if __name__ == '__main__':
    from utils.ResultNode import ResultNode

    result = Result(10)
    for i in range(10):
        _ = True if i % 2 == 1 else False
        # node = ResultNode(i, _)
        result.set_node_result(i, _)
    print(result)
