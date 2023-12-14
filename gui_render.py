import os
import sys
import random
import numpy as np

try:
    import pygame
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import queue
except ImportError:
    import Queue as queue

class GuiRender(object):
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.font = self.__get_front()
        self.clock = pygame.time.Clock()
        self.render_queue = queue.Queue()

    def __get_front(self):
        fonts = [x for x in pygame.font.get_fonts()]
        default_font = 'ubuntumono'
        font = default_font if default_font in fonts else fonts[0]
        font = pygame.font.match_font(font)
        return pygame.font.Font(font, 14)

    def set_caption(self, title='GuiRender'):
        pygame.display.set_caption(title)

    def put_render_queue(self, image):
        self.render_queue.put(image)

    def get_render_queue(self):
        self.clock.tick()
        return self.render_queue.get()

    def draw_image(self, height, width, image=[]):
        array = np.array(image, dtype=np.dtype("uint8"))
        array = np.reshape(array, (height, width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        self.display.blit(image_surface, (0, 0))

    def flip_display(self):
        self.display.blit(self.font.render('% 5d FPS (real)' % self.clock.get_fps(), True, (255, 255, 255)), (8, 10))
        pygame.display.flip()

    def __del__(self):
        pygame.quit()
        print('Bye pygame.quit!')