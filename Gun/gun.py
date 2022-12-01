import math
from random import choice, randint

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

g = 2 # Ускорение мяча

WIDTH = 800
HEIGHT = 600
h = 30  # Высота нижней границы игрового поля


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.life_time = 0  # Счётчик времени 'жизни' мяча
        self.movement = True  # 'Индикатор' движения мяча

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна WIDTHхHEIGHT).
        """
        # FIXME
        # Если мяч касается края экрана, то он отскакивает как при
        # неупругом ударе (коэффициент 0.8 симулирует потерю энергии):
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
        if self.x - self.r < 0:
            self.x = self.r
        if self.y + self.r + self.vy > HEIGHT - h:
            self.y = HEIGHT - self.r - h
        if self.y - self.r + self.vy < 0:
            self.y = self.r
        if self.x + self.r == WIDTH or self.x - self.r == 0:
            self.vx *= -0.8
            self.vy *= 0.8
        if self.y + self.r == HEIGHT - h or self.y - self.r == 0:
            self.vy *= -0.8
            self.vx *= 0.8

        self.vy += g

        self.x += self.vx
        self.y += self.vy

        self.life_time += 1

        # Время 'жизни' мяча ограничено:
        if self.life_time == 200:
            self.color = WHITE
            self.x = 0
            self.y = 0
            self.vx = 0
            self.vy = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.y = y

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        if event.pos[0] > self.x:
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = self.f2_power * math.sin(self.an)
        else:
            new_ball.vx = - self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] - self.x > 0:
                self.an = math.atan((self.y - event.pos[1]) / (event.pos[0]-self.x))
            if event.pos[0] - self.x < 0:
                self.an = math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        pygame.draw.polygon(self.screen, self.color,
                            (
                                (
                                    self.x,
                                    self.y
                                ),
                                (
                                    self.x + self.f2_power * math.cos(self.an),
                                    self.y - self.f2_power * math.sin(self.an),
                                ),
                                (
                                    self.x + self.f2_power * math.cos(self.an) - 10 * math.sin(self.an),
                                    self.y - self.f2_power * math.sin(self.an) - 10 * math.cos(self.an)
                                ),
                                (
                                    self.x - 10 * math.sin(self.an),
                                    self.y - 10 * math.cos(self.an)
                                )
                            )
                            )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # FIXME: don't work!!! How to call this functions when object is created?
    def __init__(self, screen: pygame.Surface):
        self.points = 0
        self.r = randint(10, 50)
        self.x = randint(600, WIDTH - self.r)
        self.y = randint(300, HEIGHT - h - self.r)
        self.live = 1
        self.screen = screen
        self.v = 10
        self.vx = randint(0, self.v)
        self.vy = (self.v ** 2 - self.vx ** 2) ** 0.5
        self.color = choice(GAME_COLORS)

    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям окна
        (размер окна WIDTHхHEIGHT).
        """
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
        if self.x - self.r < 0:
            self.x = self.r
        if self.y + self.r + self.vy > HEIGHT - h:
            self.y = HEIGHT - self.r - h
        if self.y - self.r + self.vy < 0:
            self.y = self.r
        if self.x + self.r == WIDTH or self.x - self.r == 0:
            self.vx *= -1
        if self.y + self.r == HEIGHT - h or self.y - self.r == 0:
            self.vy *= -1

        self.x += self.vx
        self.y += self.vy

    def new_target(self):
        """ Инициализация новой цели. """
        self.r = randint(10, 50)
        self.x = randint(600, WIDTH - self.r)
        self.y = randint(300, HEIGHT - h - self.r)
        self.vx = randint(0, self.v)
        self.vy = (self.v ** 2 - self.vx ** 2) ** 0.5
        self.color = choice(GAME_COLORS)

    def draw(self):
        if self.live == 1:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points


class Extra_target:
    def __init__(self, screen: pygame.Surface):
        self.points = 0
        self.r = randint(10, 50)
        self.x = randint(600, WIDTH - 20 - self.r)
        self.y = randint(300, HEIGHT - h - self.r)
        self.live = 1
        self.screen = screen
        self.v = 10
        self.vx = randint(0, self.v)
        self.vy = (self.v ** 2 - self.vx ** 2) ** 0.5
        self.color = choice(GAME_COLORS)
        # Введём таймер, по истечении которого мячик переместиться в случайную
        # точку экрана:
        self.ball_timer = 0

    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям окна
        (размер окна WIDTHхHEIGHT).
        """
        # Введём случайное число L, необходимое для хаотичного движения мячей:
        L = randint(0, 1)

        self.vx = randint(-self.v, self.v)
        self.vy = (self.v ** 2 - self.vx ** 2) ** 0.5
        if L == 0:
            self.vy *= -1
        self.ball_timer += 1
        if self.ball_timer == 100:
            self.ball_timer = 0
            self.x = randint(200, WIDTH - 20 - self.r)
            self.y = randint(100, HEIGHT - h - self.r)
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
        if self.x - self.r < 0:
            self.x = self.r
        if self.y + self.r + self.vy > HEIGHT - h:
            self.y = HEIGHT - self.r - h
        if self.y - self.r + self.vy < 0:
            self.y = self.r
        if self.x + self.r == WIDTH or self.x - self.r == 0:
            self.vx *= -1
        if self.y + self.r == HEIGHT - h or self.y - self.r == 0:
            self.vy *= -1

        self.x += self.vx
        self.y += self.vy

    def draw(self):
        if self.live == 1:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )

    def new_target(self):
        """ Инициализация новой цели. """
        self.r = randint(10, 50)
        self.x = randint(600, WIDTH - 20 - self.r)
        self.y = randint(300, HEIGHT - h - self.r)
        self.vx = randint(0, self.v)
        self.vy = (self.v ** 2 - self.vx ** 2) ** 0.5
        self.color = choice(GAME_COLORS)
        self.ball_timer = 0

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen, 50, 450)
target = Target(screen)
extra_target = Extra_target(screen)
finished = False
timer = 0
score = 0

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    extra_target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    target.move()
    extra_target.move()

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
        if b.hittest(extra_target) and extra_target.live:
            extra_target.live = 0
            extra_target.hit()
            extra_target.new_target()
        if not target.live and not extra_target.live:
            timer += 1
            if timer == 200:
                timer = 0
                target.live = 1
                extra_target.live = 1
                target.draw()
                extra_target.draw()
    gun.power_up()

pygame.quit()

print('Score:', target.points + extra_target.points)
