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

    def push_sensor_data(self, metadata, sensor_data):
        if(self.render != None):
            self.render.put_render_queue(image=(metadata, sensor_data))

def main():
    server = msgpackrpc.Server(VehicleServer())
    server.listen(msgpackrpc.Address("localhost", 18800))
    server.start()

if __name__ == '__main__':
    main()
