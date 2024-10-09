'''
# @Authors      : Darwin Neira Carrasco 
#               : Nohelia Estefhania Tacca Apaza
#               : Angel Eduardo Hincho Jove
# @Email        : dneirac@unsa.edu.pe
# @File         : game
#
# @Description  : 
'''
import pygame as pg
from random import randint, uniform
#from pygame.locals import *
from character import Character
from dialogue import Dialogue
import subprocess

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
    def __init__(self, x, y, w, h, shape="rect", image = None):
        self.groups = all_sprites, obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.shape = shape  # Puede ser 'rect' o 'circle'
        
        if self.shape == "rect":
            # Si el obstáculo es un rectángulo
            #self.image = pg.Surface((w, h))
            #self.image.fill(WHITE)
            #self.image = pg.image.load(image).convert_alpha()  # Carga la imagen cuadrada
            self.image = pg.image.load(image).convert_alpha() if image else pg.Surface((w, h))
            if image:  # Si se proporciona una imagen, escalarla
                self.image = pg.transform.scale(self.image, (w, h))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        
        elif self.shape == "circle":
            self.image = pg.image.load(image).convert_alpha()  # Carga la imagen cuadrada
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
obstacles = pg.sprite.Group()
mobs = pg.sprite.Group()
bg_image = pg.image.load('assets/floor.jpeg').convert()  # Cambia la ruta a tu imagen de fondo

# Cargar personajes
#inca = Character('assets/inca.png', 100, 100, 50, 50)
#chasqui = Character('assets/chasqui.png', 400, 300, 50, 50)
# Cargar personajes
inca = Character('assets/inca.png', WIDTH // 2, HEIGHT // 2 - 80, 50, 50)  # Arriba de la fuente
chasqui = Character('assets/chasqui.png', WIDTH // 2, HEIGHT // 2 + 80, 50, 50)  # Debajo de la fuente


# Crear diálogo
dialogue_text = "Inca: ¡Hola, Chasqui!\nChasqui: ¡Hola, Inca!"
dialogue = Dialogue(WIDTH, HEIGHT, dialogue_text)

# Crear obstáculos en las esquinas
Obstacle(0, 0, 150, 150, shape="rect", image = "assets/hospital.png")  # esquina superior izquierda
Obstacle(WIDTH - 150, 0, 150, 150, shape="rect", image = "assets/house.png")  # esquina superior derecha
Obstacle(0, HEIGHT - 150, 150, 150, shape="rect", image = "assets/market.png")  # esquina inferior izquierda
Obstacle(WIDTH - 150, HEIGHT - 150, 150, 150, shape="rect", image = "assets/market.png")  # esquina inferior derecha

# Crear el obstáculo circular en el centro
Obstacle(WIDTH // 2, HEIGHT // 2, 200, 200, shape="circle", image = "assets/font.png")  # Círculo en el centro

# Crear mobs
for i in range(5):
    Mob()

paused = False
show_vectors = False
running = True
game_won = False
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
        # Mover al inca con las teclas
    keys = pg.key.get_pressed()
    inca.move(keys, 5)
    if not paused:
        all_sprites.update()

    # Fill the screen and draw background first
    screen.fill(DARKGRAY)
    screen.blit(bg_image, (0, 0))  # Draw background

    all_sprites.draw(screen)
    # Dibujar personajes
    inca.draw(screen)
    chasqui.draw(screen)

    # Detectar colisión y mostrar diálogo
    if inca.is_collision(chasqui) and not game_won:
        dialogue.show(screen)
        pg.display.flip()  # Ensure the dialogue is displayed before the next step
        pg.time.delay(2000)  # Pause for 2 seconds to let the player read the dialogue
        dialogue.reset()
        game_won = True
        subprocess.run(["python3", "QuechuaGame/main.py"])  # Adjust path as necessary

    elif not inca.is_collision(chasqui):
        dialogue.reset()
        game_won = False
                    
    if not paused:
        all_sprites.update()

    pg.display.set_caption("{:.2f}".format(clock.get_fps()))

    if show_vectors:
        for sprite in mobs:
            sprite.draw_vectors()
    pg.display.flip()

pg.quit()

