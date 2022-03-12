import pygame
import os
import Tiles
import GenerateBuildings as gen
import menu
import time

pygame.init()
tile_list = []
check_press = False
mouse_pos = [0, 0]
screen = pygame.display.set_mode([1000, 1000])
exit_game = False
clock = pygame.time.Clock()
save_path = 'Saves'
cur_game_save_path = None
left_lower_corner = [-3, -3]
offset = [0, 0]
offset_change_speed = 10
Tile_list = None
show_overlay = False

# Some parameters
tile_size = screen.get_size()[0] / 8


def draw_tiles(surface, _list):
    for sub_list in _list:
        for tile in sub_list:
            tile.draw(surface, mouse_pos, check_press, offset)


def generate_base_tiles():
    print('need to implement')


def create_new_save(name: str):
    global cur_game_save_path
    # Creating a new directory
    cur_game_save_path = save_path + '\\' + name
    os.mkdir(cur_game_save_path)
    generate_base_tiles()


def load_save(name: str):
    global cur_game_save_path
    cur_game_save_path = save_path + '\\' + name


def event_handler():
    global exit_game, offset, mouse_pos, check_press
    mouse_pos = pygame.mouse.get_pos()
    check_press = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                offset[1] += offset_change_speed
            if event.key == pygame.K_UP:
                offset[1] -= offset_change_speed
            if event.key == pygame.K_RIGHT:
                offset[0] += offset_change_speed
            if event.key == pygame.K_LEFT:
                offset[0] -= offset_change_speed
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_press = True


def close_game():
    print('Exiting game without saving')


def game_loop():
    global tile_list
    while not exit_game:
        event_handler()
        screen.fill((255, 255, 255))
        draw_tiles(screen, tile_list)

        pygame.display.update()
        print(offset)
    close_game()


if __name__ == '__main__':
    menu.show_menu(screen)
    for i in range(0, 7):
        new_list = []
        for j in range(0, 7):
            new_list.append(Tiles.RoadTile((i - 1) * 200, (j - 1) * 200, 'vertical'))
        tile_list.append(new_list[:])
    game_loop()
