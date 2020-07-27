from copy import copy

import pygame


class Sprite(object):
    def __init__(self, file_name):
        self.position = [0.0, 0.0]
        self.previous_position = [0.0, 0.0]
        self.image = pygame.image.load(file_name)
        self.image_rect = self.image.get_rect()

    def update_position(self, new_position):
        self.previous_position = copy(self.position)
        self.position = copy(new_position)

    def render(self, display, physics_fraction):
        self.image_rect.x = int(self._interpolate_coordinate(0, physics_fraction))
        self.image_rect.y = -int(self._interpolate_coordinate(1, physics_fraction))
        display.blit(self.image, self.image_rect)

    def _interpolate_coordinate(self, index, physics_fraction):
        return self.previous_position[index] + physics_fraction * (self.position[index] - self.previous_position[index])
