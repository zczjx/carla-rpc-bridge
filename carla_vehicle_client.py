#!/usr/bin/env python3

import os
import sys
import carla
import random
from vehicle_proxy import *

try:
    import pygame
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

try:
    import queue
except ImportError:
    import Queue as queue

def draw_image(surface, image, blend=False):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    if blend:
        image_surface.set_alpha(100)
    surface.blit(image_surface, (0, 0))

def get_font():
    fonts = [x for x in pygame.font.get_fonts()]
    default_font = 'ubuntumono'
    font = default_font if default_font in fonts else fonts[0]
    font = pygame.font.match_font(font)
    return pygame.font.Font(font, 14)

def main():
    pygame.init()

    display = pygame.display.set_mode(
        (800, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    display2 = pygame.display.set_mode(
        (800, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    font = get_font()
    clock = pygame.time.Clock()

    client = carla.Client('localhost', 2000)
    client.set_timeout(30.0)
    world = client.get_world()
    vehicle_client = VehicleProxy(rig=None, world=world)

    vehicle_client.start()
    while True:
        clock.tick()
        vehicle_client.tick_update()
        # image_rgb = vehicle_client.get_render_image(timeout=2.0)

        # Draw the display.
        # draw_image(display, image_rgb)
        display.blit(font.render('% 5d FPS (real)' % clock.get_fps(), True, (255, 255, 255)), (8, 10))
        pygame.display.flip()

    vehicle_client.stop()
    pygame.quit()
    print('done.')

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')