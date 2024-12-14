import sys
import os
import pygame as pg
from config import *
from ball import BallGameScene
from AnimalShotLevel.main import AnimalShotScene
from characters.character import Character
from dialogues.dialogue import InteractiveDialogue
from mobs.mob import Mob
from obstacles.obstacle import Obstacle

class MainScene:
    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.inca = Character('assets/inca.png', WIDTH // 2, HEIGHT // 2 - 80, 50, 50)
        self.chasqui = Character('assets/chasqui.png', WIDTH // 2, HEIGHT // 2 + 80, 50, 50)
        self.dialogue = InteractiveDialogue(WIDTH, HEIGHT, "Inca: ¡Hola, Chasqui!\nChasqui: ¡Hola, Inca!")
        self.obstacles = pg.sprite.Group()
        self.bg_image = pg.image.load('assets/floor.jpeg').convert()

        # Cargar imagen del trofeo
        self.trophy_image = pg.image.load('assets/trophy.jpg').convert_alpha()
        self.trophy_image = pg.transform.scale(self.trophy_image, (350, 350))
        self.trophy_bg_image = pg.image.load('assets/background_trophy.jpg').convert_alpha()
        self.trophy_bg_image = pg.transform.scale(self.trophy_bg_image, (500, 500))

        # Crear obstáculos
        self.hospital = Obstacle(0, 0, 150, 150, shape="rect", image="assets/hospital.png", obstacles=self.obstacles)
        self.house = Obstacle(WIDTH - 150, 0, 150, 150, shape="rect", image="assets/house.png", obstacles=self.obstacles)
        self.market = Obstacle(0, HEIGHT - 150, 150, 150, shape="rect", image="assets/market.png", obstacles=self.obstacles)
        self.secondMarket = Obstacle(WIDTH - 150, HEIGHT - 150, 150, 150, shape="rect", image="assets/market.png", obstacles=self.obstacles )  

        self.font = Obstacle(WIDTH // 2, HEIGHT // 2, 200, 200, shape="circle", image="assets/font.png", obstacles=self.obstacles)

        # Cargar imágenes de ciudadanos
        citizen_images = [
            pg.transform.scale(pg.image.load('assets/citizen1.png').convert_alpha(), (50, 50)),
            pg.transform.scale(pg.image.load('assets/citizen2.png').convert_alpha(), (50, 50)),
            pg.transform.scale(pg.image.load('assets/citizen3.png').convert_alpha(), (50, 50)),
        ]

        # Crear ciudadanos (mobs)
        for _ in range(5):  # Cambia el número según la cantidad de ciudadanos que quieras
            Mob(self.all_sprites, self.mobs, citizen_images, self.obstacles)

        self.running = True
        self.show_trophy_screen = False
        # Bandera para verificar si los juegos están completados
        self.games_completed = {"ball_game": False, "animal_shot": False}

    def close_image(self):
        self.show_trophy_screen = False

    def run(self, events, keys):
        self.screen.fill(DARKGRAY)
        self.screen.blit(self.bg_image, (0, 0))

        # Actualizar y dibujar sprites
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

        self.inca.move(keys, 5)
        self.inca.draw(self.screen)
        self.chasqui.draw(self.screen)
        self.obstacles.draw(self.screen)

        # Detectar colisión
        if self.inca.is_collision(self.chasqui):
            self.dialogue.start()
            for event in events:
                self.dialogue.update(event)
            self.dialogue.draw(self.screen)

        elif self.inca.is_collision(self.house):  # Choca con la casa
            return 'ball_game'
        elif self.inca.is_collision(self.hospital):  # Choca con el hospital
            return 'animal_shot'
        
        # Mostrar trofeo si ambos juegos están completados
        if all(self.games_completed.values()) and self.inca.is_collision(self.font):
            self.show_trophy_screen = True  # Mostrar la pantalla del trofeo

        if self.show_trophy_screen:
            bg_rect = self.trophy_bg_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(self.trophy_bg_image, bg_rect.topleft)

            # Dibujar imagen del trofeo
            trophy_rect = self.trophy_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(self.trophy_image, trophy_rect.topleft)
            
            
            # Dibujar texto "Felicidades"
            font = pg.font.Font(None, 36)  # Fuente y tamaño
            text = font.render("Felicidades, sigue aprendiendo", True, (255, 215, 0))  # Texto en dorado
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 225))
            # Dibujar un rectángulo blanco como fondo del texto
            rect_padding = 10  # Espaciado alrededor del texto
            rect = pg.Rect(text_rect.left - rect_padding, text_rect.top - rect_padding, 
                        text_rect.width + rect_padding * 2, text_rect.height + rect_padding * 2)
            pg.draw.rect(self.screen, (255, 255, 255), rect)  # Rectángulo blanco
            self.screen.blit(text, text_rect)
                        # Dibujar un botón de cierre en la esquina superior derecha
            close_button_rect = pg.Rect(WIDTH - 50, 10, 40, 40)  # Botón de cierre
            pg.draw.rect(self.screen, (255, 0, 0), close_button_rect)  # Color rojo para el botón
            close_text = font.render("X", True, (255, 255, 255))  # Texto de "X" blanco
            close_text_rect = close_text.get_rect(center=close_button_rect.center)
            self.screen.blit(close_text, close_text_rect)

            # Detectar clic para cerrar
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if close_button_rect.collidepoint(event.pos):  # Verificar si se hizo clic en el botón
                        self.close_image()  # Llamar a la función de cierre o terminar la pantalla


        return 'main'

class SceneManager:
    def __init__(self, screen):
        try:
            self.screen = screen
            self.scenes = {
                'main': MainScene(screen),
                'ball_game': BallGameScene(screen),
                'animal_shot': AnimalShotScene(screen)
            }
            self.current_scene = 'main'
            self.last_scene = None
            self.change_time = None
        except Exception as e:
            print(f"Error en SceneManager.__init__: {e}")
            raise

    def change_scene(self, scene_name):
        if self.current_scene != scene_name:
            self.last_scene = self.current_scene
            self.current_scene = scene_name
            self.change_time = pg.time.get_ticks()
        #self.current_scene = scene_name

    def reset_scene(self, scene_name):
        if scene_name == 'ball_game':
            self.scenes['ball_game'] = BallGameScene(self.screen)
        elif scene_name == 'animal_shot':
            self.scenes['animal_shot'] = AnimalShotScene(self.screen) 

    def run(self, events, keys):
        if self.change_time and pg.time.get_ticks() - self.change_time > 5000:  # 5 segundos
            if self.last_scene in ['ball_game', 'animal_shot']:
                self.reset_scene(self.last_scene)
            self.change_time = None
        new_scene = self.scenes[self.current_scene].run(events, keys)
        if new_scene != self.current_scene:
            if self.current_scene in ['ball_game', 'animal_shot']:
                self.scenes['main'].games_completed[self.current_scene] = True
            self.change_scene(new_scene)

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    scene_manager = SceneManager(screen)

    running = True
    while running:
        events = pg.event.get()
        keys = pg.key.get_pressed()

        for event in events:
            if event.type == pg.QUIT:
                running = False

        scene_manager.run(events, keys)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()

