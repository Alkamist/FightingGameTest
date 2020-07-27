from character import Character


class FightingGame(object):
    def __init__(self):
        self.character = Character(
            position=[0.0, -400.0],
            velocity=[20.0, 20.0],
            gravity=[0.0, -1.0],
        )

    def update(self):
        character = self.character
        character.update()

        left_wall = 0.0
        right_wall = 1000.0
        top_wall = 0.0
        bottom_wall = -800.0

        if character.position[0] < left_wall:
            character.position[0] = left_wall
            character.velocity[0] = -character.velocity[0]

        if character.position[0] > right_wall:
            character.position[0] = right_wall
            character.velocity[0] = -character.velocity[0]

        if character.position[1] < bottom_wall:
            character.position[1] = bottom_wall
            character.velocity[1] = -character.velocity[1]

        if character.position[1] > top_wall:
            character.position[1] = top_wall
            character.velocity[1] = -character.velocity[1]
