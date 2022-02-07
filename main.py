import pygame
import os
import Tiles
import GenerateBuildings as gen

pygame.init()
screen = pygame.display.set_mode([1500, 1000], flags=pygame.FULLSCREEN)
exit_game = False
chunk_list = [[]]
clock = pygame.time.Clock()
save_path = 'Saves'
cur_game_save_path = None
left_corner = [0, 0]

# Some parameters
chunkSize = 15
tile_size = screen.get_size()[0] / 10
offset = 0
max_offset = screen.get_size()[0]

scroll_dic = {
    'right': scroll_chunk_right,
    'left': scroll_chunk_left,
    'up': scroll_chunk_up,
    'down': scroll_chunk_down

}


# Returns the correct chunk ids
def calc_chunk(x: int, y: int):
    chunk_x = x / chunkSize
    chunk_y = y / chunkSize
    return chunk_x, chunk_y


# Loads a chunk file, chunk is a 10X10 tiles
def scroll_chunk(direction: int):
    scroll_dic[direction]()


def scroll_chunk_right():
    chunk_list[0][0] = chunk_list[0][1]
    chunk_list[1][0] = chunk_list[1][1]
    _x, _y = Tiles.Chunk.get_location(chunk_list[1][0])
    _x = _x - 1
    chunk_list[0][0] = Tiles.Chunk(_x, _Y)
    chunk_list[0][1] = Tiles.Chunk(_x, _Y)

# Generates the starting map, 4 chunks exactly
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
