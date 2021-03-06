def sign(value):
    if value >= 0.0:
        return 1.0
    else:
        return -1.0


def apply_friction(velocity, friction):
    return velocity - sign(velocity) * min(abs(velocity), friction)


def apply_acceleration(velocity, axis_value, base_acceleration, axis_acceleration, max_velocity, friction):
    base_velocity = velocity
    if abs(base_velocity) > max_velocity:
        base_velocity = apply_friction(base_velocity, friction)

    base = sign(axis_value) * base_acceleration
    axis_addition = axis_value * axis_acceleration
    additional_velocity = base + axis_addition

    if axis_value > 0.0:
        additional_velocity = min(additional_velocity, max_velocity - base_velocity)
        additional_velocity = max(0.0, additional_velocity)
    elif axis_value < 0.0:
        additional_velocity = max(additional_velocity, -max_velocity - base_velocity)
        additional_velocity = min(0.0, additional_velocity)
    else:
        additional_velocity = 0.0

    return base_velocity + additional_velocity


class Character(object):
    def __init__(self, controller):
        self.controller = controller

        self.width = 8.0
        self.height = 16.0

        self.ground_friction = 0.08
        self.dash_start_velocity = 1.9
        self.dash_max_velocity = 2.2
        self.dash_base_acceleration = 0.02
        self.dash_axis_acceleration = 0.1

        self.walk_start_velocity = 0.16
        self.walk_max_velocity = 1.6
        self.walk_base_acceleration = 0.2
        self.walk_axis_acceleration = 0.0

        self.air_friction = 0.02
        self.air_base_acceleration = 0.02
        self.air_axis_acceleration = 0.06
        self.air_max_velocity = 0.83

        self.jump_squat_frames = 3
        self.jump_velocity_dampening = 0.83
        self.jump_max_horizontal_velocity = 1.7
        self.jump_start_horizontal_velocity = 0.72
        self.short_hop_velocity = 2.1
        self.full_hop_velocity = 3.68
        self.fall_velocity = 2.8
        self.fast_fall_velocity = 3.4
        self.extra_jump_velocity_multiplier = 1.2
        self.extra_jump_horizontal_axis_multiplier = 0.9
        self.extra_jumps = 1
        self.gravity = 0.23

        self.x = 0.0
        self.y = 0.0
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.state = "airborne"
        self.previous_state = "airborne"
        self.state_frame = 0
        self.extra_jumps_left = self.extra_jumps
        self.is_facing_right = True

        self._should_full_hop = False

    def land(self):
        self.y_velocity = 0.0
        self.state = "idle"
        self.extra_jumps_left = self.extra_jumps
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

        should_jump = controller.jump.just_activated or controller.short_hop.just_activated or controller.full_hop.just_activated

        if self.state == "idle":
            if should_jump:
                self.state = "jump_squat"
            elif controller.x_axis.just_activated and not controller.tilt.is_active:
                self.state = "dash"
            elif controller.x_axis.is_active:
                self.state = "walk"

        elif self.state == "walk":
            if should_jump:
                self.state = "jump_squat"
            elif (controller.x_axis.just_activated or controller.x_axis.just_crossed_center) and not controller.tilt.is_active:
                self.state = "dash"
            else:
                self.state = "idle"

        elif self.state == "dash":
            if should_jump:
                self.state = "jump_squat"
            elif controller.x_axis.just_crossed_center and controller.tilt.is_active:
                self.state = "walk"
            elif not controller.x_axis.is_active:
                self.state = "idle"

        elif self.state == "jump_squat":
            if controller.full_hop.is_active:
                self._should_full_hop = True

            if self.state_frame >= self.jump_squat_frames:
                self.state = "airborne"

    def process_state(self):
        controller = self.controller

        if self.state == "idle":
            self.x_velocity = apply_friction(self.x_velocity, self.ground_friction)

        elif self.state == "walk":
            if controller.x_axis.value < 0.0:
                self.is_facing_right = False
            else:
                self.is_facing_right = True
            self._handle_walk_movement()

        elif self.state == "dash":
            if controller.x_axis.value < 0.0:
                self.is_facing_right = False
            else:
                self.is_facing_right = True
            self._handle_dash_movement()

        elif self.state == "jump_squat":
            self.x_velocity = apply_friction(self.x_velocity, self.ground_friction)

        elif self.state == "airborne":
            self._handle_grounded_jump()
            self._handle_extra_jumps()
            self._handle_horizontal_air_movement()
            self._handle_fast_fall()
            self._handle_gravity()

    def _handle_walk_movement(self):
        controller = self.controller

        if abs(self.x_velocity) < self.walk_start_velocity:
            self.x_velocity = sign(controller.x_axis.value) * self.walk_start_velocity

        self.x_velocity = apply_acceleration(
            self.x_velocity,
            controller.x_axis.value,
            self.walk_base_acceleration,
            self.walk_axis_acceleration,
            self.walk_max_velocity,
            self.ground_friction,
        )

    def _handle_dash_movement(self):
        controller = self.controller

        if abs(self.x_velocity) < self.dash_start_velocity:
            self.x_velocity = sign(controller.x_axis.value) * self.dash_start_velocity

        self.x_velocity = apply_acceleration(
            self.x_velocity,
            controller.x_axis.value,
            self.dash_base_acceleration,
            self.dash_axis_acceleration,
            self.dash_max_velocity,
            self.ground_friction,
        )

    def _handle_horizontal_air_movement(self):
        controller = self.controller
        if controller.x_axis.is_active:
            self.x_velocity = apply_acceleration(
                self.x_velocity,
                controller.x_axis.value,
                self.air_base_acceleration,
                self.air_axis_acceleration,
                self.air_max_velocity,
                self.air_friction,
            )
        else:
            self.x_velocity = apply_friction(self.x_velocity, self.air_friction)

    def _handle_fast_fall(self):
        controller = self.controller
        if self.y_velocity <= 0.0 and controller.y_axis.value < -0.6 and controller.y_axis.active_frames < 4:
            self.y_velocity = -self.fast_fall_velocity

    def _handle_grounded_jump(self):
        controller = self.controller
        if self.previous_state == "jump_squat":
            # Handle changing horizontal velocity when jumping off of the ground based on stick x axis.
            self.x_velocity = (self.x_velocity * self.jump_velocity_dampening) + (controller.x_axis.value * self.jump_start_horizontal_velocity)
            if (abs(self.x_velocity) > self.jump_max_horizontal_velocity):
                self.x_velocity = sign(self.x_velocity) * self.jump_max_horizontal_velocity

            #Handle short hopping and full hopping.
            if controller.jump.is_active or self._should_full_hop:
                self.y_velocity = self.full_hop_velocity
                self._should_full_hop = False
            else:
                self.y_velocity = self.short_hop_velocity

    def _handle_extra_jumps(self):
        controller = self.controller
        should_jump = controller.jump.just_activated or controller.short_hop.just_activated or controller.full_hop.just_activated
        if should_jump and self.extra_jumps_left > 0:
            self.x_velocity = controller.x_axis.value * self.extra_jump_horizontal_axis_multiplier
            self.y_velocity = self.full_hop_velocity * self.extra_jump_velocity_multiplier
            self.extra_jumps_left -= 1

    def _handle_gravity(self):
        self.y_velocity -= min(self.gravity, self.fall_velocity + self.y_velocity)
