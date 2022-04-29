import Buttons
import pygame

pygame.init()
assets_path = 'Assets'
chunk_map = [[None]]  # all the tiles in the game
active_chunks = [[None]]  # 3x3 chunks representing the tiles that can be seen on screen
chunk_map_x_bounds = [0, 0]
chunk_map_y_bounds = [0, 0]
menu_function = None
res_list = []
money = 50
active_resturaunt = None
gui_font = pygame.font.SysFont('Narkisim', 26)


def close_menu():
    global menu_function
    Buttons.disable_buttons = False
    menu_function = None


def upgrade_res():
    active_resturaunt.upgrade()


exit_btn_size = 100
exit_pic = pygame.image.load(assets_path + '\\GUI\\close.png')
exit_pic = pygame.transform.scale(exit_pic, (exit_btn_size, exit_btn_size))
exit_menu_button = Buttons.ButtonImg([750 - exit_btn_size, 0], exit_pic, close_menu, listen_disable=False)

upgrade_btn_size = 150
upgrade_pic = pygame.image.load(assets_path + '\\GUI\\upgrade.png')
upgrade_pic = pygame.transform.scale(upgrade_pic, (upgrade_btn_size, upgrade_btn_size))
upgrade_menu_button = Buttons.ButtonImg([425, 300], upgrade_pic, upgrade_res, listen_disable=False)

buy_btn_size = 150
buy_pic = pygame.image.load(assets_path + '\\GUI\\buy.png')
buy_pic = pygame.transform.scale(buy_pic, (buy_btn_size, buy_btn_size))
buy_menu_button = Buttons.ButtonImg([425, 300], buy_pic, upgrade_res, listen_disable=False)

restock_btn_size = 150
restock_pic = pygame.image.load(assets_path + '\\GUI\\upgrade.png')
restock_pic = pygame.transform.scale(restock_pic, (restock_btn_size, restock_btn_size))
restock_menu_button = Buttons.ButtonImg([175, 300], restock_pic, close_menu, listen_disable=False)


def draw_menu(surface, mouse, press):
    exit_menu_button.draw(surface, mouse, press, [0, 0], exit_btn_size)
    price_upgrade = gui_font.render('Cost: ' + str(active_resturaunt.price_to_upgrade), True, (255, 70, 50))
    if active_resturaunt.level == 0:
        buy_menu_button.draw(surface, mouse, press, [0, 0], buy_btn_size)
    else:
        upgrade_menu_button.draw(surface, mouse, press, [0, 0], upgrade_btn_size)
    surface.blit(price_upgrade, (425, 460))
    restock_menu_button.draw(surface, mouse, press, [0, 0], restock_btn_size)


def chunk_map_x(row):
    global chunk_map
    while row > chunk_map_x_bounds[1]:
        chunk_map.append([None] * (chunk_map_y_bounds[1] - chunk_map_y_bounds[0] + 1))
        chunk_map_x_bounds[1] = chunk_map_x_bounds[1] + 1
    while row < chunk_map_x_bounds[0]:
        chunk_map.insert(0, [None] * (chunk_map_y_bounds[1] - chunk_map_y_bounds[0] + 1))
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

    def show_menu(self):
        pass


class RoadTile(Tile):

    def __init__(self, x: int, y: int, orientation: str = None, texture: str = None, size=100):
        super().__init__(x, y, size)
        if orientation is None and texture is None:
            print('failed to create road tile')
        else:
            # Can be center, vertical, horizontal
            self.set_type('road')
            if texture is None:
                self.set_texture(assets_path + '\\Roads\\' + orientation)
            else:
                self.set_texture(texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, self.show_menu)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data


class RestaurantTile(Tile):

    def __init__(self, x: int, y: int, texture: str = '1', size=100):
        super().__init__(x, y, size)
        self.set_type('restaurant')
        self.set_texture(assets_path + '\\Resturants\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, self.show_menu)
        self.income = 0
        self.level = 0
        self.people_arr = []
        self.potential_costumers = 0
        self.space = 0
        res_list.append(self)
        self.price_to_upgrade = 30 * pow(2, self.level)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data

    def show_menu(self):
        global menu_function, active_resturaunt
        menu_function = draw_menu
        Buttons.disable_buttons = True
        active_resturaunt = self

    def get_income(self):
        return self.income

    def upgrade(self):
        global money
        if money >= self.price_to_upgrade:
            money -= self.price_to_upgrade
            self.income = self.income * 2 + 1
            self.space = self.space * 2 + 1
            self.level += 1
            self.price_to_upgrade = 10 * self.level * pow(2, self.level)


class ParkingTile(Tile):

    def __init__(self, x: int, y: int, texture: str = '1', size=100):
        super().__init__(x, y, size)
        self.set_type('parking')
        self.set_texture(assets_path + '\\Parking\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, self.show_menu)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data


class ParkTile(Tile):

    def __init__(self, x: int, y: int, texture: str = '1', size=100):
        super().__init__(x, y, size)
        self.set_type('park')
        self.population = 0
        self.set_texture(assets_path + '\\Parks\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, self.show_menu)
        self.update_pop()

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data

    def update_pop(self):
        self.population = 0
        if self.pos[0] / 5 < 0:
            offset_x = -1
        else:
            offset_x = 0
        if self.pos[1] / 5 < 0:
            offset_y = -1
        else:
            offset_y = 0
        for i in range(1, 4):
            for j in range(1, 4):
                if i == 2 and j == 2:
                    pass
                elif chunk_map[int(self.pos[0] / 5) - chunk_map_x_bounds[0] + offset_x][
                    int(self.pos[1] / 5) - chunk_map_y_bounds[0] + offset_y][i][j].type == 'house':
                    self.population += chunk_map[int(self.pos[0] / 5) - chunk_map_x_bounds[0] + offset_x][
                        int(self.pos[1] / 5) - chunk_map_y_bounds[0] + offset_y][i][j].get_pop()

    def get_pop(self):
        return self.population


class HouseTile(Tile):

    def __init__(self, x: int, y: int, population: int, texture: str = '1', size=100):
        super().__init__(x, y, size)
        self.set_type('house')
        self.population = population
        self.set_texture(assets_path + '\\Houses\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, self.show_menu)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data

    def get_pop(self):
        return self.population


class EmptyTile(Tile):

    def __init__(self, x: int, y: int, texture: str = '1', size=100):
        super().__init__(x, y, size)
        self.set_type('empty')
        self.set_texture(assets_path + '\\Empty\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (self.tile_size, self.tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, self.show_menu)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data
