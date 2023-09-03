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
        self.render = GuiRender()
        self.gui_thread = threading.Thread(target=self.gui_render_flow)
        self.gui_thread.start()

    def gui_render_flow(self):
        while True:
            metadata, sensor_data = self.render.get_render_queue()
            print(metadata)

    def push_sensor_data(self, metadata, sensor_data):
        self.render.put_render_queue(image=(metadata, sensor_data))

def main():
    server = msgpackrpc.Server(VehicleServer())
    server.listen(msgpackrpc.Address("localhost", 18800))
    server.start()

if __name__ == '__main__':
    main()
