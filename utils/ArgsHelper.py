#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class ArgsHelper(object):
    __slots__ = 'image', 'video', 'video_looping', 'rtsp', 'rtsp_latency', 'usb', 'onboard', 'copy_frame', 'do_resize', \
                'model_path', 'yolo_dim', 'names_file', 'thresh', 'category_num', \
                'camera_mode', 'camera_id', 'camera_ip', 'width', 'height', \
                'enable_remote_cv', \
                'enable_gpio_output', 'gpio_output_mode', 'gpio_output_time', 'gpio_output_pin', \
                'enable_video_save', 'only_save_ng_video', 'max_save_video_count', \
                'enable_auto_start', 'application_title', \
                'item_list', \
                'time_delay'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
