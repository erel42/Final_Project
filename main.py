import pygame
import os

pygame.init()
screen = pygame.display.set_mode([1500, 1000], flags=pygame.FULLSCREEN)
exit_game = False
tile_list = [[]]
clock = pygame.time.Clock()
assets_path = 'Assets'
save_path = 'Saves'
cur_game_save_path = None


class Tile:
    grid_location = [0, 0]
    texture = None

    def set_location(self, x: int, y: int):
        self.grid_location = [x, y]

    def set_texture(self, path: str):
        self.texture = assets_path + '\\' + path


class RoadTile(Tile):

    def __init__(self, x: int, y: int, orientation: str):
        self.set_location(x, y)
        self.set_texture(orientation)  # Can be cross, vertical, horizontal, T_down, T_left, T_right and T_up


# Loads a tile from file
def load_tile(x: int, y: int):


# Unloads and saves a tile
def unload_tile(x: int, y: int):


# Generates the starting map
def generate_base_tiles():



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
    global exit_game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True


def main_menu():  # Display settings and save select



def close_game():
    print('Exiting game without saving')


def game_loop():
    while not exit_game:
        event_handler()

    close_game()


if __name__ == '__main__':
    main_menu()
    game_loop()
