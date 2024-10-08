'''
# @Author      : Darwin Neira Carrasco 
# @Email       : dneirac@unsa.edu.pe
# @File        : move
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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
BROWN = (139, 69, 19)

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 4
MAX_FORCE = 0.4
RAND_TARGET_TIME = 500
WANDER_RING_DISTANCE = 150
WANDER_RING_RADIUS = 50
WANDER_TYPE = 2

# Grupo de obstáculos
obstacles = pg.sprite.Group()

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
        
        # Detectar colisión con obstáculos (cuadrados blancos y círculo central)
        hits = pg.sprite.spritecollide(self, obstacles, False)
        if hits:
            # Calcular una nueva dirección alejada del obstáculo más cercano
            for obstacle in hits:
                # Desviarse del obstáculo más cercano
                diff = self.pos - obstacle.rect.center  # Dirección opuesta al obstáculo
                if diff.length() > 0:  # Si la longitud no es cero
                    diff.scale_to_length(MAX_SPEED)  # Ajustar la magnitud a la velocidad máxima
                self.vel = diff  # Aplicar la nueva dirección

        self.rect.center = self.pos

class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        self.groups = all_sprites, obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()

# Crear obstáculos en las esquinas
Obstacle(0, 0, 150, 150)  # esquina superior izquierda
Obstacle(WIDTH - 150, 0, 150, 150)  # esquina superior derecha
Obstacle(0, HEIGHT - 150, 150, 150)  # esquina inferior izquierda
Obstacle(WIDTH - 150, HEIGHT - 150, 150, 150)  # esquina inferior derecha

# Crear el obstáculo circular en el centro
center_circle_rect = pg.Rect(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 200)

# Crear mobs
for i in range(5):
    Mob()

paused = False
show_vectors = False
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
            if event.key == pg.K_v:
                show_vectors = not show_vectors
            if event.key == pg.K_m:
                Mob()
    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)

    # Dibujar los obstáculos (cuadrados blancos y círculo central)
    all_sprites.draw(screen)
    pg.draw.ellipse(screen, WHITE, center_circle_rect)  # Dibuja el círculo central

    if show_vectors:
        for sprite in mobs:
            sprite.draw_vectors()
    pg.display.flip()

pg.quit()
