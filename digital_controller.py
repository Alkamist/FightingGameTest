import pygame

from state import State
from button_axis import ButtonAxis


KEY_BINDS = {
    "left" : pygame.K_a,
    "right" : pygame.K_d,
    "down" : pygame.K_s,
    "up" : pygame.K_w,
    "tilt" : pygame.K_LSHIFT,
    "jump" : pygame.K_LEFTBRACKET,
    "attack" : pygame.K_SEMICOLON,
}


class KeyBinds(object):
    def __init__(self):
        self.key_binds = KEY_BINDS
        self.actions = {}
        for action_name in KEY_BINDS:
            self.actions[action_name] = State()

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        for action_name, action in self.actions.items():
            action_key = KEY_BINDS[action_name]
            action.update(bool(pressed_keys[action_key]))


class DigitalController(object):
    def __init__(self):
        self.key_binds = KeyBinds()
        self.actions = self.key_binds.actions
        self.x_axis = ButtonAxis()
        self.y_axis = ButtonAxis()

        for action_name in KEY_BINDS:
            setattr(self, action_name, self.key_binds.actions[action_name])

    def update(self):
        self.key_binds.update()
        self.x_axis.update(self.left.is_active, self.right.is_active)
        self.y_axis.update(self.down.is_active, self.up.is_active)
