import Buttons
import pygame

assets_path = 'Assets'
chunk_map = [[None]]  # all the tiles in the game
active_chunks = [[None]]  # 3x3 chunks representing the tiles that can be seen on screen
chunk_map_x_bounds = [0, 0]
chunk_map_y_bounds = [0, 0]


def chunk_map_x(row):
    global chunk_map
    while row > chunk_map_x_bounds[1]:
        chunk_map.append([None] * (chunk_map_y_bounds[1] - chunk_map_y_bounds[0]))
        chunk_map_x_bounds[1] = chunk_map_x_bounds[1] + 1
    while row < chunk_map_x_bounds[0]:
        chunk_map.insert(0, [None] * (chunk_map_y_bounds[1] - chunk_map_y_bounds[0]))
        chunk_map_x_bounds[0] = chunk_map_x_bounds[0] - 1


def chunk_map_y(col):
    global chunk_map
    while col > chunk_map_y_bounds[1]:
        for row in chunk_map:
            row.append(None)
        chunk_map_y_bounds[1] = chunk_map_y_bounds[1] + 1
    while col < chunk_map_y_bounds[0]:
        for row in chunk_map:
            row.insert(0, None)
        chunk_map_y_bounds[0] = chunk_map_y_bounds[0] - 1


class Tile:
    type = ''
    texture = None
    btn = None

    def __init__(self, x: int, y: int, size: int):
        self.grid_location = [x, y]
        self.set_location(x * size, y * size)
        self.pos = [x, y]
        self.tile_size = size

    def set_location(self, x: int, y: int):
        self.grid_location = [x, y]

    def set_texture(self, path: str):
        self.texture = path

    def set_type(self, _type: str):
        self.type = _type

    def draw(self, surface, mouse, press, offset):
        self.btn.draw(surface, mouse, press, offset, self.tile_size)


class RoadTile(Tile):

    def __init__(self, x: int, y: int, orientation: str = None, texture: str = None, size=100):
        super().__init__(x, y, size)
        if orientation is None and texture is None:
            print('failed to create road tile')
        else:
            # Can be cross, vertical, horizontal, T_down, T_left, T_right and T_up
            self.set_type('road')
            if texture is None:
                self.set_texture(assets_path + '\\Roads\\' + orientation)
            else:
                self.set_texture(texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        picture_hover = pygame.image.load(self.texture + 'Hover.png')
        picture_hover = pygame.transform.scale(picture_hover, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, picture_hover, self.show_memu)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data

    def show_memu(self):
        pass


class RestaurantTile(Tile):

    def __init__(self, x: int, y: int, texture: str = '1', size=100):
        super().__init__(x, y, size)
        self.set_type('restaurant')
        self.set_texture(assets_path + '\\Resturants\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        picture_hover = pygame.image.load(self.texture + 'Hover.png')
        picture_hover = pygame.transform.scale(picture_hover, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, picture_hover, self.show_menu)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data

    def show_menu(self):
        print('needToImplement')


class ParkingTile(Tile):

    def show_menu(self):
        pass

    def __init__(self, x: int, y: int, texture: str = '1', size=100):
        super().__init__(x, y, size)
        self.set_type('restaurant')
        self.set_texture(assets_path + '\\Parking\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        picture_hover = pygame.image.load(self.texture + 'Hover.png')
        picture_hover = pygame.transform.scale(picture_hover, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, picture_hover, self.show_menu)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data


class GeneratorTile(Tile):

    def __init__(self, x: int, y: int, direction: str, size=100):
        super().__init__(x, y, size)
        self.direction = direction

    def draw(self, surface, mouse, press, offset):
        pass
