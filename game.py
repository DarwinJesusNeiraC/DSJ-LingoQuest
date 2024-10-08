import pygame
from pygame.locals import *
from character import Character
from dialogue import Dialogue

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inca y Chasqui")

# Colores
WHITE = (255, 255, 255)

# Cargar personajes
inca = Character('assets/inca.png', 100, 100, 50, 50)
chasqui = Character('assets/chasqui.png', 400, 300, 50, 50)

# Crear diálogo
dialogue_text = "Inca: ¡Hola, Chasqui!\nChasqui: ¡Hola, Inca!"
dialogue = Dialogue(WIDTH, HEIGHT, dialogue_text)

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Mover al inca con las teclas
    keys = pygame.key.get_pressed()
    inca.move(keys, 5)

    # Dibujar personajes
    inca.draw(screen)
    chasqui.draw(screen)

    # Detectar colisión y mostrar diálogo
    if inca.is_collision(chasqui):
        dialogue.show(screen)
    else:
        dialogue.reset()

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de FPS
    pygame.time.Clock().tick(30)

pygame.quit()
