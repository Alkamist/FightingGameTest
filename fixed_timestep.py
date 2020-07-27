import time


class FixedTimestep(object):
    def __init__(self, physics_fps, display_fps):
        self.physics_fps = physics_fps
        self.physics_fraction = 0.0
        self.physics_delta = 1.0 / float(physics_fps)

        self.display_fps = display_fps
        self.display_delta = 0.0

        self._accumulator = 0.0
        self._time = time.perf_counter()

    def update(self, update_function):
        self.display_delta = time.perf_counter() - self._time
        self._time += self.display_delta
        self._accumulator += self.display_delta
        while self._accumulator >= self.physics_delta:
            update_function()
            self._accumulator -= self.physics_delta
        self.physics_fraction = self._accumulator / self.physics_delta
