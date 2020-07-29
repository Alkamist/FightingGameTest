from state import State
from analog_axis import AnalogAxis


class ButtonAxis(AnalogAxis):
    def __init__(self):
        super().__init__()
        self._low_was_first = False
        self._low_state = State()
        self._high_state = State()
        self._pending_value = 0.0

    def update(self, low, high):
        self._low_state.update(low)
        self._high_state.update(high)

        if self._low_state.just_activated or (self._low_state.is_active and not self._high_state.is_active):
            self._pending_value = -1.0

        elif self._high_state.just_activated or (self._high_state.is_active and not self._low_state.is_active):
            self._pending_value = 1.0

        elif not self._low_state.is_active and not self._high_state.is_active:
            self._pending_value = 0.0

        super().update(self._pending_value)
