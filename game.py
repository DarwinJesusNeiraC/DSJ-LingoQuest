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
            self.dialogue.draw(self.screen)
        elif self.inca.is_collision(self.house):  # Choca con la casa
            return 'ball_game'
        elif self.inca.is_collision(self.hospital):  # Choca con el hospital
            return 'animal_shot'

        return 'main'

class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.scenes = {
            'main': MainScene(screen),
            'ball_game': BallGameScene(screen),
            'animal_shot': AnimalShotScene(screen)
        }
        self.current_scene = 'main'
        self.last_scene = None
        self.change_time = None

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

