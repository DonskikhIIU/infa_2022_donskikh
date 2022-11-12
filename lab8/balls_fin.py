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
    k = randint(3, 6)
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


def new_cubes():
    '''
    Случайным образом определяет начальные характеристики кубиков
    (их количество - m, цвет - ccolor, сторону - cr, модуль скорости - cv,
    её направление - ckx, cdx, cky, cdy), строит кубики в начальном положении.
    '''
    global m, cx, cy, cr, ccolor, cv, ckx, cky, cdx, cdy
    m = randint(3, 6)
    cx = []
    cy = []
    cr = []
    ccolor = []
    cv = []
    # ckx*cdx, cky*cdy - проекции скорости cv на Ох и Оу соответственно:
    ckx = []
    cky = []
    cdx = [randint(-1, 1) for i in range(m)]
    cdy = [randint(-1, 1) for i in range(m)]

    for i in range(m):
        cv.append(randint(4, 8))
        cx.append(randint(100, 1100))
        cy.append(randint(100, 900))
        cr.append(randint(10, 100))
        ccolor.append(COLORS[randint(0, 5)])
        ckx.append(randint(0, cv[i]))
        cky.append(abs(cv[i] ** 2 - abs(ckx[i] * cdx[i]) ** 2) ** 0.5)

        rect(screen, ccolor[i], (cx[i], cy[i], cr[i], cr[i]))


def cubes_movement():
    '''
    Обновляет координаты кубиков, затем их рисует.
    При вызове функции после new_cubes() в цикле заставляет кубики двигаться.
    '''
    for i in range(m):
        # Введём случайное число L, необходимое для хаотичного движения кубиков:
        L = randint(0, 1)
        # Исключим случай полной остановки кубиков:
        if ckx[i] * cdx[i] == 0 and cky[i] * cdy[i] == 0:
            cdx[i] = randint(-10, 10)
            cdy[i] = randint(-10, 10)
            ckx[i] = randint(0, cv[i])
            cky[i] = abs(cv[i] ** 2 - abs(ckx[i] * cdx[i]) ** 2) ** 0.5
        # Если кубик достиг границы по Ох:
        if not (cr[i] < cx[i] + ckx[i]*cdx[i] < 1200 - cr[i]):
            cdx[i] = -cdx[i]
            cdy[i] = randint(-1, 1)
            cky[i] = randint(0, cv[i])
            ckx[i] = abs(cv[i]**2 - abs(cky[i] * cdy[i])**2)**0.5
        # Если кубик достиг границы по Оу:
        if not (cr[i] < cy[i] + cky[i]*cdy[i] < 900 - cr[i]):
            cdy[i] = -cdy[i]
            cdx[i] = randint(-1, 1)
            ckx[i] = randint(0, cv[i])
            cky[i] = abs(cv[i]**2 - abs(ckx[i] * cdx[i])**2)**0.5

        cx[i] += ckx[i] * cdx[i]
        cy[i] += cky[i] * cdy[i]
        rect(screen, ccolor[i], (cx[i], cy[i], cr[i], cr[i]))
        # В зависимости от случайного числа L
        # кубики будут случайно изменять свою траекторию:
        if L == 0:
            cdx[i] = -cdx[i]
            cdy[i] = randint(-1, 1)
            cky[i] = randint(0, cv[i])
            ckx[i] = abs(cv[i] ** 2 - abs(cky[i] * cdy[i]) ** 2) ** 0.5

        if L == 1:
            cdy[i] = -cdy[i]
            cdx[i] = randint(-1, 1)
            ckx[i] = randint(0, cv[i])
            cky[i] = abs(cv[i] ** 2 - abs(ckx[i] * cdx[i]) ** 2) ** 0.5


def click(event):
    '''
    Выводит координаты и радиусы шариков, координаты мыши.
    Возвращает 0 в случае успешного попадания по шарику, 1 - по кубику.
    event - событие (нажатие кнопки мыши)
    '''
    mouse = event.pos
    print(mouse)

    for i in range(k):
        print(x[i], y[i], r[i])
        if abs(x[i] - mouse[0]) ** 2 + abs(y[i] - mouse[1]) ** 2 <= r[i] ** 2:
            return 0

    for j in range(m):
        if mouse[0] >= cx[j] - cr[j] <= cx[j] + cr[j]:
            if mouse[1] >= cy[j] - cr[j] <= cy[j] + cr[j]:
                return 1


pygame.display.update()
clock = pygame.time.Clock()
finished = False

# счётчик:
n = 0

new_balls()
new_cubes()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # В случае успешного попадания по шарику
            # зачисляется 1 очко, по кубику - 3 очка:
            if click(event) == 0:
                n += 1
            if click(event) == 1:
                n += 3

    balls_movement()
    cubes_movement()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

print('Общий счёт:', n)
