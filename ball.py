import pygame as pg

class BallGameScene:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = 800, 600
        self.fondo = pg.image.load("background_ball.jpg")
        self.fondo = pg.transform.scale(self.fondo, (self.WIDTH, self.HEIGHT))

        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.GREY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

        # Variables del juego
        self.ball_pos = [400, 400]
        self.ball_radius = 20
        self.is_dragging = False
        self.is_launched = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.5

        self.preguntas = [
            {"texto": "¿Cuál es el sufijo que denota plural en el idioma quechua?", "respuesta": "-kuna"},
            {"texto": "¿Cuál es el sufijo que denota para en el idioma quechua?", "respuesta": "-paq"},
            {"texto": "¿Cuál es el sufijo que denota 'en' en el idioma quechua?", "respuesta": "-pi"},
            {"texto": "¿Cuál es el sufijo que denota 'hasta' en el idioma quechua?", "respuesta": "-kama"},
            {"texto": "¿Cuál es el sufijo que denota 'con' en el idioma quechua?", "respuesta": "-wan"},
        ]
        self.pregunta_actual = 0

        self.cajas = [
            {"texto": "-wan", "mensaje_error": "Incorrecto: - WAN: indica la preposición “con” y la conjunción “y”"},
            {"texto": "-kama", "mensaje_error": "Incorrecto: - KAMA: reemplaza la preposición “hasta”"},
            {"texto": "-paq", "mensaje_error": "Incorrecto: - PAQ: reemplaza la preposición “para”"},
            {"texto": "-kuna", "mensaje_error": "Incorrecto: - KUNA: Pluraliza"},
            {"texto": "-pi", "mensaje_error": "Incorrecto: - PI: reemplaza la preposición “en”"}
        ]
        self.cajas_posiciones = [(150 + i * 120, 150) for i in range(len(self.cajas))]

        self.mensaje = ""
        self.font = pg.font.Font(None, 28)

        self.launch_time = 0 
        self.reset_time_limit = 1500

    def calcular_guia_puntos(self, start_pos, vel_x, vel_y, num_puntos=15):
        puntos = []
        temp_x, temp_y = start_pos
        temp_vel_y = vel_y

        for i in range(num_puntos):
            temp_x += vel_x
            temp_y += temp_vel_y
            temp_vel_y += self.gravity
            puntos.append((int(temp_x), int(temp_y)))
        return puntos

    def run(self, events, keys):
        self.screen.blit(self.fondo, (0, 0))

        for event in events:
            if event.type == pg.QUIT:
                return 'quit'
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.is_dragging = True
                self.start_pos = pg.mouse.get_pos()
            elif event.type == pg.MOUSEBUTTONUP and self.is_dragging:
                self.is_dragging = False
                self.is_launched = True
                self.launch_time = pg.time.get_ticks()
                end_pos = pg.mouse.get_pos()
                self.velocity_x = (end_pos[0] - self.start_pos[0]) * 0.1
                self.velocity_y = (end_pos[1] - self.start_pos[1]) * 0.1

        # Mostrar pregunta si hay disponible
        if self.pregunta_actual < len(self.preguntas):
            pregunta_texto = self.font.render(self.preguntas[self.pregunta_actual]["texto"], True, self.BLACK)
            self.screen.blit(pregunta_texto, (self.WIDTH // 2 - pregunta_texto.get_width() // 2, 50))
        else:
            return 'main' 

        # Dibujar cajas
        for i, caja in enumerate(self.cajas):
            x, y = self.cajas_posiciones[i]
            pg.draw.rect(self.screen, self.GREY, (x, y, 100, 50))
            texto = self.font.render(caja["texto"], True, self.BLACK)
            self.screen.blit(texto, (x + 10, y + 10))

        # Mostrar mensaje
        if self.mensaje:
            mensaje_texto = self.font.render(self.mensaje, True, self.RED if "Incorrecto" in self.mensaje else self.GREEN)
            self.screen.blit(mensaje_texto, (self.WIDTH // 2 - mensaje_texto.get_width() // 2, self.HEIGHT - 50))

        # Dibujar guía de puntos si está arrastrando
        if self.is_dragging:
            current_pos = pg.mouse.get_pos()
            guia_puntos = self.calcular_guia_puntos(self.ball_pos, (current_pos[0] - self.start_pos[0]) * 0.1, (current_pos[1] - self.start_pos[1]) * 0.1)
            for punto in guia_puntos:
                pg.draw.circle(self.screen, self.GREY, punto, 5)

        # Actualizar posición de la pelota
        if self.is_launched:
            self.ball_pos[0] += self.velocity_x
            self.ball_pos[1] += self.velocity_y
            self.velocity_y += self.gravity

            if self.ball_pos[0] - self.ball_radius < 0: 
                self.ball_pos[0] = self.ball_radius 
                self.velocity_x = -self.velocity_x
            elif self.ball_pos[0] + self.ball_radius > self.WIDTH: 
                self.ball_pos[0] = self.WIDTH - self.ball_radius 
                self.velocity_x = -self.velocity_x
            
            if self.ball_pos[1] - self.ball_radius < 0: 
                self.ball_pos[1] = self.ball_radius 
                self.velocity_y = -self.velocity_y
            elif self.ball_pos[1] + self.ball_radius > self.HEIGHT: 
                self.ball_pos[1] = self.HEIGHT - self.ball_radius 
                self.velocity_y = -self.velocity_y

            ball_rect = pg.Rect(self.ball_pos[0] - self.ball_radius, self.ball_pos[1] - self.ball_radius, self.ball_radius * 2, self.ball_radius * 2)
            for i, caja in enumerate(self.cajas):
                caja_rect = pg.Rect(self.cajas_posiciones[i][0], self.cajas_posiciones[i][1], 100, 50)
                if ball_rect.colliderect(caja_rect):
                    if caja["texto"] == self.preguntas[self.pregunta_actual]["respuesta"]:
                        self.mensaje = "¡Correcto!"
                        self.pregunta_actual += 1
                        if self.pregunta_actual >= len(self.preguntas):
                            self.mensaje = "¡Felicidades! Usa la app para ver el AR"
                            return 'main'
                    else:
                        self.mensaje = caja["mensaje_error"]

                    self.ball_pos = [400, 400]
                    self.is_launched = False
                    break
            if pg.time.get_ticks() - self.launch_time > self.reset_time_limit: 
                self.ball_pos = [400, 400] 
                self.is_launched = False
        # Dibujar pelota
        pg.draw.circle(self.screen, self.GREEN, (int(self.ball_pos[0]), int(self.ball_pos[1])), self.ball_radius)

        pg.display.flip()
        pg.time.delay(30)
        return 'ball_game'

