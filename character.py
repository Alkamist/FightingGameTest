def sign(value):
    if value >= 0.0:
        return 1.0
    else:
        return -1.0


def apply_friction(velocity, friction):
    return velocity - sign(velocity) * min(abs(velocity), friction)


class Character(object):
    def __init__(self, controller):
        self.controller = controller

        self.run_speed = 2.2
        self.walk_speed = 1.6
        self.traction = 0.08
        self.air_friction = 0.02
        self.jump_squat_frames = 3
        self.short_hop_speed = 2.1
        self.full_hop_speed = 3.68
        self.gravity = 0.23

        self.x = 0.0
        self.y = 0.0
        self.x_velocity = 0.0
        self.y_velocity = 0.0

        self.state = "idle"
        self.previous_state = "idle"
        self.state_frame = 0

    def update(self):
        # Apply gravity.
        #self.y_velocity -= self.gravity

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
            self.state = "idle"
#            if self.state_frame > self.jump_squat_frames:
#                self.state = "airborne"

    def process_state(self):
        controller = self.controller

        if self.state == "idle":
            self.x_velocity = apply_friction(self.x_velocity, self.traction)

        elif self.state == "walk":
            self.x_velocity = controller.x_axis.value * self.walk_speed

        elif self.state == "run":
            self.x_velocity = controller.x_axis.value * self.run_speed

#        elif self.state == "jump_squat":
#            self.x_velocity *= self.traction
#
#        elif self.state == "airborne":
#            if self.previous_state == "jump_squat":
#                self.y_velocity = self.full_hop_speed
#
#            self.x_velocity *= self.air_friction