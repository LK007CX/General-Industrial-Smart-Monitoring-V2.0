# !/usr/bin/python3
# -*- coding: UTF-8 -*-

class Student(object):
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def __str__(self):
        return "学号:{}--姓名:{}--年龄{}".format(self.id, self.name, self.age)

    # __repr__ = __str__


s = Student(111, "Bob", 18)
print(s)
