assets_path = 'Assets'


class Tile:
    grid_location = [0, 0]
    texture = None

    def set_location(self, x: int, y: int):
        self.grid_location = [x, y]

    def set_texture(self, path: str):
        self.texture = path


class RoadTile(Tile):

    def __init__(self, x: int, y: int, orientation: str):
        self.set_location(x, y)
        self.set_texture(assets_path + '\\Roads\\' + orientation)  # Can be cross, vertical, horizontal, T_down, T_left, T_right and T_up

