import Buttons

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

    def __init__(self, x: int, y: int, orientation: str = None, texture: str = None):
        super().__init__(x, y)
        if orientation is None and texture is None:
            print('failed to create road tile')
        else:
            self.set_location(x, y)
            # Can be cross, vertical, horizontal, T_down, T_left, T_right and T_up
            self.set_type('road')
            if texture is None:
                self.set_texture(assets_path + '\\Roads\\' + orientation)
            else:
                self.set_texture(texture)
        btn = Buttons.ButtonImg([x, y, x + self.size[0], y + self.size[1]], texture + '.png', texture + 'Hover.png',
                                self.show_memu)

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

    def draw(self, surface, offset, tile_size):
