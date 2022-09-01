import pygame
import ingredientsAndRecipes

pygame.init()

assets_path = 'Assets'
screen_size = [750, 750]

screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

# 0 - Close btn, 1 - cancel btn, 2 - right, 3 - left, 4 - max, 5 - apply, 6 - auto buy, 7 - buy, 8 - settings,
# 9 - upgrade, 10 - buy, 11 - sell, 12 - restock, 13 - report, 14 - multi 1, 15 - multi 10, 16 - multi 100,
# 17 - road center, 18 - road hor, 19 - road ver, 20 - res 1, 21 - parking 1, 22 - park, 23 - house 1, 24 - house 2,
# 25 - house 3, 26 - empty

original_images = [
    pygame.image.load(assets_path + '\\GUI\\close.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\close.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\right.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\left.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\max.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\vee.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\autoBuy.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\buy.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\settings.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\upgrade.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\buy.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\sell.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\stock.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\report.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\multiplier_1.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\multiplier_10.png').convert(),
    pygame.image.load(assets_path + '\\GUI\\multiplier_100.png').convert(),
    pygame.image.load(assets_path + '\\Roads\\center.png').convert(),
    pygame.image.load(assets_path + '\\Roads\\horizontal.png').convert(),
    pygame.image.load(assets_path + '\\Roads\\vertical.png').convert(),
    pygame.image.load(assets_path + '\\Resturants\\1.png').convert(),
    pygame.image.load(assets_path + '\\Parking\\1.png').convert(),
    pygame.image.load(assets_path + '\\Parks\\1.png').convert(),
    pygame.image.load(assets_path + '\\Houses\\1.png').convert(),
    pygame.image.load(assets_path + '\\Houses\\2.png').convert(),
    pygame.image.load(assets_path + '\\Houses\\3.png').convert(),
    pygame.image.load(assets_path + '\\Empty\\1.png').convert(),

]

constant_img_list_size = len(original_images)

ing_imgs = [pygame.image.load(assets_path + '\\ingredients\\' + ingredientsAndRecipes.ing_list[i] + '.png') for i in
            range(0, ingredientsAndRecipes.num_of_ingredients)]

original_images = original_images + ing_imgs

exit_btn_size = 100
ing_btn_size = int(((screen_size[1] - 200) / ingredientsAndRecipes.num_of_ingredients) * 3 / 4)
cycle_btn_size = 100
max_btn_size = 100
apply_btn_size = 100
gui_btn_size = 60
buy_btn_size = 150
restock_btn_size = 150
report_btn_size = 150
multiplier_btn_size = 100
tiles_on_screen = 8
tile_size = int(screen_size[0] / tiles_on_screen)

image_size = [
    (exit_btn_size, exit_btn_size),
    (ing_btn_size, ing_btn_size),
    (cycle_btn_size, cycle_btn_size),
    (cycle_btn_size, cycle_btn_size),
    (max_btn_size, max_btn_size),
    (apply_btn_size, apply_btn_size),
    (gui_btn_size, gui_btn_size),
    (gui_btn_size, gui_btn_size),
    (gui_btn_size, gui_btn_size),
    (buy_btn_size, buy_btn_size),
    (buy_btn_size, buy_btn_size),
    (buy_btn_size, buy_btn_size),
    (restock_btn_size, restock_btn_size),
    (report_btn_size, report_btn_size),
    (multiplier_btn_size, multiplier_btn_size),
    (multiplier_btn_size, multiplier_btn_size),
    (multiplier_btn_size, multiplier_btn_size),
    (tile_size, tile_size),
    (tile_size, tile_size),
    (tile_size, tile_size),
    (tile_size, tile_size),
    (tile_size, tile_size),
    (tile_size, tile_size),
    (tile_size, tile_size),
    (tile_size, tile_size),
    (tile_size, tile_size),
    (tile_size, tile_size),

]

ing_sizes = [(ing_btn_size, ing_btn_size) for i in range(0, ingredientsAndRecipes.num_of_ingredients)]

image_size = image_size + ing_sizes

images = original_images[:]


def update_img_size(img_id, new_x, new_y):
    image_size[img_id] = (new_x, new_y)
    images[img_id] = pygame.transform.scale(original_images[img_id], (new_x, new_y))


def update_all_imgs():
    for i in range(0, len(original_images)):
        update_img_size(i, image_size[i][0], image_size[i][1])


update_all_imgs()

# If True - buttons with listen_disable property won't check hover and click
disable_buttons = False

# Locations when hover and click checks should not work
dead_areas = []

# If True buttons with btn_update_func property not None would update their location
update_location = False

# True if tile_size changed
update_size = False
t_size = 0


# Adds a dead area - location when button checks won't apply, unless that button ignores dead areas
def add_dead_area(x1, y1, x2, y2):
    dead_areas.append([x1, y1, x2, y2])


# A function to draw translucent rectangles
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


# A function to add a button
def add_button(btn_list: [], _location: [int, int, int, int], _text, _default_color, _hover_color, on_press):
    new_btn = Button(_location, _text, _default_color, _hover_color, on_press)
    btn_list.append(new_btn)


# The base button class
class Button:
    location = [0, 0, 0, 0]
    location_2 = [0, 0, 0, 0]
    text = None
    default_color = None
    hover_color = None
    active_color = None
    hover = False
    func_press = None
    text_pos_x = 0
    text_pos_y = 0

    def __init__(self, _location: [int, int, int, int], _text, _default_color, _hover_color, on_press,
                 listen_disable=True):
        self.location = _location[:]
        self.listen = listen_disable
        _location[2] = _location[2] - _location[0]
        _location[3] = _location[3] - _location[1]
        self.location_2 = _location[:]
        self.text = _text
        self.default_color = self.active_color = _default_color
        self.hover_color = _hover_color
        self.func_press = on_press
        self.text_pos_x = (((self.location[2] - self.location[0]) - self.text.get_width()) / 2) + self.location[0]
        self.text_pos_y = (((self.location[3] - self.location[1]) - self.text.get_height()) / 2) + self.location[1]

    def check_hover(self, mouse_location: [int, int]):
        if self.listen and disable_buttons:
            self.hover = False
            return
        for area in dead_areas:
            if area[0] <= mouse_location[0] <= area[2] and area[1] <= mouse_location[1] <= area[3]:
                self.hover = False
                return
        if self.location[0] <= mouse_location[0] <= self.location[2] and \
                self.location[1] <= mouse_location[1] <= self.location[3]:
            self.active_color = self.hover_color
            self.hover = True
        else:
            self.active_color = self.default_color
            self.hover = False

    def get_pos(self):
        return self.location

    def get_text(self):
        return self.text

    def get_hover(self):
        return self.hover

    def press(self):
        self.func_press()

    def draw(self, screen):
        pygame.draw.rect(screen, self.active_color, self.location_2)
        screen.blit(self.text, (self.text_pos_x, self.text_pos_y))


# A button made out of an image
class ButtonImg:
    location = [0, 0]
    location_2 = [0, 0]
    size = 200
    hover = False
    func_press = None
    disable = False

    def __init__(self, _location: [int, int], _img_id: int, on_press, listen_disable=True, parameter_for_function=None,
                 dead_zones=True, btn_update_func=None, parameter_for_update=None):
        self.dead_zones = dead_zones
        self.listen = listen_disable
        self.set_pos(_location)
        self.img_id = _img_id
        self.func_press = on_press
        self.parameter_for_function = parameter_for_function
        self.update_func = btn_update_func
        self.parameter_for_update = parameter_for_update

    def set_pos(self, _location: [int, int]):
        if not self.dead_zones or not self.listen:
            self.location = self.location_2 = _location[:]
        else:
            self.location = self.location_2 = [_location[0] / t_size, _location[1] / t_size][:]

    def check_hover(self, mouse_location: [int, int], press, size):
        if (self.listen and disable_buttons) or self.disable:
            self.hover = False
            return
        if self.dead_zones:
            for area in dead_areas:
                if area[0] <= mouse_location[0] <= area[2] and area[1] <= mouse_location[1] <= area[3]:
                    self.hover = False
                    return
        if self.location_2[0] <= mouse_location[0] <= self.location_2[0] + size and \
                self.location_2[1] <= mouse_location[1] <= self.location_2[1] + size:
            self.hover = True
            if press:
                self.press()
        else:
            self.hover = False

    def get_pos(self):
        return self.location

    def get_hover(self):
        return self.hover

    def press(self):
        if self.parameter_for_function is not None:
            self.func_press(self.parameter_for_function)
        else:
            self.func_press()

    def draw(self, screen, mouse, press, offset, size):
        if update_location and self.update_func is not None:
            if self.parameter_for_update is None:
                self.set_pos(self.update_func())
            else:
                self.set_pos(self.update_func(self.parameter_for_update))
        if update_size:
            update_img_size(self.img_id, size, size)
        if self.dead_zones and self.listen:
            self.location = [self.location[0] * size, self.location[1] * size]
        self.location_2 = [self.location[0] + offset[0], self.location[1] + offset[1]]
        self.check_hover(mouse, press, size)
        screen.blit(images[self.img_id], (self.location[0] + offset[0], self.location[1] + offset[1]))
        if self.hover:
            if self.location_2[0] < 0:
                self.location_2[0] = 0
            if self.location_2[1] < 0:
                self.location_2[1] = 0
            draw_rect_alpha(screen, (125, 125, 125, 160), (self.location_2[0], self.location_2[1], size, size))
        if self.dead_zones and self.listen:
            self.location = [self.location[0] / size, self.location[1] / size]
