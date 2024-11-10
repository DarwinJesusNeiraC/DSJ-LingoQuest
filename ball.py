import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Preguntas en Quechua")

fondo = pygame.image.load("background_ball.jpg")  
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT)) 

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

# Posición inicial de la pelota
ball_pos = [400, 400]
ball_radius = 20
is_dragging = False  # Si el usuario está preparando el lanzamiento
is_launched = False  # Si la pelota ya fue lanzada
velocity_x = 0
velocity_y = 0
gravity = 0.5

# Preguntas y respuestas
preguntas = [
    {"texto": "¿Cuál es el sufijo que denota plural en el idioma quechua?", "respuesta": "-kuna"},
    {"texto": "¿Cuál es el sufijo que denota para en el idioma quechua?", "respuesta": "-paq"},
    {"texto": "¿Cuál es el sufijo que denota en 'en' el idioma quechua?", "respuesta": "-pi"},
    {"texto": "¿Cuál es el sufijo que denota 'hasta' en el idioma quechua?", "respuesta": "-kama"},
    {"texto": "¿Cuál es el sufijo que denota 'con' en el idioma quechua?", "respuesta": "-wan"},
]
pregunta_actual = 0

# Opciones de respuesta en cajas
cajas = [
    {"texto": "-wan", "mensaje_error": "Incorrecto: - WAN: indica la preposición “con” y la conjunción “y”"},
    {"texto": "-kama", "mensaje_error": "Incorrecto: - KAMA: reemplaza la preposición “hasta”"},
    {"texto": "-paq", "mensaje_error": "Incorrecto: - PAQ: reemplaza la preposición “para”"},
    {"texto": "-kuna", "mensaje_error": "Incorrecto: - KUNA: Pluraliza"},
    {"texto": "-pi", "mensaje_error": "Incorrecto: - PI: reemplaza la preposición “en”"}
]
cajas_posiciones = [(150 + i * 120, 150) for i in range(len(cajas))]

# Variables de puntaje y estado del juego
mensaje = ""
font = pygame.font.Font(None, 28)

# Función para calcular la guía de puntos
def calcular_guia_puntos(start_pos, vel_x, vel_y, num_puntos=15):
    puntos = []
    temp_x, temp_y = start_pos
    temp_vel_y = vel_y

    for i in range(num_puntos):
        temp_x += vel_x
        temp_y += temp_vel_y
        temp_vel_y += gravity  # La gravedad afecta la trayectoria en Y
        puntos.append((int(temp_x), int(temp_y)))
    return puntos

# Bucle principal del juego
running = True
while running:
    #screen.fill(WHITE)
    screen.blit(fondo,(0,0))

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_dragging = True
            start_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and is_dragging:
            is_dragging = False
            is_launched = True
            end_pos = pygame.mouse.get_pos()
            velocity_x = (end_pos[0] - start_pos[0]) * 0.1
            velocity_y = (end_pos[1] - start_pos[1]) * 0.1

    # Mostrar pregunta actual
    pregunta_texto = font.render(preguntas[pregunta_actual]["texto"], True, BLACK)
    screen.blit(pregunta_texto, (WIDTH // 2 - pregunta_texto.get_width() // 2, 50))

    # Mostrar las cajas de respuestas
    for i, caja in enumerate(cajas):
        x, y = cajas_posiciones[i]
        pygame.draw.rect(screen, GREY, (x, y, 100, 50))
        texto = font.render(caja["texto"], True, BLACK)
        screen.blit(texto, (x + 10, y + 10))

    # Mostrar mensaje de resultado
    if mensaje:
        mensaje_texto = font.render(mensaje, True, RED if "error" in mensaje else GREEN)
        screen.blit(mensaje_texto, (WIDTH // 2 - mensaje_texto.get_width() // 2, HEIGHT - 50))

    # Mostrar la guía de puntos si está arrastrando
    if is_dragging:
        current_pos = pygame.mouse.get_pos()
        guia_puntos = calcular_guia_puntos(ball_pos, (current_pos[0] - start_pos[0]) * 0.1, (current_pos[1] - start_pos[1]) * 0.1)
        for punto in guia_puntos:
            pygame.draw.circle(screen, GREY, punto, 5)

    if is_launched:
        # Actualizar posición de la pelota
        ball_pos[0] += velocity_x
        ball_pos[1] += velocity_y
        velocity_y += gravity

        # Detectar colisión con las cajas
        ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)
        for i, caja in enumerate(cajas):
            caja_rect = pygame.Rect(cajas_posiciones[i][0], cajas_posiciones[i][1], 100, 50)
            if ball_rect.colliderect(caja_rect):
                # Verificar si la respuesta es correcta
                if caja["texto"] == preguntas[pregunta_actual]["respuesta"]:
                    mensaje = "¡Correcto!"
                    pregunta_actual += 1  # Avanzar a la siguiente pregunta
                    if pregunta_actual >= len(preguntas):
                        mensaje = "¡Felicidades! Has completado el juego"
                        running = False
                else:
                    mensaje = caja["mensaje_error"]
                
                # Resetear pelota y terminar lanzamiento
                ball_pos = [400, 400]
                is_launched = False
                break

    # Dibujar la pelota
    pygame.draw.circle(screen, GREEN, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()

