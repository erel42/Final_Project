import Buttons
import pygame

assets_path = 'Assets'


class Tile:
    type = ''
    texture = None
    btn = None
    size = [0, 0]

    def __init__(self, x: int, y: int):
        self.grid_location = [x, y]

    def set_location(self, x: int, y: int):
        self.grid_location = [x, y]

    def set_texture(self, path: str):
        self.texture = path

    def set_type(self, _type: str):
        self.type = _type

    def set_size(self, _size: [int, int]):
        self.size = _size[:]


class RoadTile(Tile):

    def __init__(self, x: int, y: int, orientation: str = None, texture: str = None, size=100):
        super().__init__(x, y)
        if orientation is None and texture is None:
            print('failed to create road tile')
        else:
            self.set_location(x * size, y * size)
            self.pos = [x, y]
            # Can be cross, vertical, horizontal, T_down, T_left, T_right and T_up
            self.set_type('road')
            if texture is None:
                self.set_texture(assets_path + '\\Roads\\' + orientation)
            else:
                self.set_texture(texture)
        self.tile_size = size
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
        print('needToImplement')

    def draw(self, surface, mouse, press, offset):
        self.btn.draw(surface, mouse, press, offset, self.tile_size)


class RestaurantTile(Tile):

    def __init__(self, x: int, y: int, texture: str = '1', size=100):
        super().__init__(x, y)
        self.set_location(x * size, y * size)
        self.pos = [x, y]
        self.set_type('restaurant')
        self.set_texture(assets_path + '\\Resturants\\' + texture)
        self.tile_size = size
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
        print('needToImplement')

    def draw(self, surface, mouse, press, offset):
        self.btn.draw(surface, mouse, press, offset, self.tile_size)


class ParkingTile(Tile):

    def __init__(self, x: int, y: int, texture: str = '1', size=100):
        super().__init__(x, y)
        self.set_location(x * size, y * size)
        self.pos = [x, y]
        self.set_type('restaurant')
        self.set_texture(assets_path + '\\Parking\\' + texture)
        self.tile_size = size
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
        print('needToImplement')

    def draw(self, surface, mouse, press, offset):
        self.btn.draw(surface, mouse, press, offset, self.tile_size)
