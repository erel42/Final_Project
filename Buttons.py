import pygame

pygame.init()

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
    default_img = None
    hover_img = None
    active_img = None
    hover = False
    func_press = None
    disable = False

    def __init__(self, _location: [int, int], _default_img, on_press, listen_disable=True, parameter_for_function=None,
                 dead_zones=True, btn_update_func=None, parameter_for_update=None):
        self.dead_zones = dead_zones
        self.listen = listen_disable
        self.set_pos(_location)
        self.default_img = self.original_image = _default_img
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
            self.default_img = pygame.transform.scale(self.original_image, (size, size))
        if self.dead_zones and self.listen:
            self.location = [self.location[0] * size, self.location[1] * size]
        self.location_2 = [self.location[0] + offset[0], self.location[1] + offset[1]]
        self.check_hover(mouse, press, size)
        screen.blit(self.default_img, (self.location[0] + offset[0], self.location[1] + offset[1]))
        if self.hover:
            if self.location_2[0] < 0:
                self.location_2[0] = 0
            if self.location_2[1] < 0:
                self.location_2[1] = 0
            draw_rect_alpha(screen, (125, 125, 125, 160), (self.location_2[0], self.location_2[1], size, size))
        if self.dead_zones and self.listen:
            self.location = [self.location[0] / size, self.location[1] / size]
