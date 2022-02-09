import pygame
import sys
import Buttons

pygame.init()
screen = pygame.display.set_mode((1500, 800))

width = screen.get_width()
height = screen.get_height()

smallfont = pygame.font.SysFont('Corbel', 35)

color_light = (170, 170, 170)

color_dark = (100, 100, 100)

mouse = [0, 0]

text = smallfont.render('quit', True, (255, 255, 255))

buttons = [Buttons.Button([width / 2, height / 2, (width / 2) + 140, (height / 2) + 40], text, color_dark, color_light,
                          pygame.quit)]

while True:
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

    # screen.blit(text, (width / 2 + 50, height / 2))

    pygame.display.update()
