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
screen = pygame.display.set_mode([750, 750])
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
    finished_list = []
    row_list = []
    row_list.append(Tiles.RoadTile(0, 0, 'center', size=150))
    for i in range(1, 4):
        row_list.append(Tiles.RoadTile(i, 0, 'horizontal', size=150))
    row_list.append(Tiles.RoadTile(4, 0, 'center', size=150))
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 1, 'vertical', size=150),
        Tiles.ParkingTile(1, 1, size=150),
        Tiles.ParkingTile(2, 1, size=150),
        Tiles.ParkingTile(3, 1, size=150),
        Tiles.RoadTile(4, 1, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 2, 'vertical', size=150),
        Tiles.ParkingTile(1, 2, size=150),
        Tiles.RestaurantTile(2, 2, size=150),
        Tiles.ParkingTile(3, 2, size=150),
        Tiles.RoadTile(4, 2, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 3, 'vertical', size=150),
        Tiles.ParkingTile(1, 3, size=150),
        Tiles.ParkingTile(2, 3, size=150),
        Tiles.ParkingTile(3, 3, size=150),
        Tiles.RoadTile(4, 3, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = []
    row_list.append(Tiles.RoadTile(0, 4, 'center', size=150))
    for i in range(1, 4):
        row_list.append(Tiles.RoadTile(i, 4, 'horizontal', size=150))
    row_list.append(Tiles.RoadTile(4, 4, 'center', size=150))
    finished_list.append(row_list)
    return finished_list


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
                offset[1] -= offset_change_speed
            if event.key == pygame.K_UP:
                offset[1] += offset_change_speed
            if event.key == pygame.K_RIGHT:
                offset[0] -= offset_change_speed
            if event.key == pygame.K_LEFT:
                offset[0] += offset_change_speed
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
    close_game()


if __name__ == '__main__':
    menu.show_menu(screen)
    for i in range(0, 7):
        new_list = []
        for j in range(0, 7):
            new_list.append(Tiles.RoadTile((i - 1), (j - 1), 'vertical', size=150))
        tile_list.append(new_list)
    tile_list = generate_base_tiles()[:]
    game_loop()
