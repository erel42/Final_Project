import pygame

pygame.init()
screen = pygame.display.set_mode([1500, 1000], flags=pygame.FULLSCREEN)
exit_game = False

assets_path = 'C:\Users\erela\OneDrive\Documents\GitHub\Final_Project\Assets'


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
        self.set_texture(orientation)


def event_handler():
    global exit_game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True


def close_game():
    print('Exiting game without saving')


def gameloop():
    while not exit_game:
        event_handler()

    close_game()


if __name__ == '__main__':
    gameloop()
