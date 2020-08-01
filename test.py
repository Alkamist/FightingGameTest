import sys
import pygame
pygame.init()

from fixed_timestep import FixedTimestep
#from sprite import Sprite
from fighting_game import FightingGame
from digital_controller import DigitalController


zoom = 6.0
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

    width_offset = int(0.5 * window_width)
    height_offset = int(0.7 * window_height)

    display.fill(background_color)

    # Draw stage ground lines.
    for poly_line in fighting_game.stage.grounds:
        point_list = []
        for point in poly_line.points:
            point_list.append((int(point.x * zoom) + width_offset, -int(point.y * zoom) + height_offset))
        pygame.draw.lines(display, (160, 160, 160), False, point_list)

    # Draw players.
    for player_index in range(number_of_players):
        player = fighting_game.players[player_index]
        player_pixel_width = int(player.width * zoom)
        player_pixel_height = int(player.height * zoom)
        rect_left = int(player.x * zoom) - player_pixel_width + width_offset
        rect_top = -int(player.y * zoom) - player_pixel_height + height_offset

        player_rect = pygame.Rect(rect_left, rect_top, player_pixel_width, player_pixel_height)
        pygame.draw.rect(display, (30, 230, 30), player_rect)

        player_face_rect_width = 15
        player_face_rect_left = rect_left + 1 if not player.is_facing_right else rect_left + player_pixel_width - player_face_rect_width - 1
        player_face_rect = pygame.Rect(player_face_rect_left, rect_top + 1, player_face_rect_width, player_pixel_height - 2)
        pygame.draw.rect(display, (230, 30, 30), player_face_rect)

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
