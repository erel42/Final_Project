import Tiles
import random


def init_chunk(chunk_list, x: int, y: int):
    Tiles.chunk_map_x(x)
    Tiles.chunk_map_y(y)
    finished_list = []
    row_list = [Tiles.RoadTile(0, 0, 'center', size=150)]
    for i in range(1, 4):
        row_list.append(Tiles.RoadTile(i, 0, 'horizontal', size=150))
    row_list.append(Tiles.RoadTile(4, 0, 'center', size=150))
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 1, 'vertical', size=150),
        None,
        None,
        None,
        Tiles.RoadTile(4, 1, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 2, 'vertical', size=150),
        None,
        None,
        None,
        Tiles.RoadTile(4, 2, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 3, 'vertical', size=150),
        None,
        None,
        None,
        Tiles.RoadTile(4, 3, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = []
    row_list.append(Tiles.RoadTile(0, 4, 'center', size=150))
    for i in range(1, 4):
        row_list.append(Tiles.RoadTile(i, 4, 'horizontal', size=150))
    row_list.append(Tiles.RoadTile(4, 4, 'center', size=150))
    finished_list.append(row_list)
    chunk_list[x][y] = finished_list


# 3 X 3 placements
# All possible structure placements

def restaurant_3x3_var_1(chunk_list, x: int, y: int):
    print('need to implement')


restaurant_dic = {
    1: restaurant_3x3_var_1
}

restaurant_dic_size = len(restaurant_dic)


def generate_restaurant(tile_list, x, y):
    restaurant_dic[random.randint(1, restaurant_dic_size)](tile_list, x, y)


def generate_house(tile_list, x, y):
    pass


def generate_blank(tile_list, x, y):
    pass


# Sets a chunk to only roads, for debug purposes
def demo_chunk(tile_list, x, y):
    _list = []
    for i in range(1, 6):
        new_list = []
        for j in range(1, 6):
            new_list.append(Tiles.RoadTile(5*x + (i - 1), 5*y + (j - 1), 'vertical', size=150))
        _list.append(new_list)
    tile_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]] = _list


def generate_base_tiles(chunk_list, x, y):
    init_chunk(chunk_list, x, y)
    chunk_list[x][y][1][1] = Tiles.ParkingTile(1, 1, size=150)
    chunk_list[x][y][1][2] = Tiles.ParkingTile(2, 1, size=150)
    chunk_list[x][y][1][3] = Tiles.ParkingTile(3, 1, size=150)

    chunk_list[x][y][2][1] = Tiles.ParkingTile(1, 2, size=150)
    chunk_list[x][y][2][2] = Tiles.RestaurantTile(2, 2, size=150)
    chunk_list[x][y][2][3] = Tiles.ParkingTile(3, 2, size=150)

    chunk_list[x][y][3][1] = Tiles.ParkingTile(1, 3, size=150)
    chunk_list[x][y][3][2] = Tiles.ParkingTile(2, 3, size=150)
    chunk_list[x][y][3][3] = Tiles.ParkingTile(3, 3, size=150)

    chunk_list[x][y][2][0] = Tiles.GeneratorTile(0, 2, "left")


restaurant_odds = 5
house_odds = 25


def generate_chunk(tile_list, x, y):
    # init_chunk(tile_list, x, y)
    Tiles.chunk_map_x(x)
    Tiles.chunk_map_y(y)
    demo_chunk(tile_list, x, y)
    """
    result = random.randint(1, 100)
    if result < restaurant_odds:
        generate_restaurant(tile_list, x, y)
    elif result < house_odds:
        generate_house(tile_list, x, y)
    else:
        generate_blank(tile_list, x, y)
    """
