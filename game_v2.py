# game.py
import pygame as pg
import subprocess
from config import * 
from characters.character import Character
from dialogues.dialogue import InteractiveDialogue
from mobs.mob import Mob
from obstacles.obstacle import Obstacle

pythonVersion = "python"

def initialize_game():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    
    # Cargar recursos iniciales
    bg_image = pg.image.load('assets/floor.jpeg').convert()  # Fondo
    citizen_images = [
        pg.transform.scale(pg.image.load('assets/citizen1.png').convert_alpha(), (MOB_SIZE, MOB_SIZE)),
        pg.transform.scale(pg.image.load('assets/citizen2.png').convert_alpha(), (MOB_SIZE, MOB_SIZE)),
        pg.transform.scale(pg.image.load('assets/citizen3.png').convert_alpha(), (MOB_SIZE, MOB_SIZE)),
    ]
    
    # Crear grupos de sprites
    all_sprites = pg.sprite.Group()
    obstacles = pg.sprite.Group()
    mobs = pg.sprite.Group()
    
    # Inicializar personajes y otros elementos
    inca = Character('assets/inca.png', WIDTH // 2, HEIGHT // 2 - 80, 50, 50)
    chasqui = Character('assets/chasqui.png', WIDTH // 2, HEIGHT // 2 + 80, 50, 50)
    
    dialogue_text_inca = """
                            Inca: ¡Hola!, 
                            \n¿estás listo para divertirte?
                            \nHoy aprenderemos el idioma de nuestros ancestros
                            \n¡EL QUECHUA! Sí, y será muy divertido
                            \nEn cada lugar hay una nueva temática y un nuevo reto
                            \nSi deseas parender vocabulario sobre animales ve a la casa
                            \nY si deseas reforzar la gramática del quechua ve al hospital
                            \n¡Suerte!
                            \nPresiona la tecla espacio para continuar
                            """
    dialogue_text_chasqui = "Chasqui: ¡Hola, Inca!, claro que sí, ¡vamos a divertirnos!"
    dialogue_inca = InteractiveDialogue(WIDTH, HEIGHT, dialogue_text_inca)
    dialogue_chasqui = InteractiveDialogue(WIDTH, HEIGHT, dialogue_text_chasqui)
    
    # Obstáculos y mobs
    hospital, house = create_obstacles(all_sprites, obstacles)
    create_mobs(all_sprites, mobs, citizen_images, obstacles)
    
    return screen, clock, bg_image, inca, chasqui, dialogue_inca, all_sprites, obstacles, mobs, hospital, house, citizen_images

def create_obstacles(all_sprites, obstacles):
    hospital = Obstacle(0, 0, 150, 150, shape="rect", image="assets/hospital.png", all_sprites=all_sprites, obstacles=obstacles)
    house = Obstacle(WIDTH - 150, 0, 150, 150, shape="rect", image="assets/house.png", all_sprites=all_sprites, obstacles=obstacles)
    Obstacle(0, HEIGHT - 150, 150, 150, shape="rect", image="assets/market.png", all_sprites=all_sprites, obstacles=obstacles)
    Obstacle(WIDTH - 150, HEIGHT - 150, 150, 150, shape="rect", image="assets/market.png", all_sprites=all_sprites, obstacles=obstacles)
    Obstacle(WIDTH // 2, HEIGHT // 2, 200, 200, shape="circle", image="assets/font.png", all_sprites=all_sprites, obstacles=obstacles)
    return hospital, house

def create_mobs(all_sprites, mobs, citizen_images, obstacles):
    for _ in range(5):
        Mob(all_sprites, mobs, citizen_images, obstacles)

def handle_events(inca, dialogue_inca, mobs, all_sprites, citizen_images):
    paused, show_vectors, running = False, False, True
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_SPACE:
                # Si el diálogo está mostrando, se muestra completo y luego se cierra
                if dialogue_inca.showing:
                    dialogue_inca.showing = False  # Cerrar el diálogo al presionar espacio
                else:
                    dialogue_inca.start()  # Iniciar el diálogo si no está mostrando
            elif event.key == pg.K_v:
                show_vectors = not show_vectors
            elif event.key == pg.K_m:
                Mob(all_sprites, mobs, citizen_images)
            dialogue_inca.update(event)
    return paused, show_vectors, running


def update_game_logic(inca, chasqui, house, hospital, dialogue_inca, all_sprites, paused, screen):
    if not paused:
        all_sprites.update()
    inca.move(pg.key.get_pressed(), 5)
    handle_collisions(inca, chasqui, house, hospital, dialogue_inca, screen)

def handle_collisions(inca, chasqui, house, hospital, dialogue_inca, screen):
    global game_won, house_collision_occurred, hospital_collision_occurred
    # Inicializar banderas de colisión si no están ya definidas
    if 'house_collision_occurred' not in globals():
        house_collision_occurred = False
    if 'hospital_collision_occurred' not in globals():
        hospital_collision_occurred = False
    # Colisión con el personaje "chasqui"
    if inca.is_collision(chasqui) and not game_won:
        dialogue_inca.start()
        handle_dialogue_loop(dialogue_inca, screen)
        game_won = True
    # Colisión con la casa (solo una vez)
    elif inca.is_collision(house) and not house_collision_occurred:
        subprocess.run([pythonVersion, "./ball.py"])
        house_collision_occurred = True  # Marcar que la colisión con la casa ya ocurrió
    # Colisión con el hospital (solo una vez)
    elif inca.is_collision(hospital) and not hospital_collision_occurred:
        subprocess.run([pythonVersion, "AnimalShotLevel/main.py"])
        hospital_collision_occurred = True  # Marcar que la colisión con el hospital ya ocurrió
    # Reinicio del diálogo y del estado de victoria si no hay colisión con "chasqui"
    elif not inca.is_collision(chasqui):
        dialogue_inca.reset()
        game_won = False


def handle_dialogue_loop(dialogue, screen):
    running = True
    while dialogue.showing and running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            dialogue.update(event)
            
        dialogue.draw(screen)
        pg.display.flip()
        pg.time.delay(100)
    dialogue.reset()

def draw_screen(screen, bg_image, all_sprites, inca, chasqui, dialogue_inca, show_vectors, mobs):
    screen.fill(DARKGRAY)
    screen.blit(bg_image, (0, 0))
    all_sprites.draw(screen)
    inca.draw(screen)
    chasqui.draw(screen)
    if show_vectors:
        for sprite in mobs:
            sprite.draw_vectors()
    pg.display.flip()

def main():
    screen, clock, bg_image, inca, chasqui, dialogue_inca, all_sprites, obstacles, mobs, hospital, house, citizen_images = initialize_game()
    paused, show_vectors, running, game_won = False, False, True, False
    
    while running:
        clock.tick(FPS)
        paused, show_vectors, running = handle_events(inca, dialogue_inca, mobs, all_sprites, citizen_images)
        update_game_logic(inca, chasqui, house, hospital, dialogue_inca, all_sprites, paused, screen)
        draw_screen(screen, bg_image, all_sprites, inca, chasqui, dialogue_inca, show_vectors, mobs)
        pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    
    pg.quit()

if __name__ == "__main__":
    main()
