import random

from character import Character


class FightingGame(object):
    def __init__(self, number_of_players, player_controllers):
        self.player_controllers = player_controllers
        self.players = []
        for player_id in range(number_of_players):
            new_player = Character(controller=player_controllers[player_id])
            new_player.x = 50.0
            new_player.y = -50.0
            self.players.append(new_player)

    def update(self):
        for player in self.players:
            player.update()
