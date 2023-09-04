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
        self.map = world.get_map()
        self.start_pose = random.choice(self.map.get_spawn_points())
        self.waypoint = self.map.get_waypoint(self.start_pose.location)
        self.blueprint_library = world.get_blueprint_library()
        self.vehicle = world.spawn_actor(self.blueprint_library.find('vehicle.tesla.model3'), self.start_pose)
        self.actor_list.append(self.vehicle)
        self.vehicle.set_simulate_physics(False)
        self.image_render_queue = queue.Queue()
        self.view_camera = world.spawn_actor(
            self.blueprint_library.find('sensor.camera.rgb'),
            carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)),
            attach_to=self.vehicle)
        self.view_camera.listen(lambda data: self.camera_dispatch(data, "view_camera"))
        self.actor_list.append(self.view_camera)
        self.simulate_frame = None
        self.client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))

    def start(self):
        self.vehicle.set_autopilot(True)

    def stop(self):
        print('destroying actors.')
        self.vehicle.set_autopilot(False)
        for actor in self.actor_list:
            actor.destroy()
    def __del__(self):
        self.stop()

    def camera_dispatch(self, sensor_data, sensor_id):
        metadata = {'name': sensor_id, 'type': 'camera'}
        metadata['fov'] = sensor_data.fov
        metadata['height'] = sensor_data.height
        metadata['width'] = sensor_data.width
        array = np.frombuffer(sensor_data.raw_data, dtype=np.dtype("uint8"))
        self.sensor_dispatch(sensor_data=array.tolist(), metadata=metadata)

    def sensor_dispatch(self, sensor_data, metadata):
        self.client.call('push_sensor_data', metadata, sensor_data)

    def tick_update(self):
        # self.waypoint = random.choice(self.waypoint.next(1.5))
        # self.vehicle.set_transform(self.waypoint.transform)
        self.simulate_frame = self.world.tick()

    def get_render_image(self, timeout):
        data = self.image_render_queue.get(timeout=timeout)
        return data