#Траектория частицы
Track = True

#длина траектории
Track_time = 10

#Гравитационная постоянная
G = 5

#Сила магнитного взаимодействия(одинаковые цвета -
#притягиваются, разные - отталкиваются)
MagnConst = 0

#Количество частиц
count = 120

#Начальная скорость частиц
kv = 5

#Случайная генерация частиц
RANDOM = False

#Радиус случайных частиц
r = 4

#Ширина и высота окна
WIN_WIDTH, WIN_HEIGHT = 900, 650


'''всё, что дальше, лучше не менять'''

#Закон для гравитационного взаимодействия
zg = 2

#Закон для магнитного взаимодействия
zm = 2

#Коэф. трения, чем он больше - тем меньше трение
k = 40

#Отталкивание частиц
antiG = 0.1

max_speed = 3

ResDist = 1

#Притяжение вниз
EarthG = 0

#Отражение частиц от стенок
Mirror = True

import pygame
from math import hypot, ceil, sqrt
from random import randint, random

def planet(sun, orb, color, r = 6, m = 15):
    vx = (sun.mass * G / orb) ** 0.5
    return Ball(sun.x, sun.y - orb, color, r = r, mass = m, vx = vx)


def custom_pos():
    '''Здесь вы можете написать своё расположение планет'''
    '''не забудьте установить RANDOM = FALSE'''
    B.append(Ball(200, 300, BLUE, r = 30, mass = 50, vx = 0))    #x, y, col, r, vx, vy, mass
    B.append(planet(B[0], 200, RED, m = 1))


class Ball:
    def __init__(self, x, y, col, r = 4, vx = 0, vy = 0, mass = 4):
        self.x = x
        self.y = y
        self.r = r
        self.col = col
        self.vx = vx
        self.vy = vy
        self.mass = mass
        
    def move(self, Walls, WIN_WIDTH, WIN_HEIGHT, ofs_x, ofs_y):
        if Walls:
            x = self.x - ofs_x
            y = self.y - ofs_y
            if x <= 0 and self.vx < 0:
                if Mirror:
                    self.vx = -self.vx
                else:
                    self.x += WIN_WIDTH
                self.vx, self.vy = self.v_norm(self.vx, self.vy)
            if x >= WIN_WIDTH and self.vx > 0:
                if Mirror:
                    self.vx = -self.vx
                else:
                    self.x -= WIN_WIDTH
                self.vx, self.vy = self.v_norm(self.vx, self.vy)
            if y <= 0 and self.vy < 0:
                if Mirror:
                    self.vy = -self.vy
                else:
                    self.y += WIN_HEIGHT
                self.vx, self.vy = self.v_norm(self.vx, self.vy)
            if y >= WIN_HEIGHT and self.vy > 0:
                if Mirror:
                    self.vy = -self.vy
                else:
                    self.y -= WIN_HEIGHT
                self.vx, self.vy = self.v_norm(self.vx, self.vy)
            
        self.x += self.vx
        self.y += self.vy

        
    def force(self, ind, selfind):
        ox = B[ind].x
        oy = B[ind].y
        m = B[ind].mass
        if m < 0.01 and self.mass < 0.01:
            return 0
        r = B[ind].r
        vx = B[ind].vx
        vy = B[ind].vy
        dist = hypot(self.x - ox, self.y - oy)
        min_dist = (self.r + B[ind].r) * ResDist
        f = 0
        m_relative = self.mass / B[ind].mass
        if dist <= min_dist:
            newVx = (vx * m + self.vx * self.mass) / (m + self.mass)
            newVy = (vy * m + self.vy * self.mass) / (m + self.mass)
            self.vx = (newVx + k * self.vx) / (k + 1)
            B[ind].vx = (newVx + k * B[ind].vx) / (k + 1)
            self.vy = (newVy + k * self.vy) / (k + 1)
            B[ind].vy = (newVy + k * B[ind].vy) / (k + 1)
            f -= antiG * min(abs(min_dist - dist), min(m, self.mass) * 3)
        else:
            f += min(self.mass * B[ind].mass * G  / (dist ** zg), G / 10)
            mf = MagnConst * self.mass / (dist ** zm)
            if B[ind].col == B[selfind].col:
                mf = - mf
            f += mf
        fx = f * ((ox - self.x) / dist)
        fy = f * ((oy - self.y) / dist)
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax
        self.vy += ay + EarthG
        B[ind].vx -= ax * m_relative
        B[ind].vy -= ay * m_relative - EarthG

    @staticmethod
    def v_norm(vx, vy):
        v = hypot(vx, vy)
        if v > max_speed:
            vx = max_speed * (vx / v)
            vy = max_speed * (vy / v)
        return vx, vy


class Point:
    def __init__(self, x, y, col, r = 0, max_age = Track_time):
        self.age = 0
        self.x = x
        self.y = y
        self.col = col
        self.r = r
        self.max_age = max_age
    def vis(self, ofs_x, ofs_y):
        pygame.draw.circle(sc, self.col, (round(self.x - ofs_x),
                                          round(self.y - ofs_y)), self.r, 0)
        self.age += 1
        if self.age > self.max_age:
            T.remove(self)
        
def rand(count, WIN_WIDTH, WIN_HEIGHT):
    global kv
    B = []
    for i in range(count):
        m = r ** 2
        x = randint(0, WIN_WIDTH) + random()
        y = randint(0, WIN_HEIGHT) + random()
        vx = kv * randint(-100, 100) / 100
        vy = kv * randint(-100, 100) / 100
        col = Colors[randint(0, len(Colors) - 1)]
        B.append(Ball(x, y, col, r = r, vx = vx, vy = vy, mass = m))
    return B

def createBall(col, x, y, r = r, m = r):
    m = r
    B.append(Ball(x, y, col))

def get_offset(B):
    sum_x, sum_y = 0, 0
    m = 0
    for i in range(len(B)):
        sum_x += B[i].x * B[i].mass
        sum_y += B[i].y * B[i].mass
        m += B[i].mass
    if len(B) == 0:
        return 0, 0
    return sum_x / m, sum_y / m

def visBalls(B):
    for i in range(len(B)):
        pygame.draw.circle(sc, B[i].col, (round(B[i].x - ofs_x),
                                          round(B[i].y - ofs_y)), B[i].r, 0)
        T.append(Point(B[i].x, B[i].y, B[i].col))
        
FPS = 60
darkblue = (0, 2, 25)
ORANGE = (255, 200, 150)
RED = (255, 150, 150)
GREEN = (150, 255, 150)
BLUE = (150, 150, 255)
YELLOW = (255, 255, 0)
Colors = [RED, BLUE]#, GREEN]#, ORANGE]                       
pygame.init() 
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
sc.fill(darkblue)

maxF = 0.3
minv = 0.01
Walls = True
Collisions = True
Same = True
Check = False
tt = []

B = []
if RANDOM:
    B = rand(count, WIN_WIDTH, WIN_HEIGHT)
else:
    custom_pos()
    
Pause = False
delay = 0

if Track:
    T = []
for z in range(100000):
    sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    sc.fill(darkblue)
    ofs_x, ofs_y = get_offset(B)
    ofs_x -= WIN_WIDTH // 2
    ofs_y -= WIN_HEIGHT // 2
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            quit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                Pause = not Pause
            elif i.key == pygame.K_w:
                WIN_HEIGHT += 10
                WIN_WIDTH += 10
            elif i.key == pygame.K_s:
                WIN_HEIGHT -= 10
                WIN_WIDTH -= 10
                
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    if pressed[0] and delay < 0:
        delay = 20
        createBall(RED, x + ofs_x, y + ofs_y)
    if pressed[2] and delay < 0:
        delay = 20
        createBall(BLUE, x + ofs_x, y + ofs_y )
    delay -= 1
    
    if not Pause:
        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                B[i].force(j, i)
        for i in range(len(B)):
            B[i].move(Walls, WIN_WIDTH, WIN_HEIGHT, ofs_x, ofs_y)
    for i in range(len(T)):
        try:
            T[i].vis(ofs_x, ofs_y)
        except IndexError:
            pass
    visBalls(B)
    
    pygame.display.update()
    clock.tick(FPS)

