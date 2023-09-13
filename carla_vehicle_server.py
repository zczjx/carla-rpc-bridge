#!/usr/bin/env python3
import os
import sys
import random
import msgpackrpc
from gui_render import GuiRender
import time, threading

try:
    import queue
except ImportError:
    import Queue as queue

class VehicleServer(object):
    def __init__(self, ip_addr="localhost", port=18800):
        self.ip_addr = ip_addr
        self.port = port
        self.render = None
        self.gui_thread = threading.Thread(target=self.gui_render_flow)
        self.gui_thread.start()

    def __del__(self):
        self.gui_thread.join()

    def gui_render_flow(self):
        self.render = GuiRender()
        self.render.set_caption('VehicleServer')
        while True:
            metadata, sensor_data = self.render.get_render_queue()
            self.render.draw_image(height = metadata[b'height'],
                                   width = metadata[b'width'],
                                   image = sensor_data)
            self.render.flip_display()

    def push_camera_data(self, metadata, sensor_data):
        print(metadata)

    def push_gps_data(self, metadata, sensor_data):
        print(metadata)
        # print(sensor_data)
        # if(metadata['type'] != 'camera'):
        #    print(metadata)
        #    print(sensor_data)
        # if((self.render != None) and (metadata['type'] == 'camera')):
        # self.render.put_render_queue(image=(metadata, sensor_data))

class CameraService(object):
    def __init__(self, ip_addr="localhost", port=18800):
        self.ip_addr = ip_addr
        self.port = port
        self.render = None
        self.gui_thread = threading.Thread(target=self.gui_render_flow)
        self.gui_thread.start()

    def __del__(self):
        self.gui_thread.join()

    def push_camera_data(self, metadata, sensor_data):
        if(self.render != None):
            # print(metadata)
            self.render.put_render_queue(image=(metadata, sensor_data))

    def gui_render_flow(self):
        self.render = GuiRender()
        self.render.set_caption('camera service')
        while True:
            metadata, sensor_data = self.render.get_render_queue()
            self.render.draw_image(height = metadata[b'height'],
                                   width = metadata[b'width'],
                                   image = sensor_data)
            self.render.flip_display()

class GPSService(object):
    def __init__(self, ip_addr="localhost", port=18801):
        self.ip_addr = ip_addr
        self.port = port

    def push_gps_data(self, metadata, sensor_data):
        print(sensor_data)

def main():
    camera_service = msgpackrpc.Server(CameraService())
    camera_service.listen(msgpackrpc.Address("localhost", 18800))
    gps_service = msgpackrpc.Server(GPSService())
    gps_service.listen(msgpackrpc.Address("localhost", 18801))
    camera_service_thread = threading.Thread(target=camera_service.start)
    gps_service_thread = threading.Thread(target=gps_service.start)
    camera_service_thread.start()
    gps_service_thread.start()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        camera_service_thread.join()
        gps_service_thread.join()
        print('\n Services Cancelled by user. Bye!')


if __name__ == '__main__':
    main()
