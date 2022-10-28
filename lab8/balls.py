import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 2
screen = pygame.display.set_mode((1200, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """
    рисует новый шарик
    """
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 800)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def click(event):
    """
    Проверка попадания в шарик
    """
    global score
    x_pos, y_pos = event.pos
    if (x_pos-x)**2+(y_pos-y)**2 <= r**2:
        score += 10
        print("Попал!")
        print("Ваш счёт: ", score)


score = 0
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
