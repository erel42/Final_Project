import pygame
import sys
import Buttons

pygame.init()

exit_menu = False

value_to_return = -1  # -1 means a new game, every other value means the selected game to load


def existing_game():
    global value_to_return
    value_to_return = 0
    return_to_game()


# Returns to main
def return_to_game():
    global exit_menu
    exit_menu = True


# Showing the main menu
def show_menu(screen=pygame.display.set_mode((1500, 800), pygame.RESIZABLE)):
    global exit_menu, value_to_return
    width = screen.get_width()
    height = screen.get_height()

    # Selecting a font and colors
    smallfont = pygame.font.SysFont('Narkisim', 35)

    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

    # Rendering texts
    text_quit = smallfont.render('quit', True, (255, 255, 255))
    text_saved_game = smallfont.render('load existing game', True, (255, 255, 255))
    text_new_game = smallfont.render('create new save', True, (255, 255, 255))

    # Creating buttons
    buttons = []

    # New game button
    Buttons.add_button(buttons, [width - 400, round(height / 3) - 200, width - 25, round(height / 3) - 150],
                       text_new_game, color_dark, color_light, return_to_game)

    # Play from save button
    Buttons.add_button(buttons, [width - 400, round(height / 3) - 100, width - 25, round(height / 3) - 50],
                       text_saved_game, color_dark, color_light, existing_game)

    # Quit button
    Buttons.add_button(buttons, [width - 400, round(height / 3), width - 25, round(height / 3) + 50], text_quit,
                       color_dark, color_light, sys.exit)

    # Displays the menu until closing
    while not exit_menu:
        # Clears the screen
        screen.fill((255, 198, 41))

        # Updates the mouse position
        mouse = pygame.mouse.get_pos()

        # Checking hover and drawing all the buttons
        for btn in buttons:
            btn.check_hover(mouse)
            btn.draw(screen)

        # Handling pygame events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.get_hover():
                        btn.press()

        pygame.display.update()
    return value_to_return
