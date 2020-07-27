import random

from character import Character


class FightingGame(object):
    def __init__(self, number_of_players):
        self.players = [Character(
            position=[300.0 * random.random(), -400.0 * random.random()],
            velocity=[20.0 * random.random(), -3.0 * random.random()],
            gravity=[0.0, -1.0],
        ) for _ in range(number_of_players)]

    def update(self):
        left_wall = 0.0
        right_wall = 1000.0
        top_wall = 0.0
        bottom_wall = -800.0

        for player in self.players:
            player.update()

            if player.position[0] < left_wall:
                player.position[0] = left_wall
                player.velocity[0] = -player.velocity[0]

            if player.position[0] > right_wall:
                player.position[0] = right_wall
                player.velocity[0] = -player.velocity[0]

            if player.position[1] < bottom_wall:
                player.position[1] = bottom_wall
                player.velocity[1] = -player.velocity[1]

            if player.position[1] > top_wall:
                player.position[1] = top_wall
                player.velocity[1] = -player.velocity[1]
