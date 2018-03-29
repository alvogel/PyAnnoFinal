from functions import *
import pygame

class CTrainingItem:

    def __init__(self, surface, digit):
        self.surface = surface

    def getImage(self, width, height, crop=False):
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