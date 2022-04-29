import Tiles
import random


def init_chunk(chunk_list, x: int, y: int):
    Tiles.chunk_map_x(x + 1)
    Tiles.chunk_map_x(x - 1)
    Tiles.chunk_map_y(y + 1)
    Tiles.chunk_map_y(y - 1)
    finished_list = []
    row_list = [
        Tiles.RoadTile(5 * x, 5 * y, 'center'),
        Tiles.RoadTile(5 * x + 1, 5 * y, 'horizontal'),
        Tiles.RoadTile(5 * x + 2, 5 * y, 'horizontal'),
        Tiles.RoadTile(5 * x + 3, 5 * y, 'horizontal'),
        Tiles.RoadTile(5 * x + 4, 5 * y, 'center')
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(5 * x, 5 * y + 1, 'vertical'),
        None,
        None,
        None,
        Tiles.RoadTile(5 * x + 4, 5 * y + 1, 'vertical')
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(5 * x, 5 * y + 2, 'vertical'),
        None,
        None,
        None,
        Tiles.RoadTile(5 * x + 4, 5 * y + 2, 'vertical')
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(5 * x, 5 * y + 3, 'vertical'),
        None,
        None,
        None,
        Tiles.RoadTile(5 * x + 4, 5 * y + 3, 'vertical')
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(5 * x, 5 * y + 4, 'center'),
        Tiles.RoadTile(5 * x + 1, 5 * y + 4, 'horizontal'),
        Tiles.RoadTile(5 * x + 2, 5 * y + 4, 'horizontal'),
        Tiles.RoadTile(5 * x + 3, 5 * y + 4, 'horizontal'),
        Tiles.RoadTile(5 * x + 4, 5 * y + 4, 'center')
    ]
    finished_list.append(row_list)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]] = finished_list


# 3 X 3 placements
# All possible structure placements

def restaurant_3x3_var_1(chunk_list, x: int, y: int):
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][1] = Tiles.EmptyTile(5 * x + 1,
                                                                                                         5 * y + 1)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][2] = Tiles.ParkingTile(5 * x + 2,
                                                                                                           5 * y + 1)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][3] = Tiles.EmptyTile(5 * x + 3,
                                                                                                         5 * y + 1)

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][1] = Tiles.ParkingTile(5 * x + 1,
                                                                                                           5 * y + 2)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][2] = Tiles.RestaurantTile(5 * x + 2,
                                                                                                              5 * y + 2)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][3] = Tiles.ParkingTile(5 * x + 3,
                                                                                                           5 * y + 2)

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][1] = Tiles.EmptyTile(5 * x + 1,
                                                                                                         5 * y + 3)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][2] = Tiles.ParkingTile(5 * x + 2,
                                                                                                           5 * y + 3)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][3] = Tiles.EmptyTile(5 * x + 3,
                                                                                                         5 * y + 3)


restaurant_dic = {
    1: restaurant_3x3_var_1
}

restaurant_dic_size = len(restaurant_dic)


def generate_restaurant(tile_list, x, y):
    restaurant_dic[random.randint(1, restaurant_dic_size)](tile_list, x, y)


# Incorrect need to fix!
def house_3x3_var_1(chunk_list, x: int, y: int):
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][1] = Tiles.HouseTile(5 * x + 1,
                                                                                                         5 * y + 1, 6)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][2] = Tiles.HouseTile(5 * x + 2,
                                                                                                         5 * y + 1, 6)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][3] = Tiles.HouseTile(5 * x + 3,
                                                                                                         5 * y + 1, 6)

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][1] = Tiles.ParkingTile(5 * x + 1,
                                                                                                           5 * y + 2)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][3] = Tiles.ParkingTile(5 * x + 3,
                                                                                                           5 * y + 2)

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][1] = Tiles.HouseTile(5 * x + 1,
                                                                                                         5 * y + 3, 3,
                                                                                                         texture='2')
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][2] = Tiles.ParkingTile(5 * x + 2,
                                                                                                           5 * y + 3)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][3] = Tiles.HouseTile(5 * x + 3,
                                                                                                         5 * y + 3, 3,
                                                                                                         texture='2')

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][2] = Tiles.ParkTile(5 * x + 2,
                                                                                                        5 * y + 2)


house_dic = {
    1: house_3x3_var_1
}

house_dic_size = len(house_dic)


def generate_house(chunk_list, x, y):
    house_dic[random.randint(1, house_dic_size)](chunk_list, x, y)


def generate_blank(chunk_list, x, y):
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][1] = Tiles.EmptyTile(5 * x + 1,
                                                                                                         5 * y + 1)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][2] = Tiles.EmptyTile(5 * x + 2,
                                                                                                         5 * y + 1)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][3] = Tiles.EmptyTile(5 * x + 3,
                                                                                                         5 * y + 1)

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][1] = Tiles.EmptyTile(5 * x + 1,
                                                                                                         5 * y + 2)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][2] = Tiles.EmptyTile(5 * x + 2,
                                                                                                         5 * y + 2)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][3] = Tiles.EmptyTile(5 * x + 3,
                                                                                                         5 * y + 2)

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][1] = Tiles.EmptyTile(5 * x + 1,
                                                                                                         5 * y + 3)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][2] = Tiles.EmptyTile(5 * x + 2,
                                                                                                         5 * y + 3)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][3] = Tiles.EmptyTile(5 * x + 3,
                                                                                                         5 * y + 3)


# Sets a chunk to only roads, for debug purposes
def demo_chunk(tile_list, x, y):
    _list = []
    for i in range(1, 6):
        new_list = []
        for j in range(1, 6):
            new_list.append(Tiles.RoadTile(5 * x + (i - 1), 5 * y + (j - 1), 'vertical'))
        _list.append(new_list)
    tile_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]] = _list


def generate_base_tiles(chunk_list, x, y):
    init_chunk(chunk_list, x, y)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][1] = Tiles.ParkingTile(1, 1)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][2] = Tiles.ParkingTile(2, 1)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][1][3] = Tiles.ParkingTile(3, 1)

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][1] = Tiles.ParkingTile(1, 2)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][2] = Tiles.RestaurantTile(2, 2)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][2][3] = Tiles.ParkingTile(3, 2)

    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][1] = Tiles.ParkingTile(1, 3)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][2] = Tiles.ParkingTile(2, 3)
    chunk_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]][3][3] = Tiles.ParkingTile(3, 3)


restaurant_odds = 7
house_odds = 60


def generate_chunk(chunk_list, x, y):
    init_chunk(chunk_list, x, y)
    result = random.randint(1, 100)
    if result < restaurant_odds:
        generate_restaurant(chunk_list, x, y)
    elif result < house_odds:
        generate_house(chunk_list, x, y)
    else:
        generate_blank(chunk_list, x, y)
