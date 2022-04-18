import Tiles


# 3 X 3 placements
# All possible structure placements

def restaurant_3x3_var_1(x: int, y: int):
    print('need to implement')


# Sets a chunk to only roads, for debug purposes
def init_chunk(tile_list, x, y):
    _list = []
    for i in range(1, 6):
        new_list = []
        for j in range(1, 6):
            new_list.append(Tiles.RoadTile(5*x + (i - 1), 5*y + (j - 1), 'vertical', size=150))
        _list.append(new_list)
    tile_list[x - Tiles.chunk_map_x_bounds[0]][y - Tiles.chunk_map_y_bounds[0]] = _list


def generate_base_tiles(_list, x, y):
    finished_list = []
    row_list = [Tiles.RoadTile(0, 0, 'center', size=150)]
    for i in range(1, 4):
        row_list.append(Tiles.RoadTile(i, 0, 'horizontal', size=150))
    row_list.append(Tiles.RoadTile(4, 0, 'center', size=150))
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 1, 'vertical', size=150),
        Tiles.ParkingTile(1, 1, size=150),
        Tiles.ParkingTile(2, 1, size=150),
        Tiles.ParkingTile(3, 1, size=150),
        Tiles.RoadTile(4, 1, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 2, 'vertical', size=150),
        Tiles.ParkingTile(1, 2, size=150),
        Tiles.RestaurantTile(2, 2, size=150),
        Tiles.ParkingTile(3, 2, size=150),
        Tiles.RoadTile(4, 2, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = [
        Tiles.RoadTile(0, 3, 'vertical', size=150),
        Tiles.ParkingTile(1, 3, size=150),
        Tiles.ParkingTile(2, 3, size=150),
        Tiles.ParkingTile(3, 3, size=150),
        Tiles.RoadTile(4, 3, 'vertical', size=150)
    ]
    finished_list.append(row_list)
    row_list = []
    row_list.append(Tiles.RoadTile(0, 4, 'center', size=150))
    for i in range(1, 4):
        row_list.append(Tiles.RoadTile(i, 4, 'horizontal', size=150))
    row_list.append(Tiles.RoadTile(4, 4, 'center', size=150))
    finished_list.append(row_list)
    _list[x][y] = finished_list
