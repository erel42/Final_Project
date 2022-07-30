import Buttons
import pygame
import random

import ingredientsAndRecipes

pygame.init()
screen_size = [750, 750]
assets_path = 'Assets'
chunk_map = [[None]]  # all the tiles in the game
active_chunks = [[None]]  # 3x3 chunks representing the tiles that can be seen on screen

# Which chunks exist
chunk_map_x_bounds = [0, 0]
chunk_map_y_bounds = [0, 0]

menu_function = None  # If None no menu is to be displayed, other wise it holds a reference to the drawing function
res_list = []  # A list of all restaurants the player owns
money = 50000000  # The player's money
active_restaurant = None  # The last restaurant the player clicked on
gui_font = pygame.font.SysFont('Narkisim', 26)  # A font for GUI elements

# Sets the size and amount of tiles on screen
tiles_on_screen = 8
tile_size = int(screen_size[0] / tiles_on_screen)
Buttons.t_size = tile_size


def update_tiles_on_screen(i: int):
    global tiles_on_screen, tile_size
    tiles_on_screen += i
    tile_size = int(screen_size[0] / tiles_on_screen)
    Buttons.update_size = True
    Buttons.t_size = tile_size


chunks_x_on_screen = chunks_y_on_screen = 0


# Calculates the number of chunks displayed (so that they can be drawn)
def update_chunks_on_screen():
    global chunks_x_on_screen, chunks_y_on_screen
    chunks_x_on_screen = int((screen_size[0] / tile_size) / 5 + 2)
    chunks_y_on_screen = int((screen_size[1] / tile_size) / 5 + 2)


update_chunks_on_screen()

buy_multiplier = 1  # For restock menu
report_price = 0  # The price of issuing a report
skip_gui_buttons = False  # If true skips GUI button, prevents accidental clicks on first frame of change

# Auto-buy menu elements
chosen_supplier_index = 0
chosen_ing = 0
max_price_input = 0
input_enable = False

# Force a screen update
force_update_screen = False

max_demand_weight = 1
min_demand_weight = 0.5

buy_upgrade_pos_text = []

# Auto-buy feature. Index marks the ingredient and value marks the chosen supplier
auto_buy = [-1] * ingredientsAndRecipes.num_of_ingredients
stop_auto_buy = [0] * ingredientsAndRecipes.num_of_ingredients  # Index marks the ingredient and value marks max price


# A function that is called upon menu closure
def close_menu():
    global menu_function, skip_gui_buttons, force_update_screen
    Buttons.disable_buttons = False
    menu_function = None
    skip_gui_buttons = True
    force_update_screen = True
    Buttons.update_size = False


# Exit button:
exit_btn_size = 100


def update_exit_btn():
    return [screen_size[0] - exit_btn_size, 0]


exit_pic = pygame.image.load(assets_path + '\\GUI\\close.png')
exit_pic = pygame.transform.scale(exit_pic, (exit_btn_size, exit_btn_size))
exit_menu_button = Buttons.ButtonImg([screen_size[0] - exit_btn_size, 0], exit_pic, close_menu, listen_disable=False,
                                     dead_zones=False, btn_update_func=update_exit_btn)


# Restocks an item
def restock_item(i):
    active_restaurant.restock_item(i)


# Sells a restaurant
def sell_res():
    active_restaurant.sell()


# Selecting an ing in auto-buy menu
def select_ing(i):
    global chosen_ing, max_price_input
    chosen_ing = i
    max_price_input = stop_auto_buy[chosen_ing]


# Canceling an existing auto-buy setting
def cancel_auto_buy(i):
    set_auto_buy(i, -1, 0)


# Create an auto buy
def apply_auto_buy():
    set_auto_buy(chosen_ing, chosen_supplier_index, max_price_input)


# ing buttons:
ing_btn_size = int(((screen_size[1] - 200) / ingredientsAndRecipes.num_of_ingredients) * 3 / 4)
ing_btn_spacing = int(ing_btn_size / 3)


def update_ing_btn(i):
    return [0, 100 + (ing_btn_size + ing_btn_spacing) * i]


ing_pic = [pygame.transform.scale(
    pygame.image.load(assets_path + '\\ingredients\\' + ingredientsAndRecipes.ing_list[i] + '.png'),
    (ing_btn_size, ing_btn_size))
    for i in range(0, ingredientsAndRecipes.num_of_ingredients)]

ing_buttons = [
    Buttons.ButtonImg([0, 100 + (ing_btn_size + ing_btn_spacing) * i], ing_pic[i], restock_item, listen_disable=False,
                      parameter_for_function=i, btn_update_func=update_ing_btn, parameter_for_update=i) for i in
    range(0, ingredientsAndRecipes.num_of_ingredients)]

ing_buttons_auto_buy = [
    Buttons.ButtonImg([0, 100 + (ing_btn_size + ing_btn_spacing) * i], ing_pic[i], select_ing, listen_disable=False,
                      parameter_for_function=i, btn_update_func=update_ing_btn, parameter_for_update=i) for i in
    range(0, ingredientsAndRecipes.num_of_ingredients)]

# Cancel buttons:
cancel_pic = pygame.image.load(assets_path + '\\GUI\\close.png')
cancel_pic = pygame.transform.scale(cancel_pic, (ing_btn_size, ing_btn_size))


def update_cancel_btn(i):
    return [200, 100 + (ing_btn_size + ing_btn_spacing) * i]


ing_delete_auto_buy = [
    Buttons.ButtonImg([200, 100 + (ing_btn_size + ing_btn_spacing) * i], cancel_pic, cancel_auto_buy,
                      listen_disable=False, parameter_for_function=i, btn_update_func=update_cancel_btn,
                      parameter_for_update=i) for i in
    range(0, ingredientsAndRecipes.num_of_ingredients)]


# Cycles between the suppliers
def cycle_supplier(i):
    global active_restaurant
    active_restaurant.supplier = active_restaurant.supplier + i
    if active_restaurant.supplier < 0:
        active_restaurant.supplier = ingredientsAndRecipes.num_of_ing_suppliers - 1
    elif active_restaurant.supplier == ingredientsAndRecipes.num_of_ing_suppliers:
        active_restaurant.supplier = 0


# Cycles between suppliers in auto-buy menu
def cycle_supplier_auto_buy(i):
    global chosen_supplier_index
    chosen_supplier_index = chosen_supplier_index + i
    if chosen_supplier_index < 0:
        chosen_supplier_index = ingredientsAndRecipes.num_of_ing_suppliers - 1
    elif chosen_supplier_index == ingredientsAndRecipes.num_of_ing_suppliers:
        chosen_supplier_index = 0


# Cycles recipe
def cycle_recipe(i):
    global active_restaurant
    index = active_restaurant.activeRecipe.meal_index
    index = index + i
    if index < 0:
        index = ingredientsAndRecipes.meal_count - 1
    elif index == ingredientsAndRecipes.meal_count:
        index = 0
    active_restaurant.activeRecipe = ingredientsAndRecipes.recipes[index]


# Enables input for max price for auto-buy
def set_price_limit():
    global max_price_input, input_enable
    max_price_input = 0
    input_enable = True


# Cycle buttons:
cycle_btn_size = 100


def update_cycle_right_btn():
    return [screen_size[0] - cycle_btn_size, exit_btn_size + 70]


cycle_right_pic = pygame.image.load(assets_path + '\\GUI\\right.png')
cycle_right_pic = pygame.transform.scale(cycle_right_pic, (cycle_btn_size, cycle_btn_size))
cycle_right_button = Buttons.ButtonImg([screen_size[0] - cycle_btn_size, exit_btn_size + 70], cycle_right_pic,
                                       cycle_supplier, listen_disable=False, parameter_for_function=1,
                                       btn_update_func=update_cycle_right_btn)


def update_cycle_left_btn():
    return [screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 70]


cycle_left_pic = pygame.image.load(assets_path + '\\GUI\\left.png')
cycle_left_pic = pygame.transform.scale(cycle_left_pic, (cycle_btn_size, cycle_btn_size))
cycle_left_button = Buttons.ButtonImg([screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 70], cycle_left_pic,
                                      cycle_supplier, listen_disable=False, parameter_for_function=-1,
                                      btn_update_func=update_cycle_left_btn)


def update_cycle_2_right_btn():
    return [screen_size[0] - cycle_btn_size, exit_btn_size + cycle_btn_size + 110]


cycle_2_right_button = Buttons.ButtonImg([screen_size[0] - cycle_btn_size, exit_btn_size + cycle_btn_size + 110],
                                         cycle_right_pic, cycle_recipe, listen_disable=False,
                                         parameter_for_function=1, btn_update_func=update_cycle_2_right_btn)


def update_cycle_2_left_btn():
    return [screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + cycle_btn_size + 110]


cycle_2_left_button = Buttons.ButtonImg(
    [screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + cycle_btn_size + 110], cycle_left_pic, cycle_recipe,
    listen_disable=False, parameter_for_function=-1, btn_update_func=update_cycle_2_left_btn)

cycle_3_right_button = Buttons.ButtonImg([screen_size[0] - cycle_btn_size, exit_btn_size + 70],
                                         cycle_right_pic, cycle_supplier_auto_buy, listen_disable=False,
                                         parameter_for_function=1, btn_update_func=update_cycle_right_btn)

cycle_3_left_button = Buttons.ButtonImg(
    [screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 70], cycle_left_pic, cycle_supplier_auto_buy,
    listen_disable=False, parameter_for_function=-1, btn_update_func=update_cycle_left_btn)

cycle_4_right_button = Buttons.ButtonImg([screen_size[0] - cycle_btn_size, exit_btn_size + 70], cycle_right_pic,
                                         update_tiles_on_screen, listen_disable=False, parameter_for_function=1,
                                         btn_update_func=update_cycle_right_btn)

cycle_4_left_button = Buttons.ButtonImg([screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 70], cycle_left_pic,
                                        update_tiles_on_screen, listen_disable=False, parameter_for_function=-1,
                                        btn_update_func=update_cycle_left_btn)

# Max button, AKA price limit for auto buy:
max_btn_size = 100


def update_max_btn():
    return [screen_size[0] - max_btn_size, exit_btn_size + cycle_btn_size + 110]


max_pic = pygame.image.load(assets_path + '\\GUI\\max.png')
max_pic = pygame.transform.scale(max_pic, (max_btn_size, max_btn_size))
max_button = Buttons.ButtonImg([screen_size[0] - max_btn_size, exit_btn_size + cycle_btn_size + 110],
                               max_pic, set_price_limit, listen_disable=False, btn_update_func=update_max_btn)

# Apply button, from auto-buy menu:
apply_btn_size = 100


def update_apply_btn():
    return [screen_size[0] - apply_btn_size, screen_size[1] - apply_btn_size]


apply_pic = pygame.image.load(assets_path + '\\GUI\\vee.png')
apply_pic = pygame.transform.scale(apply_pic, (apply_btn_size, apply_btn_size))
apply_button = Buttons.ButtonImg([screen_size[0] - apply_btn_size, screen_size[0] - apply_btn_size], apply_pic,
                                 apply_auto_buy, listen_disable=False, btn_update_func=update_apply_btn)

# A color for selected ing in auto-buy menu
selected_color = (0, 233, 255)


# Drawing auto-buy menu
def auto_buy_menu(surface, mouse, press):
    exit_menu_button.draw(surface, mouse, press, [0, 0], exit_btn_size)  # Exit button

    # Choose supplier
    cycle_3_right_button.draw(surface, mouse, press, [0, 0], cycle_btn_size)
    cycle_3_left_button.draw(surface, mouse, press, [0, 0], cycle_btn_size)
    supplier = gui_font.render('Current supplier: ', True, (245, 255, 59))
    surface.blit(supplier, (screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 10))
    supplier = gui_font.render(ingredientsAndRecipes.supplier_names[chosen_supplier_index], True, (225, 245, 59))
    surface.blit(supplier, (screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 40))

    # Max price
    max_button.draw(surface, mouse, press, [0, 0], max_btn_size)
    supplier = gui_font.render('Limit: ' + str(max_price_input), True, (245, 255, 59))
    surface.blit(supplier, (screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + cycle_btn_size + 80))

    # Apply button
    apply_button.draw(surface, mouse, press, [0, 0], max_btn_size)

    # Drawing the ing buttons
    for i in range(0, len(ing_buttons)):
        if i is chosen_ing:
            color = selected_color
        else:
            color = (255, 70, 50)
        ingredients_upgrade = gui_font.render(
            'price: ' + str(ingredientsAndRecipes.supplier_prices[chosen_supplier_index][i] * buy_multiplier),
            True, color)
        surface.blit(ingredients_upgrade, (ing_btn_size * 1.2, 120 + (ing_btn_size + ing_btn_spacing) * i))
        ing_buttons_auto_buy[i].draw(surface, mouse, press, [0, 0], ing_btn_size)
        if auto_buy[i] >= 0:
            ing_delete_auto_buy[i].draw(surface, mouse, press, [0, 0], ing_btn_size)


# Shows the auto-buy menu
def show_auto_buy_menu():
    global menu_function
    Buttons.disable_buttons = True
    menu_function = auto_buy_menu


# Auto-buy menu button
settings_btn_size = auto_buy_btn_size = 60


def update_auto_buy_btn():
    return [screen_size[0] - auto_buy_btn_size, 0]


auto_buy_pic = pygame.image.load(assets_path + '\\GUI\\autoBuy.png')
auto_buy_pic = pygame.transform.scale(auto_buy_pic, (auto_buy_btn_size, auto_buy_btn_size))
auto_buy_menu_button = Buttons.ButtonImg([screen_size[0] - auto_buy_btn_size, 0], auto_buy_pic, show_auto_buy_menu,
                                         dead_zones=False, btn_update_func=update_auto_buy_btn)


# Shows the settings menu
def show_settings_menu():
    global menu_function
    Buttons.disable_buttons = True
    menu_function = draw_settings_menu


def update_settings_btn():
    return [screen_size[0] - settings_btn_size - auto_buy_btn_size, 0]


# Settings menu button
settings_pic = pygame.image.load(assets_path + '\\GUI\\settings.png')
settings_pic = pygame.transform.scale(settings_pic, (settings_btn_size, settings_btn_size))
settings_menu_button = Buttons.ButtonImg([screen_size[0] - settings_btn_size - auto_buy_btn_size, 0], settings_pic,
                                         show_settings_menu, dead_zones=False, btn_update_func=update_settings_btn)


# Updates dead areas
def update_dead_area():
    Buttons.dead_areas = []
    Buttons.add_dead_area(screen_size[0] - auto_buy_btn_size - settings_btn_size, 0, screen_size[0],
                          max(auto_buy_btn_size, settings_btn_size))


update_dead_area()  # Sets them on first run


# Applies an auto buy rule
def set_auto_buy(ing_index: int, sup_index: int, max_price: int):
    global auto_buy, stop_auto_buy
    auto_buy[ing_index] = sup_index
    stop_auto_buy[ing_index] = max_price


# GUI colors
money_color = (41, 210, 22)

money_gui = gui_font.render('money:' + str(money), True, money_color)


# Updates the money to be displayed
def update_money():
    global money_gui
    money_gui = gui_font.render('money:' + str(money), True, (41, 210, 22))


# Draws the gui elements
def draw_gui(screen, mouse, press):
    global skip_gui_buttons
    if menu_function is None and not skip_gui_buttons:
        auto_buy_menu_button.draw(screen, mouse, press, [0, 0], auto_buy_btn_size)
        settings_menu_button.draw(screen, mouse, press, [0, 0], auto_buy_btn_size)
    skip_gui_buttons = False
    screen.blit(money_gui, (20, 20))


# Upgrades a restaurant
def upgrade_res():
    global force_update_screen
    active_restaurant.upgrade()
    force_update_screen = True


def restock_menu_res():
    global report_price
    active_restaurant.restock_menu()


def report_menu_res():
    global report_price
    active_restaurant.report_menu()
    report_price = 50 * pow(2, active_restaurant.level)


# Upgrade / buy / sell buttons:
upgrade_btn_size = buy_btn_size = 150


def update_upgrade_btn():
    global buy_upgrade_pos_text
    temp = [int(screen_size[0] * 2 / 3 - (upgrade_btn_size / 2)), screen_size[1] * 0.4]
    buy_upgrade_pos_text = temp[:]
    buy_upgrade_pos_text[1] = buy_upgrade_pos_text[1] + upgrade_btn_size + 10
    return temp


buy_upgrade_pos = [int(screen_size[0] * 2 / 3 - (upgrade_btn_size / 2)), screen_size[1] * 0.4]
buy_upgrade_pos_text = buy_upgrade_pos[:]
buy_upgrade_pos_text[1] = buy_upgrade_pos_text[1] + upgrade_btn_size + 10

upgrade_pic = pygame.image.load(assets_path + '\\GUI\\upgrade.png')
upgrade_pic = pygame.transform.scale(upgrade_pic, (upgrade_btn_size, upgrade_btn_size))
upgrade_menu_button = Buttons.ButtonImg(buy_upgrade_pos, upgrade_pic, upgrade_res, listen_disable=False,
                                        btn_update_func=update_upgrade_btn)

buy_pic = pygame.image.load(assets_path + '\\GUI\\buy.png')
buy_pic = pygame.transform.scale(buy_pic, (buy_btn_size, buy_btn_size))
buy_menu_button = Buttons.ButtonImg(buy_upgrade_pos, buy_pic, upgrade_res, listen_disable=False,
                                    btn_update_func=update_upgrade_btn)


def update_sell_btn():
    return [screen_size[0] - buy_btn_size, screen_size[1] - buy_btn_size]


sell_pic = pygame.image.load(assets_path + '\\GUI\\sell.png')
sell_pic = pygame.transform.scale(sell_pic, (buy_btn_size, buy_btn_size))
sell_menu_button = Buttons.ButtonImg([screen_size[0] - buy_btn_size, screen_size[1] - buy_btn_size], sell_pic, sell_res,
                                     listen_disable=False, btn_update_func=update_sell_btn)

# Restock button
restock_btn_size = 150


def update_restock_btn():
    return [int(screen_size[0] / 3 - (upgrade_btn_size / 2)), screen_size[1] * 0.4]


restock_pic = pygame.image.load(assets_path + '\\GUI\\stock.png')
restock_pic = pygame.transform.scale(restock_pic, (restock_btn_size, restock_btn_size))
restock_menu_button = Buttons.ButtonImg([screen_size[0] * 0.2, screen_size[1] * 0.4], restock_pic, restock_menu_res,
                                        listen_disable=False, btn_update_func=update_restock_btn)

# Report button
report_btn_size = 150


def update_report_btn():
    return [screen_size[0] * 0.5 - report_btn_size / 2, screen_size[1] * 0.7]


report_pic = pygame.image.load(assets_path + '\\GUI\\report.png')
report_pic = pygame.transform.scale(report_pic, (report_btn_size, report_btn_size))
report_menu_button = Buttons.ButtonImg([screen_size[0] * 0.5 - report_btn_size / 2, screen_size[1] * 0.7], report_pic,
                                       report_menu_res, listen_disable=False, btn_update_func=update_report_btn)


# Buy multiplier
def update_buy_multiplier(new_multiplier: int):
    global buy_multiplier
    buy_multiplier = new_multiplier


multiplier_btn_spacing = 20

multiplier_btn_size = 100


def update_multiplier_1_btn():
    return [screen_size[0] - multiplier_btn_size - exit_btn_size - multiplier_btn_spacing, 0]


multiplier_1_pic = pygame.image.load(assets_path + '\\GUI\\multiplier_1.png')
multiplier_1_pic = pygame.transform.scale(multiplier_1_pic, (multiplier_btn_size, multiplier_btn_size))
multiplier_1_button = Buttons.ButtonImg(
    [screen_size[0] - multiplier_btn_size - exit_btn_size - multiplier_btn_spacing, 0],
    multiplier_1_pic, update_buy_multiplier, listen_disable=False,
    parameter_for_function=1, btn_update_func=update_multiplier_1_btn)


def update_multiplier_10_btn():
    return [screen_size[0] - exit_btn_size - ((multiplier_btn_size + multiplier_btn_spacing) * 2), 0]


multiplier_10_pic = pygame.image.load(assets_path + '\\GUI\\multiplier_10.png')
multiplier_10_pic = pygame.transform.scale(multiplier_10_pic, (multiplier_btn_size, multiplier_btn_size))
multiplier_10_button = Buttons.ButtonImg(
    [screen_size[0] - exit_btn_size - ((multiplier_btn_size + multiplier_btn_spacing) * 2), 0], multiplier_10_pic,
    update_buy_multiplier, listen_disable=False, parameter_for_function=10, btn_update_func=update_multiplier_10_btn)


def update_multiplier_100_btn():
    return [screen_size[0] - exit_btn_size - ((multiplier_btn_size + multiplier_btn_spacing) * 3), 0]


multiplier_100_pic = pygame.image.load(assets_path + '\\GUI\\multiplier_100.png')
multiplier_100_pic = pygame.transform.scale(multiplier_100_pic, (multiplier_btn_size, multiplier_btn_size))
multiplier_100_button = Buttons.ButtonImg(
    [screen_size[0] - exit_btn_size - ((multiplier_btn_size + multiplier_btn_spacing) * 3), 0], multiplier_100_pic,
    update_buy_multiplier, listen_disable=False, parameter_for_function=100, btn_update_func=update_multiplier_100_btn)


# Draws the menu... pretty self explanatory
def draw_menu(surface, mouse, press):
    exit_menu_button.draw(surface, mouse, press, [0, 0], exit_btn_size)
    price_upgrade = gui_font.render('Cost: ' + str(int(active_restaurant.price_to_upgrade)), True, (255, 70, 50))
    price_sell = gui_font.render('sell for: ' + str(int(10 * pow(2, active_restaurant.level - 1))), True, (255, 70, 50))
    if active_restaurant.level == 0:
        buy_menu_button.draw(surface, mouse, press, [0, 0], buy_btn_size)
    else:
        upgrade_menu_button.draw(surface, mouse, press, [0, 0], upgrade_btn_size)
        report_menu_button.draw(surface, mouse, press, [0, 0], upgrade_btn_size)
        restock_menu_button.draw(surface, mouse, press, [0, 0], restock_btn_size)
        sell_menu_button.draw(surface, mouse, press, [0, 0], restock_btn_size)
        surface.blit(price_sell, [screen_size[0] - buy_btn_size, screen_size[1] - buy_btn_size * 1.2])
    surface.blit(price_upgrade, buy_upgrade_pos_text)


# Draws the settings menu
def draw_settings_menu(surface, mouse, press):
    exit_menu_button.draw(surface, mouse, press, [0, 0], exit_btn_size)
    _text = gui_font.render('Change zoom:', True, (245, 255, 59))
    surface.blit(_text, (screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 10))
    cycle_4_left_button.draw(surface, mouse, press, [0, 0], exit_btn_size)
    cycle_4_right_button.draw(surface, mouse, press, [0, 0], exit_btn_size)


# Updates the report
def update_report():
    global money, report_price
    if money >= report_price:
        money -= report_price
        active_restaurant.update_report()


def update_create_report_btn():
    return [screen_size[0] * 0.5 - report_btn_size / 2, exit_btn_size]


create_report_btn = Buttons.ButtonImg([screen_size[0] * 0.5 - report_btn_size / 2, exit_btn_size], report_pic,
                                      update_report, listen_disable=False, btn_update_func=update_create_report_btn)

report_spacing = 40
report_stats_color = (104, 145, 27)


# Drawing the report menu
def draw_report_menu(surface, mouse, press):
    exit_menu_button.draw(surface, mouse, press, [0, 0], exit_btn_size)  # Exit button

    create_report_btn.draw(surface, mouse, press, [0, 0], report_btn_size)  # Create report button

    # Price of issuing a report
    report_price_text = gui_font.render('Cost: ' + str(report_price), True, (255, 70, 50))
    surface.blit(report_price_text,
                 (int(screen_size[0] / 2 - report_price_text.get_width() / 2), exit_btn_size + report_btn_size))

    # Showing the report details
    report_text = gui_font.render('Restaurant level: ' + str(active_restaurant.report.level), True, report_stats_color)
    surface.blit(report_text, (50, exit_btn_size + report_btn_size + 10 + report_spacing))

    report_text = gui_font.render('Maximum demand: ' + str(active_restaurant.report.potential_demand), True,
                                  report_stats_color)
    surface.blit(report_text, (50, exit_btn_size + report_btn_size + 10 + 2 * report_spacing))

    report_text = gui_font.render('Current demand: ' + str(active_restaurant.report.current_demand), True,
                                  report_stats_color)
    surface.blit(report_text, (50, exit_btn_size + report_btn_size + 10 + 3 * report_spacing))

    for index in range(0, ingredientsAndRecipes.meal_count):
        formatted_float = "{:.3f}".format(active_restaurant.report.demand_weights[index])
        report_text = gui_font.render(str(ingredientsAndRecipes.meal_list[index]) + "  -  Revenue: " + str(
            active_restaurant.report.meal_revenues[index]) + ", Weight: " + formatted_float, True, report_stats_color)
        surface.blit(report_text, (50, exit_btn_size + report_btn_size + 10 + report_spacing * (index + 4)))


# Drawing the restock menu
def draw_restock_menu(surface, mouse, press):
    exit_menu_button.draw(surface, mouse, press, [0, 0], exit_btn_size)  # Exit menu

    multiplier_1_button.draw(surface, mouse, press, [0, 0], multiplier_btn_size)
    multiplier_10_button.draw(surface, mouse, press, [0, 0], multiplier_btn_size)
    multiplier_100_button.draw(surface, mouse, press, [0, 0], multiplier_btn_size)
    multiplier = gui_font.render(
        'Buy multiplier: ' + str(10 * buy_multiplier), True, (120, 0, 128))
    surface.blit(multiplier, (20, 50))

    # Supplier selection
    cycle_right_button.draw(surface, mouse, press, [0, 0], cycle_btn_size)
    cycle_left_button.draw(surface, mouse, press, [0, 0], cycle_btn_size)
    supplier = gui_font.render('Current supplier: ', True, (245, 255, 59))
    surface.blit(supplier, (screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 10))
    supplier = gui_font.render(ingredientsAndRecipes.supplier_names[active_restaurant.supplier], True, (225, 245, 59))
    surface.blit(supplier, (screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + 40))

    # Recipe selection
    recipe_text = gui_font.render(
        'recipe: ' + ingredientsAndRecipes.meal_list[active_restaurant.activeRecipe.meal_index],
        True, (43, 196, 176))
    surface.blit(recipe_text, (screen_size[0] - 20 - 2 * cycle_btn_size, exit_btn_size + cycle_btn_size + 80))
    cycle_2_right_button.draw(surface, mouse, press, [0, 0], cycle_btn_size)
    cycle_2_left_button.draw(surface, mouse, press, [0, 0], cycle_btn_size)

    for i in range(0, len(ing_buttons)):
        ingredients_upgrade = gui_font.render('in stock: ' + str(active_restaurant.ingredients_array[i]), True,
                                              (255, 70, 50))
        surface.blit(ingredients_upgrade, (ing_btn_size * 1.2, 100 + (ing_btn_size + ing_btn_spacing) * i))
        ingredients_upgrade = gui_font.render(
            'price: ' + str(ingredientsAndRecipes.supplier_prices[active_restaurant.supplier][i] * buy_multiplier),
            True, (255, 70, 50))
        surface.blit(ingredients_upgrade, (ing_btn_size * 1.2, 120 + (ing_btn_size + ing_btn_spacing) * i))
        ing_buttons[i].draw(surface, mouse, press, [0, 0], ing_btn_size)


# Checks and expends limits
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


class ResReport:
    def __init__(self):
        self.level = 0
        self.potential_demand = 0
        self.current_demand = 0
        self.demand_weights = [0] * ingredientsAndRecipes.meal_count
        self.meal_revenues = [0] * ingredientsAndRecipes.meal_count

    def update_report(self, lvl, pot_demand, cur_demand, weights):
        self.level = lvl
        self.potential_demand = pot_demand
        self.current_demand = cur_demand
        self.demand_weights = weights[:]
        self.meal_revenues = ingredientsAndRecipes.meal_revenue[:]


# The tile class, the base of the map, every type of tile has its own class from here on out
class Tile:
    type = ''
    texture = None
    btn = None

    def __init__(self, x: int, y: int):
        global tile_size
        self.grid_location = [x, y]
        self.set_location(x * tile_size, y * tile_size)
        self.pos = [x, y]

    def set_location(self, x: int, y: int):
        self.grid_location = [x, y]

    def set_texture(self, path: str):
        self.texture = path

    def set_type(self, _type: str):
        self.type = _type

    def draw(self, surface, mouse, press, offset):
        self.btn.draw(surface, mouse, press, offset, tile_size)

    def show_menu(self):
        pass

    def update_tile(self):
        pass


class RoadTile(Tile):

    def __init__(self, x: int, y: int, orientation: str = None, texture: str = None):
        super().__init__(x, y)
        global tile_size
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
        picture = pygame.transform.scale(picture, (tile_size, tile_size))
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

    def __init__(self, x: int, y: int, texture: str = '1'):
        super().__init__(x, y)
        global tile_size
        self.set_type('restaurant')
        self.set_texture(assets_path + '\\Resturants\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (tile_size, tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, self.show_menu)
        self.max_costumers = 0
        self.level = 0
        self.space = 0
        self.demand = 5
        self.costumers = 0
        res_list.append(self)
        self.price_to_upgrade = 30 * pow(2, self.level)
        self.ingredients_array = [50] * ingredientsAndRecipes.num_of_ingredients
        self.activeRecipe = ingredientsAndRecipes.recipes[ingredientsAndRecipes.meal_dic["burger"]]
        self.supplier = 0
        self.report = ResReport()
        self.demand_weights = [random.uniform(min_demand_weight, max_demand_weight) for i in
                               range(0, ingredientsAndRecipes.meal_count)]
        self.costumer_variance = 1
        self.variance_timer = 60

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data

    def show_menu(self):
        global menu_function, active_restaurant
        menu_function = draw_menu
        Buttons.disable_buttons = True
        active_restaurant = self

    def sell(self):
        global money
        res_list.remove(self)
        money += 10 * pow(2, self.level - 1)
        self.max_costumers = 0
        self.level = 0
        self.space = 0
        self.demand = 5
        self.costumers = 0
        res_list.append(self)
        self.price_to_upgrade = 30 * pow(2, self.level)
        self.ingredients_array = [50] * ingredientsAndRecipes.num_of_ingredients
        self.activeRecipe = ingredientsAndRecipes.recipes[ingredientsAndRecipes.meal_dic["burger"]]
        self.supplier = 0
        self.report = ResReport()
        self.demand_weights = [random.uniform(min_demand_weight, max_demand_weight) for i in
                               range(0, ingredientsAndRecipes.meal_count)] * ingredientsAndRecipes.meal_count
        self.costumer_variance = 1
        self.variance_timer = 60

    def update_report(self):
        self.report.update_report(self.level, self.demand, self.costumers, self.demand_weights)

    def get_income(self):
        global money
        self.variance_timer -= 1
        if self.variance_timer == 0:
            self.variance_timer = 60
            self.costumer_variance = random.uniform(0.8, 1.2)
            self.calc_costumers()
        if money >= 0:
            for i in range(0, ingredientsAndRecipes.num_of_ingredients):
                desired_amount = self.activeRecipe.ing_list[i] * self.costumers
                if desired_amount > 0 and auto_buy[i] != -1 and ingredientsAndRecipes.supplier_prices[auto_buy[i]][i] < \
                        stop_auto_buy[i]:
                    difference = self.ingredients_array[i] - desired_amount
                    if difference < 0:
                        self.ingredients_array[i] -= difference
                        money = int(money - ingredientsAndRecipes.supplier_prices[auto_buy[i]][i] * (-difference / 10))
        return self.activeRecipe.use_ing(self.ingredients_array,
                                         int(self.costumers * self.demand_weights[self.activeRecipe.meal_index]))

    def check_demand(self):
        _demand = 5
        if self.pos[0] / 5 < 0:
            offset_x = -1
        else:
            offset_x = 0
        if self.pos[1] / 5 < 0:
            offset_y = -1
        else:
            offset_y = 0
        for i in range(-2, 3):
            for j in range(-2, 3):
                try:
                    _demand += chunk_map[int(self.pos[0] / 5) - chunk_map_x_bounds[0] + offset_x + i][
                        int(self.pos[1] / 5) - chunk_map_y_bounds[0] + offset_y + j][2][2].get_pop()
                except:
                    pass
        self.demand = int(_demand * self.costumer_variance)

    def calc_costumers(self):
        if self.demand < self.max_costumers:
            self.costumers = int(self.demand * self.costumer_variance)
        else:
            self.costumers = int(self.max_costumers * self.costumer_variance)

    def upgrade(self):
        global money
        if money >= self.price_to_upgrade:
            money -= self.price_to_upgrade
            self.max_costumers = int(self.max_costumers * 1.2 + 5)
            self.space = self.space * 2 + 1
            self.level += 1
            self.price_to_upgrade = 10 * self.level * pow(2, self.level)
            self.calc_costumers()

    def update_tile(self):
        self.check_demand()
        self.calc_costumers()

    def restock_menu(self):
        global menu_function, active_restaurant
        menu_function = draw_restock_menu
        Buttons.disable_buttons = True
        active_restaurant = self

    def report_menu(self):
        global menu_function, active_restaurant
        menu_function = draw_report_menu
        Buttons.disable_buttons = True
        active_restaurant = self

    def restock_item(self, index):
        global money, buy_multiplier
        if money > ingredientsAndRecipes.supplier_prices[self.supplier][index]:
            self.ingredients_array[index] += buy_multiplier * 10
            money = money - ingredientsAndRecipes.supplier_prices[self.supplier][index] * buy_multiplier


class ParkingTile(Tile):

    def __init__(self, x: int, y: int, texture: str = '1'):
        super().__init__(x, y)
        global tile_size
        self.set_type('parking')
        self.set_texture(assets_path + '\\Parking\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (tile_size, tile_size))
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

    def __init__(self, x: int, y: int, texture: str = '1'):
        super().__init__(x, y)
        global tile_size
        self.set_type('park')
        self.population = 0
        self.set_texture(assets_path + '\\Parks\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (tile_size, tile_size))
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

    def __init__(self, x: int, y: int, population: int, texture: str = '1'):
        super().__init__(x, y)
        global tile_size
        self.set_type('house')
        self.population = population
        self.set_texture(assets_path + '\\Houses\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (tile_size, tile_size))
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

    def __init__(self, x: int, y: int, texture: str = '1'):
        super().__init__(x, y)
        global tile_size
        self.set_type('empty')
        self.set_texture(assets_path + '\\Empty\\' + texture)
        picture = pygame.image.load(self.texture + '.png')
        picture = pygame.transform.scale(picture, (tile_size, tile_size))
        self.btn = Buttons.ButtonImg(self.grid_location[:], picture, self.show_menu)

    def json_ready(self):
        data = {
            'type': self.type,
            'x': self.grid_location[0],
            'y': self.grid_location[1],
            'texture': self.texture
        }
        return data
