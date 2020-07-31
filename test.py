import sys
import pygame
pygame.init()

from fixed_timestep import FixedTimestep
#from sprite import Sprite
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
player_controllers = [DigitalController()]
fighting_game = FightingGame(number_of_players, player_controllers)
#player_sprites = [Sprite(file_name="ppL.png") for _ in range(number_of_players)]


def update():
    player_controllers[0].update()
    fighting_game.update()

    #for player_index, player_sprite in enumerate(player_sprites):
    #    player_position = fighting_game.players[player_index].position
    #    player_sprite.update_position(player_position)

    display.fill(background_color)

    for player_index in range(number_of_players):
        player = fighting_game.players[player_index]
        zoom = 4.0
        rect_width = 30
        rect_height = 50
        rect_left = int(player.x * zoom) - int(0.5 * rect_width)
        rect_top = -int(player.y * zoom) - rect_height
        player_rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)
        pygame.draw.rect(display, (30, 230, 30), player_rect)

    pygame.display.flip()


def render():
    display.fill(background_color)
    #for player_sprite in player_sprites:
    #    player_sprite.render(display, fixed_timestep.physics_fraction)
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    fixed_timestep.update(update)
    #render()

    clock.tick(display_fps)
