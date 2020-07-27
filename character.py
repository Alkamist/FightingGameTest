class Character(object):
    def __init__(self, position, velocity, gravity):
        self.position = position
        self.velocity = velocity
        self.gravity = gravity

    def update(self):
        self._handle_gravity()
        self._handle_movement()

    def _handle_gravity(self):
        self.velocity[0] += self.gravity[0]
        self.velocity[1] += self.gravity[1]

    def _handle_movement(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]