import numpy as np
import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

screen.fill((250, 250, 250))


def rotated(color, x1, y1, a, b, angle):
    """
    Cтроит повёрнутый прямоугольник.
    color - цвет прямоугольника
    a, b - стороны прямоугольника
    angle - угол поворота (отсчитывается от горизонтали по часовой стрелке)
    x1, y1 - координаты вершины (левая верхняя вершина при angle = 0),
    относительно которой происходит вращение
    """
    an = np.pi * angle / 180

    x2 = x1 - a * np.sin(an)
    x3 = x2 + b * np.cos(an)
    x4 = x1 + b * np.cos(an)

    y2 = y1 + a * np.cos(an)
    y3 = y2 + b * np.sin(an)
    y4 = y1 + b * np.sin(an)

    polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])


circle(screen, (0, 0, 0), (200, 200), 153)  # чёрный обод вокруг смайлика
circle(screen, (250, 250, 0), (200, 200), 150)  # основа смайлика (жёлтый фон)

circle(screen, (250, 0, 0), (135, 170), 30)  # левая красная оболочка глаза
circle(screen, (0, 0, 0), (135, 170), 10)  # левый зрачок
rotated((0, 0, 0), 70, 85, 15, 130, 30)  # левая бровь

circle(screen, (250, 0, 0), (400 - 135, 170), 25)  # правая красная оболочка глаза
circle(screen, (0, 0, 0), (400 - 135, 170), 10)  # правый зрачок
rotated((0, 0, 0), 340, 120, 15, 130, 160)  # правая бровь

rect(screen, (0, 0, 0), (125, 260, 150, 20))  # рот

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
