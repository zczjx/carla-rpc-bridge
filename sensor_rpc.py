#!/usr/bin/env python3
import os
import sys
import random
import msgpackrpc

class cameraRPC(object):
    def __init__(self, ip_addr="localhost", port=18800):
        self.ip_addr = ip_addr
        self.port = port
        self.put_render_queue = None

    def set_put_render_callback(self, put_render_callback=None):
        self.put_render_queue = put_render_callback

    def push_camera_data(self, metadata, sensor_data):
        if(self.put_render_queue != None):
            self.put_render_queue(image=(metadata, sensor_data))

class gpsRPC(object):
    def __init__(self, ip_addr="localhost", port=18801):
        self.ip_addr = ip_addr
        self.port = port

    def push_gps_data(self, metadata, sensor_data):
        print(sensor_data)

class imuRPC(object):
    def __init__(self, ip_addr="localhost", port=18802):
        self.ip_addr = ip_addr
        self.port = port

    def push_imu_data(self, metadata, sensor_data):
        print(sensor_data)