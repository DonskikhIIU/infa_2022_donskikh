import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 900))

# Цвета шариков:
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_balls():
    '''
    Случайным образом определяет начальные характеристики шариков
    (их количество - k, цвет - color, радиус - r, модуль скорости - v,
    её направление - kx, dx, ky, dy), строит шарики в начальном положении.
    '''
    global k, x, y, r, color, v, kx, ky, dx, dy
    k = randint(3, 6)  # число шариков
    x = []
    y = []
    r = []
    color = []
    v = []
    # kx*dx, ky*dy - проекции скорости v на Ох и Оу соответственно:
    kx = []
    ky = []
    dx = [randint(-1, 1) for i in range(k)]
    dy = [randint(-1, 1) for i in range(k)]

    for i in range(k):
        v.append(randint(4, 8))
        x.append(randint(100, 1100))
        y.append(randint(100, 900))
        r.append(randint(10, 100))
        color.append(COLORS[randint(0, 5)])
        kx.append(randint(0, v[i]))
        ky.append(abs(v[i] ** 2 - abs(kx[i] * dx[i]) ** 2) ** 0.5)

        circle(screen, color[i], (x[i], y[i]), r[i])

def balls_movement():
    '''
    Обновляет координаты шариков, затем их рисует.
    При вызове функции после new_balls() в цикле заставляет шарики двигаться.
    '''
    for i in range(k):
        # Исключим случай полной остановки шариков:
        if kx[i] * dx[i] == 0 and ky[i] * dy[i] == 0:
            dx[i] = randint(-1, 1)
            dy[i] = randint(-1, 1)
            kx[i] = randint(0, v[i])
            ky[i] = abs(v[i] ** 2 - abs(kx[i] * dx[i]) ** 2) ** 0.5
        # Если шарик достиг границы по Ох:
        if not (r[i] < x[i] + kx[i]*dx[i] < 1200 - r[i]):
            dx[i] = -dx[i]
            dy[i] = randint(-1, 1)
            ky[i] = randint(0, v[i])
            kx[i] = abs(v[i]**2 - abs(ky[i] * dy[i])**2)**0.5
        # Если шарик достиг границы по Оу:
        if not (r[i] < y[i] + ky[i]*dy[i] < 900 - r[i]):
            dy[i] = -dy[i]
            dx[i] = randint(-1, 1)
            kx[i] = randint(0, v[i])
            ky[i] = abs(v[i]**2 - abs(kx[i] * dx[i])**2)**0.5

        x[i] += kx[i] * dx[i]
        y[i] += ky[i] * dy[i]
        circle(screen, color[i], (x[i], y[i]), r[i])


def click(event):
    '''
    Выводит координаты и радиусы кругов, координаты мыши.
    Возвращает True в случае успешного попадания.
    event - событие (нажатие кнопки мыши)
    '''
    mouse = event.pos
    print(mouse)
    for i in range(k):
        print(x[i], y[i], r[i])
        if abs(x[i] - mouse[0]) ** 2 + abs(y[i] - mouse[1]) ** 2 <= r[i] ** 2:
            return True


pygame.display.update()
clock = pygame.time.Clock()
finished = False

# счётчик:
n = 0

new_balls()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # В случае успешного попадания счётчик обновляется:
            if click(event): n += 1

    balls_movement()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

print('Общий счёт:', n)
