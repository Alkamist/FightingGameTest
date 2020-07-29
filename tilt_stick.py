import time

from state import State


def sign(value):
    if value >= 0.0:
        return 1.0
    else:
        return -1.0

def bipolar_max(value, magnitude):
    if value > 0.0:
        return max(value, magnitude)
    elif value < 0.0:
        return min(value, -magnitude)
    else:
        return 0.0


class AxisTiltTracker(object):
    def __init__(self, minimum_active_value=0.2875):
        self.minimum_active_value = minimum_active_value
        self.is_tilting = False
        self.just_activated = False
        self.just_crossed_center = False

        self._input_value = 0.0
        self._input_previous_value = 0.0
        self._tilt_time = 0.0

    def update(self, input_value, reset_tilt=False, tilt_modifier=False, hold_tilt=False):
        self._input_previous_value = self._input_value
        self._input_value = input_value

        input_value_is_active = abs(self._input_value) >= self.minimum_active_value
        input_previous_value_is_active = abs(self._input_previous_value) >= self.minimum_active_value

        self.just_activated = input_value_is_active and not input_previous_value_is_active
        self.just_crossed_center = input_value_is_active and input_previous_value_is_active \
                               and sign(self._input_value) != sign(self._input_previous_value)

        if tilt_modifier and (self.just_activated or self.just_crossed_center or reset_tilt):
            self.is_tilting = True
            self._tilt_time = time.perf_counter()

        if (not hold_tilt) and time.perf_counter() - self._tilt_time > 0.117:
            self.is_tilting = False


class TiltStick(object):
    def __init__(self, tilt_level=0.65, minimum_active_value=0.2875, tilt_on_activation=False):
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0
        self.tilt_level = tilt_level
        self.minimum_active_value = minimum_active_value
        self.tilt_on_activation = tilt_on_activation

        self._tilt_state = State()
        self._x_axis = AxisTiltTracker(self.minimum_active_value)
        self._y_axis = AxisTiltTracker(self.minimum_active_value)

    def update(self, tilt_modifier, hold_tilt, ls_x, ls_y):
        self.x_axis_output = ls_x
        self.y_axis_output = ls_y

        self._tilt_state.is_active = tilt_modifier
        self._tilt_state.update()

        reset_tilt = (self.tilt_on_activation and self._tilt_state.just_activated) or self._tilt_state.just_deactivated


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
