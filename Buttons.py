import pygame


def add_button(btn_list: [], _location: [int, int, int, int], _text, _default_color, _hover_color, on_press):
    new_btn = Button(_location, _text, _default_color, _hover_color, on_press)
    btn_list.append(new_btn)


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

    def __init__(self, _location: [int, int, int, int], _text, _default_color, _hover_color, on_press):
        self.location = _location[:]
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
