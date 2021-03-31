#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

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

        self.init_GPIO()

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

    def custom_output(self):
        if not self.enable:
            return
        print("GPIO ouput")
        if self.output_mode == 'low':
            print(GPIO.input(self.output_pin))
            GPIO.output(self.output_pin, GPIO.LOW)
            print(GPIO.input(self.output_pin))
            self.sleep(self.output_time)
            GPIO.output(self.output_pin, GPIO.HIGH)
            print(GPIO.input(self.output_pin))
        else:
            print(GPIO.input(self.output_pin))
            GPIO.output(self.output_pin, GPIO.HIGH)
            print(GPIO.input(self.output_pin))
            self.sleep(self.output_time)
            GPIO.output(self.output_pin, GPIO.LOW)
            print(GPIO.input(self.output_pin))

    def run(self):
        pass
