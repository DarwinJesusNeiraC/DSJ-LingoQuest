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
BLACK = (0, 0, 0)
CAFE_OSCURO = (101, 67, 33)  # Color café oscuro para el borde
CAFE_CLARO = (205, 133, 63)  # Color café claro para el fondo del cuadro de diálogo

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
dialogue_text = "Inca: ¡Hola, Chasqui!\nChasqui: ¡Hola, Inca!"
dialogue_lines = dialogue_text.split("\n")  # Para manejar varias líneas

# Control de texto progresivo
current_text = ""  # El texto actual que se muestra de manera progresiva
current_char_index = 0  # Índice para las letras
text_display_speed = 2  # Velocidad en la que se muestran las letras (mayor número = más lento)
frame_count = 0  # Contador de frames

# Dimensiones del cuadro de diálogo
dialogue_box_width = 400
dialogue_box_height = 100
dialogue_box_x = (WIDTH - dialogue_box_width) // 2  # Centrar el cuadro
dialogue_box_y = HEIGHT - dialogue_box_height - 20  # Abajo, con un margen de 20px

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
    else:
        show_dialogue = False
        current_text = ""  # Reiniciar el texto si no hay colisión
        current_char_index = 0

    # Mostrar el cuadro de diálogo si hay colisión
    if show_dialogue:
        # Dibujar el fondo del cuadro de diálogo (color café claro)
        pygame.draw.rect(screen, CAFE_CLARO, 
                         (dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height))

        # Dibujar el borde del cuadro de diálogo (color café oscuro)
        pygame.draw.rect(screen, CAFE_OSCURO, 
                         (dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height), 5)

        # Control del texto progresivo
        frame_count += 1
        if frame_count % text_display_speed == 0 and current_char_index < len(dialogue_text):
            current_text += dialogue_text[current_char_index]
            current_char_index += 1

        # Dibujar el texto progresivo
        for i, line in enumerate(current_text.split("\n")):
            dialogue_surface = font.render(line, True, BLACK)
            screen.blit(dialogue_surface, (dialogue_box_x + 20, dialogue_box_y + 20 + i * 30))  # Posición con margen

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de FPS
    pygame.time.Clock().tick(30)

pygame.quit()
