def sign(value):
    if value >= 0.0:
        return 1.0
    else:
        return -1.0


def apply_friction(velocity, friction):
    return velocity - sign(velocity) * min(abs(velocity), friction)


def apply_acceleration(velocity, axis_value, base_acceleration, axis_acceleration, max_velocity):
    base = sign(axis_value) * base_acceleration
    axis_addition = axis_value * axis_acceleration
    additional_velocity = base + axis_addition

    if axis_value > 0.0:
        additional_velocity = min(additional_velocity, max_velocity - velocity)
        additional_velocity = max(0.0, additional_velocity)
    elif axis_value < 0.0:
        additional_velocity = max(additional_velocity, -max_velocity - velocity)
        additional_velocity = min(0.0, additional_velocity)
    else:
        additional_velocity = 0.0

    return velocity + additional_velocity


class Character(object):
    def __init__(self, controller):
        self.controller = controller

        self.width = 8.0
        self.height = 16.0

        self.run_velocity = 2.2
        self.walk_velocity = 1.6
        self.ground_friction = 0.08
        self.air_friction = 0.02
        self.air_base_acceleration = 0.02
        self.air_additional_acceleration = 0.06
        self.air_max_velocity = 0.83
        self.jump_squat_frames = 3
        self.short_hop_velocity = 2.1
        self.full_hop_velocity = 3.68
        self.fall_velocity = 2.8
        self.fast_fall_velocity = 3.4
        self.gravity = 0.23

        self.x = 0.0
        self.y = 0.0
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.state = "airborne"
        self.previous_state = "airborne"
        self.state_frame = 0

    def land(self):
        self.y_velocity = 0.0
        self.state = "idle"
        self.update()

    def update(self):
        self.previous_state = self.state
        self.decide_state()
        if self.state != self.previous_state:
            self.state_frame = 0
        self.process_state()

        # Move based on velocity.
        self.x += self.x_velocity
        self.y += self.y_velocity

        self.state_frame += 1

    def decide_state(self):
        controller = self.controller

        if self.state == "idle":
            if controller.jump.just_activated:
                self.state = "jump_squat"
            elif controller.x_axis.just_activated and not controller.tilt.is_active:
                self.state = "run"
            elif controller.x_axis.is_active:
                self.state = "walk"

        elif self.state == "walk":
            if controller.jump.just_activated:
                self.state = "jump_squat"
            elif (controller.x_axis.just_activated or controller.x_axis.just_crossed_center) and not controller.tilt.is_active:
                self.state = "run"
            else:
                self.state = "idle"

        elif self.state == "run":
            if controller.jump.just_activated:
                self.state = "jump_squat"
            elif controller.x_axis.just_crossed_center and controller.tilt.is_active:
                self.state = "walk"
            elif not controller.x_axis.is_active:
                self.state = "idle"

        elif self.state == "jump_squat":
            if self.state_frame > self.jump_squat_frames:
                self.state = "airborne"

    def process_state(self):
        controller = self.controller

        if self.state == "idle":
            self.x_velocity = apply_friction(self.x_velocity, self.ground_friction)

        elif self.state == "walk":
            self.x_velocity = controller.x_axis.value * self.walk_velocity

        elif self.state == "run":
            self.x_velocity = controller.x_axis.value * self.run_velocity

        elif self.state == "jump_squat":
            self.x_velocity = apply_friction(self.x_velocity, self.ground_friction)

        elif self.state == "airborne":
            if self.previous_state == "jump_squat":
                self.y_velocity = self.full_hop_velocity

            if controller.x_axis.is_active:
                self.x_velocity = apply_acceleration(
                    self.x_velocity,
                    controller.x_axis.value,
                    self.air_base_acceleration,
                    self.air_additional_acceleration,
                    self.air_max_velocity,
                )
            else:
                self.x_velocity = apply_friction(self.x_velocity, self.air_friction)

            self.y_velocity -= self.gravity
            self.y_velocity = max(self.y_velocity, -self.fall_velocity)
