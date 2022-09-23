import pygame
from pygame.draw import *
from random import *

pygame.init()

# создание фона и настройки фона
width = 1000
height = 1000
FPS = 120
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))
pygame.display.set_caption('gun')

# используемые и, возможно, неиспользуемые цвета
SILVER = (192, 192, 192)
RED = (255, 0, 0)
OLIVE = (128, 128, 0)
DARK_GREEN = (0, 128, 0)
DARK_DARK_GREEN = (0, 64, 0)
DARK_DARK_DARK_GREEN = (0, 32, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Начальные парметры
max_life = 1000 # максимальное время жизни
target_count = 2 # количсество целей
min_gun_len = 20 # длина пушки до выстрела
max_gun_len = 80 # максимальная длина отрезка, изображающего пушку
max_radius = 50 # максимальный радиус мишени
rad_bullet = 15 # радиус пули
min_power = 4 # Минимальная можность пушки
min_radius = 10 # минимальный радиус мишени
max_velocity = 3 # максимальная состовляющая скоррости на одну координату
g = 0.1 #  типа ускорение свободного падения (пусть мы нахордимся в каком-то поле тяжести)

class target:
    """
    Класс мишени:
    r - радиус мишени
    x, y - координаты мишени
    vx, vy - скорости мишени
    x_0 y_0 - координаты торпеды, котороый будут стрелять цели
    T - переод пуска торпеды
    t - время для отсчёта времени жизни торпеды
    """
    def __init__(self):
        """
        Конструтктор класса мишень
        """
        self.r = min_radius + random() * max_radius
        self.x = min_radius + random() * (width - max_radius)
        self.y = min_radius + random() * (height - max_radius)
        self.x_0 = self.x
        self.y_0 = self.y
        self.vy_0 = 0
        self.vx = random() * max_velocity
        self.vy = random() * max_velocity
        self.T = 50

    def draw_target(self):
        """
        Метод отрисовки мишени
        """
        circle(screen, BLACK, (self.x, self.y), self.r)
        circle(screen, WHITE, (self.x, self.y), self.r * 4 / 5)
        circle(screen, BLACK, (self.x, self.y), self.r * 3 / 5)
        circle(screen, WHITE, (self.x, self.y), self.r * 2 / 5)
        circle(screen, BLACK, (self.x, self.y), self.r / 5)

    def moving_target_type_1(self):
        """
        Движение мишени первый тип: абсолютно упругие отражения он стен
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x >= width - self.r or self.x <= self.r:
            self.vx = - self.vx
        if self.y >= height - self.r or self.y <= self.r:
            self.vy = - self.vy

    def moving_target_type_2(self):
        """
        Просто стоящие неподвижные цели
        """
        if self.x >= width - self.r or self.x <= self.r:
            self.vx = - self.vx
        if self.y >= height - self.r or self.y <= self.r:
            self.vy = - self.vy

    def move_torpeda(self):
        self.vy_0 += g
        self.y_0 += self.vy_0
        if (self.y_0 > height):
            self.x_0 = self.x
            self.y_0 = self.y
            self.vy_0 = 0

    def draw_torpeda(self):
        
        pygame.draw.polygon(screen, RED, [[self.x_0, self.y_0], [self.x_0 - 6, self.y_0 - 10], [self.x_0 + 6, self.y_0 - 10 ]])

class gun:
    """
    Класс пушки
    x, y - координаты пушки
    vx, vy - состовляющие скорости пушки
    min_power - минимальная энергия стрельбы (немножко не физически, но тут энергия пропорциальна скорости, пусть будет кастомная физика)
    barrel_length - длина ствола пушки
    """
    def __init__(self):
        """
        Конструтуор пушки
        """
        self.barrel_length = min_gun_len
        self.x = 500
        self.y = 900
        self.vx = 2
        self.vy = 2
        self.power = min_power

    def move_left(self):
        self.x -= self.vx

    def move_right(self):
        self.x += self.vx

    def move_fordward(self):
        self.y -= self.vy

    def move_back(self):
        self.y += self.vy

    def draw_gun(self):
        """
        Метод отрисовки пушки, типа танк
        """
        rect(screen, DARK_GREEN, (self.x - 25, self.y - 50, 50, 100))
        circle(screen, OLIVE, (self.x, self.y), 20)
        cord = list(pygame.mouse.get_pos())
        l = ((cord[0] - self.x) ** 2 + (cord[1] - self.y) ** 2) ** 0.5
        cord[0] = self.x + (cord[0] - self.x) * self.barrel_length / (l)
        cord[1] = self.y + (cord[1] - self.y) * self.barrel_length / (l)
        line(screen, DARK_DARK_GREEN, (self.x, self.y), cord, 7)

class bullet:
    """
    Класс снаряда
    x, y - координаты снаряда
    vx, vy - состовляющие скорости снаряда
    r - радиукс снаряда
    time_live - время, которое живёт снаряд
    R  - харрактеристический радиус пули
    """
    def __init__(self, gun):
        """
        Конструктор снаряда
        """
        self.x = gun.x
        self.y = gun.y
        cord = list(pygame.mouse.get_pos())
        l = ((cord[0] - self.x) ** 2 + (cord[1] - self.y) ** 2) ** 0.5
        self.vx = gun.power * (cord[0] - self.x) / l
        self.vy = gun.power * ( - cord[1] + self.y) / l
        self.r = 10
        self.live = 0
        self.R = 2

    def draw_bullet_type_1(self):
        """
        Отрисовка снаряда: бомбочка - летит и сильно подвержен полю тяжести
        """
        circle(screen, BLACK, (self.x, self.y), self.r)
        circle(screen, WHITE, (self.x, self.y), self.r - 2)
        circle(screen, SILVER, (self.x, self.y - self.r), 4)

    def draw_bullet_type_2(self):
        """
        Отрисовка снаряда: пуля летит и слабо подвержена полю тяжести
        для отслеживания соударения введу харрактеристический радиус пули R = 2
        """
        pygame.draw.polygon(screen, BLACK,[[self.x - 2, self.y + 2], [self.x + 2, self.y - 2], [self.x - 5, self.y - 5]])

    def hit_target_type_1(self, target):
        """
        Проверка соударяется ли какая-либо цель с бомбочкой
        """
        if ((self.y - target.y) ** 2 + (self.x - target.x) ** 2 <= (target.r + self.r) ** 2):
            return True
        else:
            return False

    def hit_target_type_2(self, target):
        """
        Проверка соударяется ли какая-либо цель с пулей
        """
        if ((self.y - target.y) ** 2 + (self.x - target.x) ** 2 <= (target.r + self.R) ** 2):
            return True
        else:
            return False

    def moving_bullet_type_1(self):
        """
        Движегние снаряда - бомбочка
        """
        self.x += self.vx
        self.y -= self.vy
        self.live += 1
        self.vy -= g
        if self.x >= width - self.r or self.x <= self.r:
            self.vx = - self.vx
        if self.y >= height - self.r or self.y <= self.r:
            self.vy = - self.vy

    def moving_bullet_type_2(self):
        """
        Движегние снаряда - пуля
        """
        self.x += self.vx
        self.y -= self.vy
        self.live += 1

clock = pygame.time.Clock()
finished = False

# создание пушки, множества снарядов и мнодества целей
main_gun = gun()
set_of_bullet = []
set_of_bombs = []
set_of_target = [target() for i in range(target_count)]

# следующий код служит для работы пушки, а имено механизма индикатора стрельбы и т.п.
flag_1 = 0
flag_2 = 0
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            flag_1 = 1
            flag_2 = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            flag_1 = 1
            flag_2 = 0
    if flag_1 == 1 and flag_2 == 0:
        a = bullet(main_gun)
        if randint(1, 5) % 2 == 0:
            set_of_bullet.append([a, 0])
        else:
            set_of_bombs.append([a , 0])
        main_gun.color = DARK_DARK_GREEN
        main_gun.barrel_length = min_gun_len
        main_gun.power = min_power
        flag_2 = 0
        flag_1 = 0
    elif flag_1 == 1 and flag_2 == 1:
        main_gun.color = DARK_DARK_DARK_GREEN
        if main_gun.barrel_length < max_gun_len:
            main_gun.barrel_length += 1
            main_gun.power += 0.2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        main_gun.move_left()
    if keys[pygame.K_RIGHT]:
        main_gun.move_right()
    if keys[pygame.K_UP]:
        main_gun.move_fordward();
    if keys[pygame.K_DOWN]:
        main_gun.move_back()

    for i in set_of_target:
        i.move_torpeda()
        i.draw_torpeda()


    #отрисовка, движения и проверка соударений

    # 1) нарисовал пушку
    main_gun.draw_gun()

    # 2) проверка соударений целей и снарядов
    #  отрисовка моударений бомбочку и целей
    counter = 0
    for i in set_of_bullet:
        for j in set_of_target:
            if i[0].hit_target_type_1(j):
                j.r = min_radius + random() * max_radius
                j.x = min_radius + random() * (width - max_radius)
                j.y = min_radius + random() * (height - max_radius)
                j.vx = random() * max_velocity
                j.vy = random() * max_velocity
        i[1] += 1
        if (i[1] < max_life):
            i[0].moving_bullet_type_1()
            i[0].draw_bullet_type_1()

    for i in set_of_bombs:
        for j in set_of_target:
            if i[0].hit_target_type_2(j):
                j.r = min_radius + random() * max_radius
                j.x = min_radius + random() * (width - max_radius)
                j.y = min_radius + random() * (height - max_radius)
                j.vx = random() * max_velocity
                j.vy = random() * max_velocity
        i[1] += 1
        if (i[1] < max_life):
            i[0].moving_bullet_type_2()
            i[0].draw_bullet_type_2()

    # 3) движение и отрисовка целей

    set_of_target[0].moving_target_type_1()
    set_of_target[0].draw_target()
    set_of_target[1].moving_target_type_2()
    set_of_target[1].draw_target()

    pygame.display.update()
    screen.fill((255, 255, 255))

pygame.quit()
