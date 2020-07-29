import pygame

from state import State
from button_axis import ButtonAxis


KEY_BINDS = {
    "left" : pygame.K_a,
    "right" : pygame.K_d,
    "down" : pygame.K_s,
    "up" : pygame.K_w,
    "tilt" : pygame.K_CAPSLOCK,
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
            action.update(pressed_keys[action_key])


class DigitalStick(object):
    def __init__(self, tilt_level=0.6500):
        self._x_button_axis = ButtonAxis()
        self._y_button_axis = ButtonAxis()
        self.tilt_level = tilt_level

        self._tilt_modifier = State()

    def update(self, tilt_modifier):
        self._tilt_modifier.update(tilt_modifier)

        reset_tilt = self._tilt_modifier.just_deactivated

        self.x_axis
        self._x_axis.update(ls_x, reset_tilt, tilt_modifier, hold_tilt)

        abs_ls_x = abs(ls_x)
        if self._x_axis.is_tilting and abs_ls_x > self.tilt_level:
            scale_factor = self.tilt_level / abs_ls_x
            self.x_axis_output = sign(ls_x) * self.tilt_level
            self.y_axis_output = bipolar_max(ls_y * scale_factor, self.minimum_active_value)


        self._y_axis.update(self.y_axis_output, reset_tilt, tilt_modifier, hold_tilt)

        abs_ls_y = abs(self.y_axis_output)
        if self._y_axis.is_tilting and abs_ls_y > self.tilt_level:
            scale_factor = self.tilt_level / abs_ls_y
            self.x_axis_output = bipolar_max(self.x_axis_output * scale_factor, self.minimum_active_value)
            self.y_axis_output = sign(ls_y) * self.tilt_level


class DigitalController(object):
    def __init__(self):
        self.key_binds = KeyBinds()
        self.actions = self.key_binds.actions
        self.x_axis = ButtonAxis()
        self.y_axis = ButtonAxis()
        self.tilt = self.actions["tilt"]
        self.jump = self.actions["jump"]
        self.attack = self.actions["attack"]

    def update(self):
        self.key_binds.update()
        self.x_axis.update(self.actions["left"].is_active, self.actions["right"].is_active)
        self.y_axis.update(self.actions["down"].is_active, self.actions["up"].is_active)
