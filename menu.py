import pygame
import pickle
import sys
import Buttons

pygame.init()

exit_menu = False

choose_save = False

value_to_return = -1  # -1 means a new game, every other value means the selected game to load

pic = None

num_saves = 0


def existing_game():
    global choose_save, value_to_return, num_saves, pic
    if num_saves == 0:
        return_to_game()
    else:
        value_to_return = 0
        choose_save = True


# Returns to main
def return_to_game():
    global exit_menu
    exit_menu = True


# Showing the main menu
def show_menu(num_of_saves, screen=pygame.display.set_mode((1500, 800), pygame.RESIZABLE)):
    global exit_menu, value_to_return, num_saves, pic
    num_saves = num_of_saves
    width = screen.get_width()
    height = screen.get_height()

    # Selecting a font and colors
    smallfont = pygame.font.SysFont('Narkisim', 35)

    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

    # Rendering texts
    text_quit = smallfont.render('Quit', True, (255, 255, 255))
    text_saved_game = smallfont.render('Load existing game', True, (255, 255, 255))
    text_new_game = smallfont.render('Create a new save', True, (255, 255, 255))
    text_select_game = smallfont.render('Use arrows and press enter to select file...', True, (0, 0, 0))

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

    if num_saves > 0:
        pic = pygame.image.load('Saves\\0screenshot.jpg')
        pic = pygame.transform.scale(pic, (int(screen.get_width() * 0.85), int(screen.get_height() * 0.85)))
        with open('Saves\\0', "rb") as fp:  # Unpickling
            data = pickle.load(fp)
            last_played = data[7]
        text_game_time = smallfont.render('Last played: ' + last_played, True, (0, 0, 0))

    # Displays the menu until closing
    while not exit_menu:
        # Clears the screen
        screen.fill((255, 198, 41))

        # Updates the mouse position
        mouse = pygame.mouse.get_pos()

        # Handling pygame events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.get_hover():
                        btn.press()

            if choose_save and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    value_to_return = value_to_return + 1
                    if value_to_return == num_of_saves:
                        value_to_return = 0

                if ev.key == pygame.K_LEFT:
                    value_to_return = value_to_return - 1
                    if value_to_return == -1:
                        value_to_return = num_of_saves - 1

                if ev.key == pygame.K_RETURN:
                    return_to_game()

                pic = pygame.image.load('Saves\\' + str(value_to_return) + 'screenshot.jpg')
                pic = pygame.transform.scale(pic, (int(width * 0.85), int(height * 0.85)))

                with open('Saves\\' + str(value_to_return), "rb") as fp:  # Unpickling
                    data = pickle.load(fp)
                    last_played = data[7]
                text_game_time = smallfont.render('Last played: ' + last_played, True, (0, 0, 0))

        if not choose_save:
            # Checking hover and drawing all the buttons
            for btn in buttons:
                btn.check_hover(mouse)
                btn.draw(screen)
        else:
            # Select file
            screen.blit(text_select_game, (10, 10))
            screen.blit(text_game_time, (10, height - 10 - text_select_game.get_height()))
            screen.blit(pic, (int((width * 0.15) / 2), int((height * 0.15) / 2)))

        pygame.display.update()
    return value_to_return
