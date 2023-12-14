#!/usr/bin/env python3

import os
import sys
import carla
import random
from vehicle_proxy import *
try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

try:
    import queue
except ImportError:
    import Queue as queue

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(30.0)
    world = client.get_world()
    vehicle_client = VehicleProxy(rig=None, world=world)

    vehicle_client.start()
    try:
        while True:
            vehicle_client.tick_update()

    except KeyboardInterrupt:
        print('vehicle_client done.')


if __name__ == '__main__':
        main()
