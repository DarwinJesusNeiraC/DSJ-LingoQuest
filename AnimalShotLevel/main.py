import pygame as pg
import math
import random
import os

class AnimalShotScene:
    def __init__(self, screen):
        self.screen = screen
        self.background = pg.transform.scale(
            pg.image.load(os.path.join(os.path.dirname(__file__), 'assets/background.jpg')), (800, 600)
        )

        # Jugador
        self.player_img = pg.image.load(os.path.join(os.path.dirname(__file__), 'assets/ufo.png'))
        self.player_img = pg.transform.scale(self.player_img, (50, 50))
        self.player_x = 300
        self.player_y = 500
        self.player_x_change = 0

        # Balas
        self.bullet_img = pg.image.load(os.path.join(os.path.dirname(__file__), 'assets/bullet.png'))
        self.bullet_img = pg.transform.scale(self.bullet_img, (10, 20))
        self.bullet_x = 0
        self.bullet_y = 480
        self.bullet_y_change = -10
        self.bullet_state = "ready"

        # Enemigos
        self.animal_images = [os.path.join(os.path.dirname(__file__), f'assets/{animal}.png')
                              for animal in ['cat', 'dog', 'fox', 'dove', 'star', 'full-moon']]
        self.animal_names = ['michi', 'alqo', 'atoq', 'urpi', 'chaska', 'killa']
        self.animal_dict = dict(zip(self.animal_names, self.animal_images))
        self.enemies = []
        self.create_enemies()

        # Variables de juego
        self.current_animal = random.choice(self.animal_names)
        self.lives = 3
        self.score_value = 0
        self.font = pg.font.Font(None, 32)
        self.scene_change = False

    def create_enemies(self):
        static_positions = [(20, 100), (100, 120), (200, 140), (300, 160), (450, 180), (600, 200)]
        for i, (animal_name, image_path) in enumerate(self.animal_dict.items()):
            enemy_img = pg.image.load(image_path)
            enemy_img = pg.transform.scale(enemy_img, (40, 40))
            enemy_x, enemy_y = static_positions[i]
            self.enemies.append({
                'img': enemy_img,
                'name': animal_name,
                'x': enemy_x,
                'y': enemy_y,
                'x_change': 2,
                'y_change': 40
            })

    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        self.screen.blit(self.bullet_img, (x + 16, y + 10))

    def is_collision(self, enemy_x, enemy_y, bullet_x, bullet_y):
        distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
        return distance < 27

    def run(self, events, keys):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))

        for event in events:
            if event.type == pg.QUIT:
                return 'quit'
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player_x_change = -5
                if event.key == pg.K_RIGHT:
                    self.player_x_change = 5
                if event.key == pg.K_SPACE and self.bullet_state == "ready":
                    self.bullet_x = self.player_x
                    self.fire_bullet(self.bullet_x, self.bullet_y)
            if event.type == pg.KEYUP:
                if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                    self.player_x_change = 0

        # Movimiento del jugador
        self.player_x += self.player_x_change
        if self.player_x <= 0:
            self.player_x = 0
        elif self.player_x >= 736:
            self.player_x = 736

        # Movimiento de la bala
        if self.bullet_y <= 0:
            self.bullet_y = 480
            self.bullet_state = "ready"
        if self.bullet_state == "fire":
            self.fire_bullet(self.bullet_x, self.bullet_y)
            self.bullet_y += self.bullet_y_change

        # Movimiento de enemigos y colisiones
        for enemy in self.enemies:
            enemy['x'] += enemy['x_change']
            if enemy['x'] <= 0 or enemy['x'] >= 760:
                enemy['x_change'] = -enemy['x_change']
                enemy['y'] += enemy['y_change']

            # Detectar colisión
            if self.is_collision(enemy['x'], enemy['y'], self.bullet_x, self.bullet_y):
                self.bullet_y = 480
                self.bullet_state = "ready"
                if enemy['name'] == self.current_animal:
                    self.score_value += 1
                    self.enemies.remove(enemy)
                    if not self.enemies:
                        print("Todos los enemigos han sido eliminados. Volviendo a 'main'.")
                        self.scene_change = True
                        break
                    self.current_animal = random.choice([e['name'] for e in self.enemies])

                else:
                    self.lives -= 1
                    self.enemies.remove(enemy)
                    if self.lives <= 0:
                        self.scene_change = True
                        break
                        #return 'main'

            # Dibujar enemigo
            self.screen.blit(enemy['img'], (enemy['x'], enemy['y']))

        if self.scene_change:
            return 'main'

        # Mostrar estado del juego
        self.screen.blit(self.player_img, (self.player_x, self.player_y))
        score_text = self.font.render(f"Score: {self.score_value}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 0, 0))
        animal_text = self.font.render(f"Find: {self.current_animal}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        self.screen.blit(animal_text, (10, 70))

        pg.display.flip()
        return 'animal_shot'
