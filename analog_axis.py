class AnalogAxis(object):
    def __init__(self, dead_zone=0.2875):
        self.value = 0.0
        self.previous_value = 0.0
        self.magnitude = 0.0
        self.previous_magnitude = 0.0
        self.dead_zone = dead_zone

        self.is_active = False
        self.was_active = False
        self.just_activated = False
        self.just_deactivated = False
        self.just_crossed_center = False

        self.active_frames = 0

    def update(self, value):
        self.previous_value = self.value
        self.previous_magnitude = self.magnitude
        self.value = value
        self.magnitude = abs(self.value)

        self.was_active = self.is_active
        self.is_active = self.magnitude >= self.dead_zone
        self.just_activated = self.is_active and not self.was_active
        self.just_deactivated = self.was_active and not self.is_active
        self.just_crossed_center = self.value < 0.0 and self.previous_value >= 0.0 \
                                or self.value > 0.0 and self.previous_value <= 0.0

        if self.just_deactivated or self.just_crossed_center:
            self.active_frames = 0
        else:
            self.active_frames += 1
