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

# sensor_queue = Queue()

try:

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the host and the port
    host = '192.168.1.6'
    port = 23149

    # Bind to the port
    s.bind((host, port))

    # Listen for a connection
    s.listen(1)

    print("Server lidar started. Waiting for connections...")

    # Accept a connection
    conn, addr = s.accept()

    print(f"Connected by {addr}")


    client = carla.Client('localhost',2000)
    client.set_timeout(2000.0)
    sim_world = client.get_world()

    # settings = sim_world.get_settings()
    # settings.synchronous_mode = True
    # settings.fixed_delta_seconds = 0.05
    # sim_world.apply_settings(settings)

    vehicle_blueprints = sim_world.get_blueprint_library().filter('*vehicle*')
    
    
    # get a random valid occupation in the world
    transform = random.choice(sim_world.get_map().get_spawn_points())
    # spawn the vehilce
    ego_vehicle = sim_world.spawn_actor(random.choice(vehicle_blueprints), transform)


    window_size = (361, 408)

    lidar_range = 50
    lidar_bp_trans = carla.Transform(carla.Location(z=3.5))
    lidar_bp = sim_world.get_blueprint_library().find('sensor.lidar.ray_cast')
    lidar = sim_world.spawn_actor(lidar_bp,lidar_bp_trans,attach_to=ego_vehicle)
    def lidar_callback(image):
        points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0]/4), 4))
        lidar_data = np.array(points[:,:2])
        lidar_data *= min(window_size)/(2.0*(lidar_range))
        lidar_data += (0.5 * window_size[0], 0.5 * window_size[1])
        lidar_data = np.fabs(lidar_data)
        lidar_data = lidar_data.astype(np.int32)
        lidar_data = np.reshape(lidar_data,(-1,2))
        lidar_img_size = (window_size[0], window_size[1], 3)
        lidar_img = np.zeros((lidar_img_size), dtype=np.uint8)
        lidar_img[tuple(lidar_data.T)] = (255,255,255)

        array_bytes_1 = pickle.dumps(lidar_img)
        array_length_1 = struct.pack('!I', len(array_bytes_1))
        conn.sendall(array_length_1+array_bytes_1)
        
    lidar.listen(lambda image: lidar_callback(image))
    
    # set the vehicle autopilot mode
    ego_vehicle.set_autopilot(True)


    while True:
        sim_world.wait_for_tick()
        spectator = sim_world.get_spectator()
        transform = ego_vehicle.get_transform()
        spectator.set_transform(carla.Transform(transform.location + carla.Location(x=-20,y=0,z=8),
                                                carla.Rotation(pitch=0,yaw=0,roll=0)))
        # s_frame = sensor_queue.get(True,2.0)
        # print(s_frame[0])


finally:
    lidar.destroy()
    ego_vehicle.destroy()
    conn.close()

