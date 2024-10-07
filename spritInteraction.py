import pygame
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inca y Chasqui")

# Colores
WHITE = (255, 255, 255)

# Cargar imágenes de los personajes (Inca y Chasqui)
inca_image = pygame.image.load('assets/inca.png')  # Coloca la imagen del inca aquí
chasqui_image = pygame.image.load('assets/chasqui.png')  # Coloca la imagen del chasqui aquí

# Escalar imágenes (opcional)
inca_image = pygame.transform.scale(inca_image, (50, 50))
chasqui_image = pygame.transform.scale(chasqui_image, (50, 50))

# Posiciones iniciales
inca_x, inca_y = 100, 100
chasqui_x, chasqui_y = 400, 300

# Velocidad del inca
inca_speed = 5

# Fuente de texto
font = pygame.font.Font(None, 36)

# Variables de estado
show_dialogue = False
dialogue_text = ""

# Función para detectar colisiones entre los personajes
def is_collision(inca_x, inca_y, chasqui_x, chasqui_y):
    inca_rect = pygame.Rect(inca_x, inca_y, 50, 50)
    chasqui_rect = pygame.Rect(chasqui_x, chasqui_y, 50, 50)
    return inca_rect.colliderect(chasqui_rect)

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)
    
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Obtener teclas presionadas
    keys = pygame.key.get_pressed()

    # Movimiento del inca
    if keys[K_LEFT]:
        inca_x -= inca_speed
    if keys[K_RIGHT]:
        inca_x += inca_speed
    if keys[K_UP]:
        inca_y -= inca_speed
    if keys[K_DOWN]:
        inca_y += inca_speed

    # Dibujar los personajes
    screen.blit(inca_image, (inca_x, inca_y))
    screen.blit(chasqui_image, (chasqui_x, chasqui_y))

    # Detectar colisión y mostrar diálogo
    if is_collision(inca_x, inca_y, chasqui_x, chasqui_y):
        show_dialogue = True
        dialogue_text = "Inca: ¡Hola, Chasqui!\nChasqui: ¡Hola, Inca!"
    else:
        show_dialogue = False

    # Mostrar el diálogo si hay colisión
    if show_dialogue:
        dialogue_surface = font.render(dialogue_text, True, (0, 0, 0))
        screen.blit(dialogue_surface, (50, 50))

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de FPS
    pygame.time.Clock().tick(30)

pygame.quit()
