#!/usr/bin/env python3
import os
import sys
import random
import msgpackrpc
from gui_render import GuiRender
from sensor_rpc import cameraRPC, gpsRPC, imuRPC
import time, threading

try:
    import queue
except ImportError:
    import Queue as queue

class SensorServer(object):
    def __init__(self, rig=''):
        self.init_camera_service()
        self.init_gps_service()
        self.init_imu_service()

        self.render = None
        self.gui_thread = threading.Thread(target=self.gui_render_flow)

    def __del__(self):
        self.gui_thread.join()
        self.camera_service.stop()
        self.camera_service_thread.join()
        self.gps_service.stop()
        self.gps_service_thread.join()
        self.imu_service.stop()
        self.imu_service_thread.join()

    def init_camera_service(self):
        self.camera_rpc = cameraRPC()
        self.camera_service = msgpackrpc.Server(self.camera_rpc)
        self.camera_service.listen(msgpackrpc.Address("localhost", 18800))
        self.camera_service_thread = threading.Thread(target=self.camera_service.start)

    def init_gps_service(self):
        self.gps_service = msgpackrpc.Server(gpsRPC())
        self.gps_service.listen(msgpackrpc.Address("localhost", 18801))
        self.gps_service_thread = threading.Thread(target=self.gps_service.start)

    def init_imu_service(self):
        self.imu_service = msgpackrpc.Server(imuRPC())
        self.imu_service.listen(msgpackrpc.Address("localhost", 18802))
        self.imu_service_thread = threading.Thread(target=self.imu_service.start)


    def start(self):
        self.gui_thread.start()
        self.camera_service_thread.start()
        self.gps_service_thread.start()
        self.imu_service_thread.start()

    def gui_render_flow(self):
        self.render = GuiRender()
        self.camera_rpc.set_put_render_callback(put_render_callback=self.render.put_render_queue)
        self.render.set_caption('camera service')
        while True:
            metadata, sensor_data = self.render.get_render_queue()
            self.render.draw_image(height = metadata[b'height'],
                                   width = metadata[b'width'],
                                   image = sensor_data)
            self.render.flip_display()

def main():
    server = SensorServer()
    server.start()
    try:
        while True:
            pass

    except KeyboardInterrupt:
        print('\n Services Cancelled by user. Bye!')


if __name__ == '__main__':
    main()
