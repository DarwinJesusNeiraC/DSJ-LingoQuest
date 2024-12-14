'''
# @Author      : Darwin Neira Carrasco 
# @Email       : dneirac@unsa.edu.pe
# @File        : mob
#
# @Description : 
'''

# mobs/mob.py
import pygame as pg
from random import randint, uniform, choice
from config import * 

class Mob(pg.sprite.Sprite):
    def __init__(self, all_sprites, mobs, citizen_images, obstacles):
        super().__init__(all_sprites, mobs)
        self.groups = all_sprites, mobs
        #pg.sprite.Sprite.__init__(self, self.groups)
        self.image = choice(citizen_images)
        self.rect = self.image.get_rect()
        self.pos = pg.math.Vector2(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = pg.math.Vector2(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = pg.math.Vector2(0, 0)
        self.rect.center = self.pos
        self.obstacles = obstacles  # Almacena el grupo de obstáculos
        #self.last_update = 0
        self.target = pg.math.Vector2(randint(0, WIDTH), randint(0, HEIGHT))

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def wander_improved(self):
        future = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = future + pg.math.Vector2(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        return self.seek(target)

    def wander(self):
        now = pg.time.get_ticks()
        if now - self.last_update > RAND_TARGET_TIME:
            self.last_update = now
            self.target = pg.math.Vector2(randint(0, WIDTH), randint(0, HEIGHT))
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
        hits = pg.sprite.spritecollide(self, self.obstacles, False)
        if hits:
            for obstacle in hits:
                diff = self.pos - obstacle.rect.center
                if diff.length() > 0:
                    diff.scale_to_length(MAX_SPEED)
                self.vel = diff

        self.pos += self.vel
        self.rect.center = self.pos

