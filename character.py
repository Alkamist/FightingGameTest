class Character(object):
    def __init__(self, position, velocity, gravity):
        self.run_speed = 10.0
        self.walk_speed = 3.0
        self.ground_friction = 0.6

        self.position = position
        self.velocity = velocity
        self.gravity = gravity
        self.state = "idle"

    def update(self, controller):
        # Apply gravity.
        #self.velocity[0] += self.gravity[0]
        #self.velocity[1] += self.gravity[1]

        x_axis_just_smashed = controller.x_axis.magnitude >= 0.8000 and controller.x_axis.active_frames < 3
        #y_axis_just_smashed = controller.y_axis.magnitude >= 0.6625 and controller.x_axis.active_frames < 3

        if self.state == "idle":
            if x_axis_just_smashed and not controller.tilt.is_active:
                self.state = "run"
            #elif controller.jump.just_activated:
            #    self.state = "jump_squat"
            elif controller.x_axis.is_active:
                self.state = "walk"
            else:
                self.velocity[0] *= self.ground_friction

        elif self.state == "walk":
            if x_axis_just_smashed and not controller.tilt.is_active:
                self.state = "run"
            elif controller.x_axis.is_active:
                self.velocity[0] = controller.x_axis.value * self.walk_speed
            else:
                self.state = "idle"

        elif self.state == "run":
            if controller.x_axis.is_active:
                if controller.x_axis.magnitude >= 0.8000:
                    if controller.tilt.is_active and controller.x_axis.just_crossed_center:
                        self.state = "walk"
                    else:
                        self.velocity[0] = controller.x_axis.value * self.run_speed
                else:
                    self.state = "walk"
            else:
                self.state = "idle"

#        elif self.state == "jump_squat":
#            self.velocity[0] *= self.ground_friction

        # Move based on velocity.
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
