'''
# @Author      : Darwin Neira Carrasco 
# @Email       : dneirac@unsa.edu.pe
# @File        : game
#
# @Description : 
'''

import pygame as pg
from random import randint, uniform

vec = pg.math.Vector2
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
DARKGRAY = (40, 40, 40)

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 4
MAX_FORCE = 0.4
RAND_TARGET_TIME = 500
WANDER_RING_DISTANCE = 150
WANDER_RING_RADIUS = 50
WANDER_TYPE = 2

# Obstacle sizes
OBSTACLE_SIZE = 100
CIRCLE_RADIUS = 80

class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color, is_circle=False):
        self.groups = all_sprites, obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.color = color
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_circle = is_circle
        self.radius = w // 2 if is_circle else 0

        if is_circle:
            pg.draw.circle(self.image, color, (w // 2, h // 2), self.radius)
        else:
            self.image.fill(color)

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites, mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.last_update = 0
        self.target = vec(randint(0, WIDTH), randint(0, HEIGHT))

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def wander_improved(self):
        future = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = future + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        self.displacement = target
        return self.seek(target)

    def wander(self):
        now = pg.time.get_ticks()
        if now - self.last_update > RAND_TARGET_TIME:
            self.last_update = now
            self.target = vec(randint(0, WIDTH), randint(0, HEIGHT))
        return self.seek(self.target)

    def update(self):
        if WANDER_TYPE == 1:
            self.acc = self.wander()
        else:
            self.acc = self.wander_improved()

        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel

        # Colisión con los bordes
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        # Detectar colisión con obstáculos
        hits = pg.sprite.spritecollide(self, obstacles, False)
        if hits:
            # Mover el Mob fuera del área de colisión
            self.pos -= self.vel
            # Cambiar la dirección con un pequeño ángulo aleatorio para que no quede atrapado
            self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))

        self.rect.center = self.pos

class Player(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH // 2, HEIGHT // 2)
        self.vel = vec(0, 0)
        self.rect.center = self.pos

    def update(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -MAX_SPEED
        if keys[pg.K_RIGHT]:
            self.vel.x = MAX_SPEED
        if keys[pg.K_UP]:
            self.vel.y = -MAX_SPEED
        if keys[pg.K_DOWN]:
            self.vel.y = MAX_SPEED

        self.pos += self.vel

        # Colisiones con los bordes
        if self.pos.x < 0: self.pos.x = 0
        if self.pos.x > WIDTH: self.pos.x = WIDTH
        if self.pos.y < 0: self.pos.y = 0
        if self.pos.y > HEIGHT: self.pos.y = HEIGHT

        # Detectar colisión con obstáculos
        if pg.sprite.spritecollide(self, obstacles, False):
            self.pos -= self.vel  # Deshacer el movimiento al colisionar

        self.rect.center = self.pos

# Inicialización de Pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# Grupos de sprites
all_sprites = pg.sprite.Group()
obstacles = pg.sprite.Group()
mobs = pg.sprite.Group()

# Crear jugador
player = Player()

# Crear obstáculos (cuadrados y círculo)
Obstacle(0, 0, OBSTACLE_SIZE, OBSTACLE_SIZE, WHITE)  # Esquina superior izquierda
Obstacle(WIDTH - OBSTACLE_SIZE, 0, OBSTACLE_SIZE, OBSTACLE_SIZE, WHITE)  # Esquina superior derecha
Obstacle(0, HEIGHT - OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE, WHITE)  # Esquina inferior izquierda
Obstacle(WIDTH - OBSTACLE_SIZE, HEIGHT - OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE, WHITE)  # Esquina inferior derecha
Obstacle(WIDTH // 2 - CIRCLE_RADIUS, HEIGHT // 2 - CIRCLE_RADIUS, CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2, WHITE, is_circle=True)  # Círculo central

# Crear mob inicial
Mob()

paused = False
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_m:
                Mob()  # Agregar más mobs

    if not paused:
        all_sprites.update()

    # Dibujar
    screen.fill(DARKGRAY)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()


