#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import sys
import threading
import time

from PyQt5.QtCore import QThread

sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO


class GPIOThread(QThread):

    def __init__(self, args):
        super(GPIOThread, self).__init__()
        self.args = args

        self.enable = args.enable_gpio_output
        self.output_mode = args.gpio_output_mode
        self.output_time = args.gpio_output_time
        self.output_pin = args.gpio_output_pin

        self._lock = threading.RLock()

        self.init_GPIO()

        self.index = 0

    def __del__(self):
        GPIO.cleanup()

    def init_GPIO(self):
        """
        Initialize GPIO.
        :return: None
        """
        GPIO.setmode(GPIO.BOARD)
        if self.output_mode == 'low':
            GPIO.setup(self.output_pin, GPIO.OUT, initial=GPIO.HIGH)
        else:
            GPIO.setup(self.output_pin, GPIO.OUT, initial=GPIO.LOW)

    # def output(self):
    #     self._lock.acquire()  # acquire the lock
    #     try:
    #         if not self.enable:
    #             return
    #         if self.output_mode == 'low':
    #             print(GPIO.input(self.output_pin))
    #             GPIO.output(self.output_pin, GPIO.LOW)
    #             print(GPIO.input(self.output_pin))
    #             self.sleep(self.output_time)
    #             GPIO.output(self.output_pin, GPIO.HIGH)
    #             print(GPIO.input(self.output_pin))
    #         else:
    #             print(GPIO.input(self.output_pin))
    #             GPIO.output(self.output_pin, GPIO.HIGH)
    #             print(GPIO.input(self.output_pin))
    #             self.sleep(self.output_time)
    #             GPIO.output(self.output_pin, GPIO.LOW)
    #             print(GPIO.input(self.output_pin))
    #     finally:
    #         self._lock.release()  # release the lock

    def output(self):
        self._lock.acquire()  # acquire the lock
        pre = time.time()
        try:
            if not self.enable:
                return
            print(str(self.index) + " " + "output mode: " + str(self.output_mode) + " " + "output pin: " +
                  str(self.output_pin) + " " + "output time: " + str(self.output_time))
            if self.output_mode == 'low':
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(self.output_pin)))
                GPIO.output(self.output_pin, GPIO.LOW)
            else:
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(self.output_pin)))
                GPIO.output(self.output_pin, GPIO.HIGH)
            # replace the time.sleep()
            while True:
                if time.time() - pre > self.output_time:
                    break
            if self.output_mode == 'low':
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(self.output_pin)))
                GPIO.output(self.output_pin, GPIO.HIGH)
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(self.output_pin)))
                self.index += 1
            else:
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(self.output_pin)))
                GPIO.output(self.output_pin, GPIO.LOW)
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(self.output_pin)))
                self.index += 1
        finally:
            self._lock.release()  # release the lock

    def custom_output(self):
        # prevent thread blocking the program
        threading.Thread(target=self.output, args=()).start()

    def run(self):
        pass
