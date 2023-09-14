#!/usr/bin/env python3

import msgpackrpc
import os
import sys
import carla
import random
import numpy as np

try:
    import queue
except ImportError:
    import Queue as queue

class VehicleProxy(object):
    def __init__(self, world, rig=None):
        self.world = world
        self.actor_list = []
        self.sensor_list = []
        self.init_vehicle(world=world)
        self.init_camera_client(world=world)
        self.init_gps_client(world=world)
        self.init_imu_client(world=world)

    def __del__(self):
        print('closing clients.')
        self.camera_client.close()
        self.gps_client.close()
        self.imu_client.close()
        self.vehicle.set_autopilot(False)
        for actor in self.actor_list:
            actor.destroy()

    def init_vehicle(self, world):
        self.map = world.get_map()
        self.start_pose = random.choice(self.map.get_spawn_points())
        self.waypoint = self.map.get_waypoint(self.start_pose.location)
        self.blueprint_library = world.get_blueprint_library()
        self.vehicle = world.spawn_actor(self.blueprint_library.find('vehicle.tesla.model3'), self.start_pose)
        self.actor_list.append(self.vehicle)
        self.vehicle.set_simulate_physics(False)
        self.simulate_frame = None

    def init_camera_client(self, world):
        self.camera_client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
        self.view_camera = world.spawn_actor(
            self.blueprint_library.find('sensor.camera.rgb'),
            carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)),
            attach_to=self.vehicle)
        self.view_camera.listen(lambda data: self.camera_dispatch(data, "view_camera"))
        self.actor_list.append(self.view_camera)

    def init_gps_client(self, world):
        self.gps_client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18801))
        self.gps = world.spawn_actor(
        self.blueprint_library.find('sensor.other.gnss'),
            carla.Transform(carla.Location(x=1.0, z=2.8)),
            attach_to=self.vehicle)
        self.gps.listen(lambda data: self.gps_dispatch(data, "gps"))
        self.actor_list.append(self.gps)

    def init_imu_client(self, world):
        self.imu_client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18802))
        self.imu = world.spawn_actor(
        self.blueprint_library.find('sensor.other.imu'),
            carla.Transform(carla.Location(x=1.0, z=2.8)),
            attach_to=self.vehicle)
        self.imu.listen(lambda data: self.imu_dispatch(data, "imu"))
        self.actor_list.append(self.imu)

    def start(self):
        self.vehicle.set_autopilot(True)

    def camera_dispatch(self, sensor_data, sensor_id):
        metadata = {'name': sensor_id, 'type': 'camera'}
        metadata['fov'] = sensor_data.fov
        metadata['height'] = sensor_data.height
        metadata['width'] = sensor_data.width
        array = np.frombuffer(sensor_data.raw_data, dtype=np.dtype("uint8"))
        self.camera_client.call('push_camera_data', metadata, array.tolist())

    def gps_dispatch(self, sensor_data, sensor_id):
        metadata = {'name': sensor_id, 'type': 'gps'}
        gps_data = {
                    'altitude': sensor_data.altitude,
                    'latitude': sensor_data.latitude,
                    'longitude': sensor_data.longitude,
                   }
        self.gps_client.call('push_gps_data', metadata, gps_data)

    def imu_dispatch(self, sensor_data, sensor_id):
        metadata = {'name': sensor_id, 'type': 'imu'}
        imu_data = {
                    'accelerometer':
                        {
                        'x': sensor_data.accelerometer.x,
                        'y': sensor_data.accelerometer.y,
                        'z': sensor_data.accelerometer.z,
                        },
                    'compass': sensor_data.compass,
                    'gyroscope':
                        {
                        'x': sensor_data.gyroscope.x,
                        'y': sensor_data.gyroscope.y,
                        'z': sensor_data.gyroscope.z,
                        },
                   }

        self.imu_client.call('push_imu_data', metadata, imu_data)

    def sensor_dispatch(self, sensor_data, metadata):
        # self.client.call('push_sensor_data', metadata, sensor_data)
        pass

    def tick_update(self):
        # self.waypoint = random.choice(self.waypoint.next(1.5))
        # self.vehicle.set_transform(self.waypoint.transform)
        self.simulate_frame = self.world.tick()