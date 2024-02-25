import carla
from carla import ColorConverter as cc
import argparse
import collections
import datetime
import logging
import math
import random
import numpy as np
import sys
from multiprocessing import Queue
import socket
import cv2
import time
import pickle
import struct

def sensor_callback(sensor_data, conn):
    sensor_data.convert(cc.Raw)
    array = np.frombuffer(sensor_data.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (sensor_data.height, sensor_data.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]

    array_bytes = pickle.dumps(array)
    array_length = struct.pack('!I', len(array_bytes))
    conn.sendall(array_length+array_bytes)

def main():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the host and the port
        host = 'localhost'
        port = 35650

        # Bind to the port
        s.bind((host, port))

        # Listen for a connection
        s.listen(1)

        print("Server started. Waiting for connections...")

        # Accept a connection
        conn, addr = s.accept()

        print(f"Connected by {addr}")

        client = carla.Client('localhost',2000)
        client.set_timeout(2000.0)
        sim_world = client.get_world()

        vehicle_blueprints = sim_world.get_blueprint_library().filter('*vehicle*')

        transform = random.choice(sim_world.get_map().get_spawn_points())
        ego_vehicle = sim_world.spawn_actor(random.choice(vehicle_blueprints), transform)

        camera_init_trans = carla.Transform(carla.Location(z=3.5))
        camera_bp = sim_world.get_blueprint_library().find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', str(408))
        camera_bp.set_attribute('image_size_y', str(361))
        camera = sim_world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)

        camera.listen(lambda image: sensor_callback(image, conn))

        ego_vehicle.set_autopilot(True)

        while True:
            sim_world.wait_for_tick()
            spectator = sim_world.get_spectator()
            transform = ego_vehicle.get_transform()
            spectator.set_transform(carla.Transform(transform.location + carla.Location(x=-20,y=0,z=8),
                                                    carla.Rotation(pitch=0,yaw=0,roll=0)))

    finally:
        camera.destroy()
        ego_vehicle.destroy()
        conn.close()

if __name__ == "__main__":
    main()
