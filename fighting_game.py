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
            new_player.y = 20.0
            self.players.append(new_player)

        self.stage = Stage(
            grounds=[
                PolyLine([
                    Point(-56.0, 0.0),
                    Point(56.0, 0.0),
                ]),
            ],
            ceilings=[],
            left_walls=[],
            right_walls=[],
        )

    def update(self):
        for player in self.players:
            player.update()
            ground_collision = self.detect_player_ground_collision(player)
            if ground_collision[0]:
                player.y += ground_collision[1]
                player.land()

    def detect_player_ground_collision(self, player):
        player_half_width = 0.5 * player.width
        player_left = player.x - player_half_width
        player_right = player.x + player_half_width
        player_bottom = player.y
        player_top = player.y + player.height

        for poly_line in self.stage.grounds:
            previous_point = None
            for point in poly_line.points:
                if previous_point is not None:
                    if player_right >= previous_point.x and player_left <= point.x \
                    and player_bottom < point.y and player_top >= point.y:
                        return True, previous_point.y - player_bottom
                previous_point = point

        return False, 0.0
