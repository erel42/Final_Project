import pygame
import sys
import Buttons

pygame.init()

exit_menu = False


def existing_game():
    print('need to implement')


def new_game():
    print('need to implement')


def return_to_game():
    global exit_menu
    exit_menu = True


def show_menu(screen=pygame.display.set_mode((1500, 800))):
    global exit_menu
    width = screen.get_width()
    height = screen.get_height()

    smallfont = pygame.font.SysFont('Narkisim', 35)

    color_light = (170, 170, 170)

    color_dark = (100, 100, 100)

    mouse = [0, 0]

    text_quit = smallfont.render('quit', True, (255, 255, 255))
    text_saved_game = smallfont.render('load existing game', True, (255, 255, 255))
    text_new_game = smallfont.render('create new save', True, (255, 255, 255))

    buttons = []

    # new game button
    Buttons.add_button(buttons, [width - 400, round(height / 3) - 200, width - 25, round(height / 3) - 150],
                       text_new_game, color_dark, color_light, return_to_game)

    # play from save button
    Buttons.add_button(buttons, [width - 400, round(height / 3) - 100, width - 25, round(height / 3) - 50],
                       text_saved_game, color_dark, color_light, existing_game)

    # quit button
    Buttons.add_button(buttons, [width - 400, round(height / 3), width - 25, round(height / 3) + 50], text_quit,
                       color_dark, color_light, sys.exit)

    while not exit_menu:
        screen.fill((255, 198, 41))
        mouse = pygame.mouse.get_pos()

        for btn in buttons:
            btn.check_hover(mouse)
            btn.draw(screen)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.get_hover():
                        btn.press()

        pygame.display.update()
