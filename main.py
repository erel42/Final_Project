import pygame
import os
import Tiles
import GenerateBuildings as Gen
import menu
import time

pygame.init()
chunk_list = Tiles.chunk_map
active_chunks = Tiles.active_chunks
check_press = False
mouse_pos = [0, 0]
screen = pygame.display.set_mode([750, 750])
exit_game = False
money_gui = None
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
save_path = 'Saves'
cur_game_save_path = None
left_lower_corner = [-3, -3]
offset = [0, 0]
offset_change_speed = 10
Tile_list = None
show_overlay = False
last_money_value = money = 0

# Some parameters
tile_size = screen.get_size()[0] / 8
move_up = move_down = move_right = move_left = False
center_chunk_x = center_chunk_y = 0


def update_active_chunks():
    global center_chunk_x, center_chunk_y
    center_chunk_x = -int((offset[0] / 150) / 5) - Tiles.chunk_map_x_bounds[0]
    center_chunk_y = -int((offset[1] / 150) / 5) - Tiles.chunk_map_y_bounds[0]
    Tiles.chunk_map_y(center_chunk_y + 1)
    Tiles.chunk_map_y(center_chunk_y - 1)
    Tiles.chunk_map_x(center_chunk_x + 1)
    Tiles.chunk_map_x(center_chunk_x - 1)
    center_chunk_x = -int((offset[0] / 150) / 5) - Tiles.chunk_map_x_bounds[0]
    center_chunk_y = -int((offset[1] / 150) / 5) - Tiles.chunk_map_y_bounds[0]


def draw_tiles(surface, _list):
    for i in range(center_chunk_x - 1, center_chunk_x + 2):
        for j in range(center_chunk_y - 1, center_chunk_y + 2):
            if _list[i][j] is not None:
                for _sub_list in _list[i][j]:
                    for tile in _sub_list:
                        tile.draw(surface, mouse_pos, check_press, offset)


def create_new_save(name: str):
    global cur_game_save_path
    # Creating a new directory
    cur_game_save_path = save_path + '\\' + name
    os.mkdir(cur_game_save_path)
    # generate_base_tiles()


def load_save(name: str):
    global cur_game_save_path
    cur_game_save_path = save_path + '\\' + name


def event_handler():
    global exit_game, offset, mouse_pos, check_press, move_up, move_down, move_right, move_left
    mouse_pos = pygame.mouse.get_pos()
    check_press = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                move_down = True
            if event.key == pygame.K_UP:
                move_up = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                move_down = False
            if event.key == pygame.K_UP:
                move_up = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_press = True

    if move_up:
        offset[1] += offset_change_speed
    if move_down:
        offset[1] -= offset_change_speed
    if move_right:
        offset[0] -= offset_change_speed
    if move_left:
        offset[0] += offset_change_speed


def close_game():
    print('Exiting game without saving')


def update_money():
    global money_gui
    money_gui = font.render('money:' + str(money), True, (41, 210, 22))


def game_loop():
    global chunk_list, money_gui, last_money_value, money
    while not exit_game:
        update_active_chunks()
        event_handler()
        screen.fill((255, 255, 255))
        draw_tiles(screen, chunk_list)
        if last_money_value != money:
            update_money()
            last_money_value = money
        screen.blit(money_gui, (20, 20))
        pygame.display.update()
    close_game()


if __name__ == '__main__':
    menu.show_menu(screen)
    Gen.generate_base_tiles(chunk_list, 0, 0)
    Tiles.chunk_map_y(-2)
    Gen.demo_chunk(chunk_list, 0, -2)
    update_money()
    game_loop()
