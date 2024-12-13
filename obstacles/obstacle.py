'''
# @Author      : Darwin Neira Carrasco 
# @Email       : dneirac@unsa.edu.pe
# @File        : obstacle
#
# @Description : 
'''

# obstacles/obstacle.py
import pygame as pg
from config import DARKGRAY

class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, shape="rect", image=None, all_sprites=None, obstacles=None):
        # Si no se proporcionan grupos, se inicializan como vacíos
        if all_sprites is None:
            all_sprites = pg.sprite.Group()
        if obstacles is None:
            obstacles = pg.sprite.Group()

        # Inicializar con los grupos proporcionados
        super().__init__(all_sprites, obstacles)

        self.shape = shape

        if self.shape == "rect":
            self.image = pg.image.load(image).convert_alpha() if image else pg.Surface((w, h))
            if image:
                self.image = pg.transform.scale(self.image, (w, h))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        elif self.shape == "circle":
            self.image = pg.image.load(image).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

