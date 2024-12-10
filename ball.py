import pygame as pg

# Función que manejará el juego de la pelota
def juego_pelota(screen):
    WIDTH, HEIGHT = 800, 600
    fondo = pg.image.load("background_ball.jpg")  
    fondo = pg.transform.scale(fondo, (WIDTH, HEIGHT)) 

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GREY = (200, 200, 200)
    BLACK = (0, 0, 0)

    # Inicializar variables
    ball_pos = [400, 400]
    ball_radius = 20
    is_dragging = False
    is_launched = False
    velocity_x = 0
    velocity_y = 0
    gravity = 0.5

    preguntas = [
        {"texto": "¿Cuál es el sufijo que denota plural en el idioma quechua?", "respuesta": "-kuna"},
        {"texto": "¿Cuál es el sufijo que denota para en el idioma quechua?", "respuesta": "-paq"},
        {"texto": "¿Cuál es el sufijo que denota en 'en' el idioma quechua?", "respuesta": "-pi"},
        {"texto": "¿Cuál es el sufijo que denota 'hasta' en el idioma quechua?", "respuesta": "-kama"},
        {"texto": "¿Cuál es el sufijo que denota 'con' en el idioma quechua?", "respuesta": "-wan"},
    ]
    pregunta_actual = 0

    cajas = [
        {"texto": "-wan", "mensaje_error": "Incorrecto: - WAN: indica la preposición “con” y la conjunción “y”"},
        {"texto": "-kama", "mensaje_error": "Incorrecto: - KAMA: reemplaza la preposición “hasta”"},
        {"texto": "-paq", "mensaje_error": "Incorrecto: - PAQ: reemplaza la preposición “para”"},
        {"texto": "-kuna", "mensaje_error": "Incorrecto: - KUNA: Pluraliza"},
        {"texto": "-pi", "mensaje_error": "Incorrecto: - PI: reemplaza la preposición “en”"}
    ]
    cajas_posiciones = [(150 + i * 120, 150) for i in range(len(cajas))]

    mensaje = ""
    font = pg.font.Font(None, 28)

    def calcular_guia_puntos(start_pos, vel_x, vel_y, num_puntos=15):
        puntos = []
        temp_x, temp_y = start_pos
        temp_vel_y = vel_y

        for i in range(num_puntos):
            temp_x += vel_x
            temp_y += temp_vel_y
            temp_vel_y += gravity
            puntos.append((int(temp_x), int(temp_y)))
        return puntos

    running = True
    while running:
        screen.blit(fondo, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                is_dragging = True
                start_pos = pg.mouse.get_pos()
            elif event.type == pg.MOUSEBUTTONUP and is_dragging:
                is_dragging = False
                is_launched = True
                end_pos = pg.mouse.get_pos()
                velocity_x = (end_pos[0] - start_pos[0]) * 0.1
                velocity_y = (end_pos[1] - start_pos[1]) * 0.1

        pregunta_texto = font.render(preguntas[pregunta_actual]["texto"], True, BLACK)
        screen.blit(pregunta_texto, (WIDTH // 2 - pregunta_texto.get_width() // 2, 50))

        for i, caja in enumerate(cajas):
            x, y = cajas_posiciones[i]
            pg.draw.rect(screen, GREY, (x, y, 100, 50))
            texto = font.render(caja["texto"], True, BLACK)
            screen.blit(texto, (x + 10, y + 10))

        if mensaje:
            mensaje_texto = font.render(mensaje, True, RED if "error" in mensaje else GREEN)
            screen.blit(mensaje_texto, (WIDTH // 2 - mensaje_texto.get_width() // 2, HEIGHT - 50))

        if is_dragging:
            current_pos = pg.mouse.get_pos()
            guia_puntos = calcular_guia_puntos(ball_pos, (current_pos[0] - start_pos[0]) * 0.1, (current_pos[1] - start_pos[1]) * 0.1)
            for punto in guia_puntos:
                pg.draw.circle(screen, GREY, punto, 5)

        if is_launched:
            ball_pos[0] += velocity_x
            ball_pos[1] += velocity_y
            velocity_y += gravity

            ball_rect = pg.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)
            for i, caja in enumerate(cajas):
                caja_rect = pg.Rect(cajas_posiciones[i][0], cajas_posiciones[i][1], 100, 50)
                if ball_rect.colliderect(caja_rect):
                    if caja["texto"] == preguntas[pregunta_actual]["respuesta"]:
                        mensaje = "¡Correcto!"
                        pregunta_actual += 1
                        if pregunta_actual >= len(preguntas):
                            mensaje = "¡Felicidades! Has completado el juego"
                            running = False
                    else:
                        mensaje = caja["mensaje_error"]

                    ball_pos = [400, 400]
                    is_launched = False
                    break

        pg.draw.circle(screen, GREEN, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

        pg.display.flip()
        pg.time.delay(30)
