import sys
import pygame
pygame.init()

from fixed_timestep import FixedTimestep
from sprite import Sprite
from fighting_game import FightingGame
from digital_controller import DigitalController


physics_fps = 60
display_fps = 144
window_width = 1000
window_height = 800
background_color = (0, 0, 0)
fixed_timestep = FixedTimestep(physics_fps=physics_fps, display_fps=display_fps)
clock = pygame.time.Clock()
display = pygame.display.set_mode((window_width, window_height))


number_of_players = 1
fighting_game = FightingGame(number_of_players)
player_controllers = [DigitalController()]
player_sprites = [Sprite(file_name="ppL.png") for _ in range(number_of_players)]


def update():
    player_controllers[0].update()
    fighting_game.update(player_controllers)
    for player_index, player_sprite in enumerate(player_sprites):
        player_position = fighting_game.players[player_index].position
        player_sprite.update_position(player_position)


def render():
    display.fill(background_color)
    for player_sprite in player_sprites:
        player_sprite.render(display, fixed_timestep.physics_fraction)
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    fixed_timestep.update(update)
    render()

    clock.tick(display_fps)
