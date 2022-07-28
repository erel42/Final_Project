import pygame
import os
import Tiles
import GenerateBuildings as Gen
import ingredientsAndRecipes
import menu

# Setting needed variables and initiating some things
pygame.init()
chunk_list = Tiles.chunk_map
active_chunks = Tiles.active_chunks
check_press = False
mouse_pos = [0, 0]
screen = pygame.display.set_mode(Tiles.screen_size)
pygame.display.set_caption('Restaurant manager')
exit_game = False
money_gui = None
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
save_path = 'Saves'
cur_game_save_path = None
left_lower_corner = [-3, -3]
offset = [0, 0]
offset_change_speed = 10
Tile_list = None
last_money_value = 0
revenue = 0
income_timer = income_timer_default = 60
price_update_timer = price_update_timer_default = 10
enter_menu = True

# Some parameters
tile_size = screen.get_size()[0] / 8
move_up = move_down = move_right = move_left = False
center_chunk_x = center_chunk_y = 0


# A function for drawing translucent rectangles
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


# Updates the parts of the map that are worked on, improves performance drastically
def update_active_chunks():
    global center_chunk_x, center_chunk_y
    center_chunk_x = -int((offset[0] / Tiles.tile_size) / 5) - Tiles.chunk_map_x_bounds[0]
    center_chunk_y = -int((offset[1] / Tiles.tile_size) / 5) - Tiles.chunk_map_y_bounds[0]
    Tiles.chunk_map_y(center_chunk_y + 1)
    Tiles.chunk_map_y(center_chunk_y - 1)
    Tiles.chunk_map_x(center_chunk_x + 1)
    Tiles.chunk_map_x(center_chunk_x - 1)
    for i in range(center_chunk_x - 2, center_chunk_x + 3):
        for j in range(center_chunk_y - 2, center_chunk_y + 3):
            if chunk_list[i][j] is None:
                Gen.generate_chunk(chunk_list, i + Tiles.chunk_map_x_bounds[0], j + Tiles.chunk_map_y_bounds[0])
    center_chunk_x = -int((offset[0] / Tiles.tile_size) / 5) - Tiles.chunk_map_x_bounds[0]
    center_chunk_y = -int((offset[1] / Tiles.tile_size) / 5) - Tiles.chunk_map_y_bounds[0]


# Updates the amount of money earned
def update_revenue():
    global revenue
    revenue = 0
    for res in Tiles.res_list:
        revenue += res.get_income()


# Draws the map
def draw_tiles(surface, _list):
    for i in range(center_chunk_x - 2, center_chunk_x + 3):
        for j in range(center_chunk_y - 2, center_chunk_y + 3):
            if _list[i][j] is not None:
                for _sub_list in _list[i][j]:
                    for tile in _sub_list:
                        tile.draw(surface, mouse_pos, check_press, offset)


# Work in progress, currently doesn't work
def create_new_save(name: str):
    global cur_game_save_path
    # Creating a new directory
    cur_game_save_path = save_path + '\\' + name
    os.mkdir(cur_game_save_path)
    # generate_base_tiles()


# Work in progress, currently doesn't work
def load_save(name: str):
    global cur_game_save_path
    cur_game_save_path = save_path + '\\' + name


# Handles button and mouse events
def event_handler():
    global exit_game, offset, mouse_pos, check_press, move_up, move_down, move_right, move_left
    mouse_pos = pygame.mouse.get_pos()
    check_press = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_down = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_r:
                offset[0] = 0
                offset[1] = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_down = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_press = True
    if Tiles.menu_function is None:
        if move_up:
            offset[1] += offset_change_speed
        if move_down:
            offset[1] -= offset_change_speed
        if move_right:
            offset[0] -= offset_change_speed
        if move_left:
            offset[0] += offset_change_speed


# Closes the game
def close_game():
    print('Exiting game without saving')


# Updates the money text
def update_money():
    global money_gui
    money_gui = font.render('money:' + str(Tiles.money), True, (41, 210, 22))


# The actual game logic and flow. runs as long as the game runs
def game_loop():
    # Some globals
    global chunk_list, money_gui, last_money_value, income_timer, price_update_timer, income_timer_default
    global price_update_timer_default, check_press, enter_menu

    # As long as the game runs:
    while not exit_game:
        # Drawing the map
        update_active_chunks()  # Updates the loaded areas of the map
        event_handler()  # Checks for any button presses
        screen.fill((255, 255, 255))  # Clearing the screen
        draw_tiles(screen, chunk_list)  # Drawing the tiles

        # Handling money
        income_timer -= 1
        if income_timer == 0:
            income_timer = income_timer_default
            update_revenue()  # Checks how much money the player should make
            Tiles.money += int(revenue)  # Adds that amount of money
            price_update_timer -= 1
            if price_update_timer == 0:
                ingredientsAndRecipes.update_prices()
                price_update_timer = price_update_timer_default
        update_money()
        last_money_value = Tiles.money

        # When tile with a menu is pressed, it will change Tiles.menu_function to it's menu
        if Tiles.menu_function is not None:
            if not enter_menu:
                draw_rect_alpha(screen, (40, 40, 40, 160), (0, 0, 750, 750))
                Tiles.menu_function(screen, mouse_pos, check_press)  # Calls the menu of the pressed button
            else:
                enter_menu = False
        else:
            enter_menu = True
        screen.blit(money_gui, (20, 20))
        pygame.display.update()
    close_game()


if __name__ == '__main__':
    menu.show_menu(screen)  # Shows opening screen, continues when player starts a game
    Gen.generate_base_tiles(chunk_list, 0, 0)  # Generating the starting area
    update_money()  # Updating the money GUI
    ingredientsAndRecipes.update_prices()  # Updating prices
    game_loop()  # Starting the game
