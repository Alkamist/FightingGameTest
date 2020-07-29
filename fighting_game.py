import random

from character import Character


class FightingGame(object):
    def __init__(self, number_of_players):
        self.players = [Character(
            position=[200.0 * player_id, -50.0],
            velocity=[0.0, 0.0],
            gravity=[0.0, -1.0],
        ) for player_id in range(number_of_players)]

    def update(self, player_controllers):
#        left_wall = 0.0
#        right_wall = 1000.0
#        top_wall = 0.0
#        bottom_wall = -800.0

        for player_index, player in enumerate(self.players):
            player.update(player_controllers[player_index])

#            if player.position[0] < left_wall:
#                player.position[0] = left_wall
#                player.velocity[0] = -player.velocity[0]
#
#            if player.position[0] > right_wall:
#                player.position[0] = right_wall
#                player.velocity[0] = -player.velocity[0]
#
#            if player.position[1] < bottom_wall:
#                player.position[1] = bottom_wall
#                player.velocity[1] = -player.velocity[1]
#
#            if player.position[1] > top_wall:
#                player.position[1] = top_wall
#                player.velocity[1] = -player.velocity[1]
