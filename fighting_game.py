import random

from character import Character


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PolyLine(object):
    def __init__(self, points):
        self.points = points


class Stage(object):
    def __init__(self, grounds, ceilings, left_walls, right_walls):
        self.grounds = grounds
        self.ceilings = ceilings
        self.left_walls = left_walls
        self.right_walls = right_walls


class FightingGame(object):
    def __init__(self, number_of_players, player_controllers):
        self.player_controllers = player_controllers

        self.players = []
        for player_id in range(number_of_players):
            new_player = Character(controller=player_controllers[player_id])
            new_player.x = 0.0
            new_player.y = 0.0
            self.players.append(new_player)

        self.stage = Stage(
            grounds=[
                PolyLine([
                    Point(-56.0, -3.5),
                    Point(-39.0, 0.0),
                    Point(39.0, 0.0),
                    Point(56.0, -3.5),
                ]),
            ],
            ceilings=[],
            left_walls=[],
            right_walls=[],
        )

    def update(self):
        for player in self.players:
            player.update()
