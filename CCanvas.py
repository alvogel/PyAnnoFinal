import pygame
from functions import *
import numpy as np

class CCanvas:

    def __init__(self,x ,y ,width, height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.points = []
        self.surface.fill((0, 0, 0, 255))


    def Clear(self):
        self.surface.fill((0, 0, 0, 0))
        self.points = []


    def Draw(self, x, y):

        self.points.append((x,y))

    def endDraw(self):

        if len(self.points) > 1:
            pygame.draw.lines(self.surface, (255,255,255), False, self.points, 10)

        self.points = list()

    def render(self, width, height, crop=False):

        if len(self.points) > 1:
            pygame.draw.lines(self.surface, (255, 255, 255), False, self.points, 10)

        #pygame.draw.lines(self.surface, (255, 0, 0), True, [(0,0),(self.width,0),(self.width,self.height),(0,self.height)], 5)

        if crop:

            box = find_bounding_box(self.surface)
            image_width = width
            image_height = height

            if image_height != 0 and image_width != 0:

                ratio = image_width / image_height

                if ratio >= 1:
                    new_width = width / image_width * image_width
                    new_height =  width / image_width * image_height
                else:
                    new_width = height / image_height * image_width
                    new_height =  height / image_height * image_height
            else:
                new_width = image_width
                new_height = image_height

            scaled = pygame.transform.scale(self.surface.subsurface(box),(int(new_width),int(new_height)))
        else:
            scaled = self.surface

        return scaled

    def set_surface(self, s):
        self.surface = s.copy()

    def getPixelArray(self):

        thumb = self.render(20, 20, True)

        vector = []

        array = pygame.surfarray.array3d(thumb)

        for x in range(thumb.get_width()):
            for y in range(thumb.get_height()):
                vector.append(array[x][y][0])

        shaped = np.array([vector])

        return shaped

