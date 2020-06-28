from time import sleep
import pygame

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


MARGIN = 50
BORDER = 5
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 250

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
logging.debug("screen created")


font = pygame.font.SysFont(None, 24)

game_over = font.render('GAME OVER!', True, pygame.Color("RED"))

game_over_height = game_over.get_height()
game_over_width = game_over.get_width()

# Work out where to put the text
# I want the centre point of the font in the centre of the screen
screen.blit(
    game_over,
    (
        (SCREEN_WIDTH/2 - game_over_width/2),
        (SCREEN_HEIGHT/2) - (game_over_height/2)
    )
)
pygame.display.update()
sleep(1)

border = 5

box_width = game_over_width+MARGIN
box_height = game_over_height+MARGIN
game_over_rect = pygame.Rect(
        ((SCREEN_WIDTH/2 - box_width/2),
        (SCREEN_HEIGHT/2) - (box_height/2)),
        (box_width, box_height)
    )

pygame.draw.rect(
    screen,
    pygame.Color("White"),
    game_over_rect,
    border)

pygame.display.update()

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break