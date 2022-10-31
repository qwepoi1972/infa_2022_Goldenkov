import pygame
from pygame.draw import *
from random import randint, random
import time
from numpy import sqrt
pygame.init()

FPS = 60
delta = 0.35  # Время между появлениями шаров(чтобы появление не зависило от частоты кадров)
screen = pygame.display.set_mode((1200, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

coord_balls = []  # Массив координат шаров, хранит массивы ([x, y, r, color], [a_x, a_y]), a - вектор движения
coord_polygons = []  # Массив координат прямоугольников, ([x, y, r_x, r_y, color], [a_x, a_y]), a - вектор движения


def new_ball():
    """
    Создаёт новый шарик и его вектор и добавляет их в coord_balls
    """
    global coord_balls
    r = randint(25, 75)
    x = randint(r, 1200-r)
    y = randint(r, 800-r)
    color = COLORS[randint(0, 5)]

    a_x = 2*random() - 1  # Координаты вектора лежат в полуинтервалах [-1, 1), тогда скорость всех шаров одинакова)
    a_y = sqrt(1 - a_x**2) * (-1)**(randint(0, 1))
    a = [a_x, a_y]

    coord_balls.append(([x, y, r, color], a))


def new_polygon():
    """
    Создаёт новый квадрат и его вектор и добавляет их в coord_polygons
    """
    global coord_polygons
    r_x = randint(30, 60)
    r_y = randint(30, 60)
    x = randint(r_x, 1200-r_x)
    y = randint(r_y, 800-r_y)
    color = COLORS[randint(0, 5)]

    a_x = 2*random() - 1  # Координаты вектора лежат в полуинтервалах [-1, 1), тогда скорость всех шаров одинакова)
    a_y = sqrt(1 - a_x**2) * (-1)**(randint(0, 1))
    a = [5*a_x, 5*a_y]

    coord_polygons.append(([x, y, r_x, r_y, color], a))


def click(event):
    """
    Проверка попадания в фигуру
    """
    global coord_balls, score
    x_pos, y_pos = event.pos
    for i in coord_balls:
        if (x_pos-i[0][0])**2+(y_pos-i[0][1])**2 <= i[0][2]**2:
            coord_balls.remove(i)
            score += 10
            print("Попадание!")
            print("Ваш счёт: ", score)
    for i in coord_polygons:
        if 0 <= (x_pos-i[0][0]) <= i[0][2] and 0 <= (y_pos-i[0][1]) <= i[0][3]:
            coord_polygons.remove(i)
            score += 50
            print("Попадание!")
            print("Ваш счёт: ", score)


def draw_balls():
    """
    Отрисовка шаров, проверка коллизии со стенами и перемещение
    """
    global coord_balls

    for coord, a in coord_balls:
        if coord[0] - coord[2] <= abs(a[0]) or coord[0] + coord[2] >= 1200 - a[0]:
            a[0] *= -1
        elif coord[1] - coord[2] <= abs(a[1]) or coord[1] + coord[2] >= 800 - a[1]:
            a[1] *= -1

        coord[0] += a[0]
        coord[1] += a[1]
        circle(screen, coord[3], (coord[0], coord[1]), coord[2])
        circle(screen, BLACK, (coord[0], coord[1]), coord[2], 1)


def draw_polygons():
    """
    Отрисовка полигонов, проверка коллизии со стенами и перемещение
    """
    for coord, a in coord_polygons:
        if coord[0] <= abs(a[0]) or coord[0] + coord[2] >= 1200 - a[0]:
            a[0] *= -1
        elif coord[1] <= abs(a[1]) or coord[1] + coord[3] >= 800 - a[1]:
            a[1] *= -1

        coord[0] += a[0]
        coord[1] += a[1]
        polygon(screen, coord[4], [(coord[0], coord[1]), (coord[0]+coord[2], coord[1]),
                                   (coord[0]+coord[2], coord[1]+coord[3]), (coord[0], coord[1]+coord[3])])
        polygon(screen, BLACK, [(coord[0], coord[1]), (coord[0] + coord[2], coord[1]),
                                (coord[0] + coord[2], coord[1] + coord[3]), (coord[0], coord[1] + coord[3])], 2)


score = 0
clock = pygame.time.Clock()
finished = False
tm1 = 0
tm2 = time.time()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    if time.time() - tm1 >= delta and len(coord_balls) + len(coord_polygons) <= 20:
        tm1 = time.time()
        new_ball()
    if time.time() - tm2 >= 8*delta and len(coord_balls) + len(coord_polygons) <= 20:
        tm2 = time.time()
        new_polygon()
    screen.fill(BLACK)
    draw_balls()
    draw_polygons()
    pygame.display.update()


pygame.quit()
