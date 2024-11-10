# game.py
import pygame as pg
import subprocess
from config import * 
from characters.character import Character
from dialogues.dialogue import InteractiveDialogue
from mobs.mob import Mob
from obstacles.obstacle import Obstacle

pythonVersion = "python"

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    obstacles = pg.sprite.Group()
    mobs = pg.sprite.Group()
    

    bg_image = pg.image.load('assets/floor.jpeg').convert()  # Cambia la ruta a tu imagen de fondo

    # Cargar personajes
    inca = Character('assets/inca.png', WIDTH // 2, HEIGHT // 2 - 80, 50, 50)  # Arriba de la fuente
    chasqui = Character('assets/chasqui.png', WIDTH // 2, HEIGHT // 2 + 80, 50, 50)  # Debajo de la fuente

    """
    # Crear diálogo
    dialogue_text = "Inca: ¡Hola, Chasqui!\nChasqui: ¡Hola, Inca!"
    dialogue = Dialogue(WIDTH, HEIGHT, dialogue_text)
    """
    # Crear diálogos
    dialogue_text = "Inca: ¡Hola, Chasqui!\nChasqui: ¡Hola, Inca!"
    dialogue = InteractiveDialogue(WIDTH, HEIGHT, dialogue_text)

    hospital = Obstacle(0, 0, 150, 150, shape="rect", image="assets/hospital.png", all_sprites=all_sprites, obstacles=obstacles)  # esquina superior izquierda
    Obstacle(WIDTH - 150, 0, 150, 150, shape="rect", image="assets/house.png", all_sprites=all_sprites, obstacles=obstacles)  # esquina superior derecha
    Obstacle(0, HEIGHT - 150, 150, 150, shape="rect", image="assets/market.png", all_sprites=all_sprites, obstacles=obstacles)  # esquina inferior izquierda
    Obstacle(WIDTH - 150, HEIGHT - 150, 150, 150, shape="rect", image="assets/market.png", all_sprites=all_sprites, obstacles=obstacles)  # esquina inferior derecha
    Obstacle(WIDTH // 2, HEIGHT // 2, 200, 200, shape="circle", image="assets/font.png", all_sprites=all_sprites, obstacles=obstacles)  # Círculo en el centro

    house = Obstacle(WIDTH - 150, 0, 150, 150, shape="rect", image="assets/house.png", all_sprites=all_sprites, obstacles=obstacles)  # esquina superior derecha
    citizen_images = [
            pg.transform.scale(pg.image.load('assets/citizen1.png').convert_alpha(), (MOB_SIZE, MOB_SIZE)),
            pg.transform.scale(pg.image.load('assets/citizen2.png').convert_alpha(), (MOB_SIZE, MOB_SIZE)),
            pg.transform.scale(pg.image.load('assets/citizen3.png').convert_alpha(), (MOB_SIZE, MOB_SIZE)),
            ]

    """
    # Crear mobs
    for i in range(5):
        Mob(all_sprites, mobs, citizen_images)
    """
    for i in range(5):
        Mob(all_sprites, mobs, citizen_images, obstacles)

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
                    Mob(all_sprites, mobs, citizen_images)

                dialogue.update(event)
        # Mover al inca con las teclas
        keys = pg.key.get_pressed()
        inca.move(keys, 5)

        if not paused:
            all_sprites.update()

        # Fill the screen and draw background first
        screen.fill(DARKGRAY)
        screen.blit(bg_image, (0, 0))  # Draw background

        all_sprites.draw(screen)
        inca.draw(screen)
        chasqui.draw(screen)

        # Detectar colisión y mostrar diálogo
        if inca.is_collision(chasqui) and not game_won:
            dialogue.start()
            #dialogue.show(screen)
            pg.display.flip()  # Ensure the dialogue is displayed before the next step
                # Aquí podrías tener un bucle adicional para manejar la entrada durante el diálogo
            while dialogue.showing:  # Mantén el diálogo activo mientras esté "mostrando"
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    dialogue.update(event)  # Actualiza el diálogo

                # Dibuja el diálogo en la pantalla
                dialogue.draw(screen)

                pg.display.flip()  # Actualiza la pantalla
                pg.time.delay(100)  # Breve pausa para evitar el uso excesivo de CPU
            #pg.time.delay(2000)  # Pause for 2 seconds to let the player read the dialogue
            dialogue.reset()
            game_won = True
            #subprocess.run([pythonVersion, "AnimalShotLevel/main.py"]) 
        
        elif inca.is_collision(house):  # Si choca con el hospital
            subprocess.run([pythonVersion, "./ball.py"]) 
            collision_occurred = True
        
        elif inca.is_collision(hospital):  # Si choca con la casa
            subprocess.run([pythonVersion, "AnimalShotLevel/main.py"]) 

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

if __name__ == "__main__":
    main()

