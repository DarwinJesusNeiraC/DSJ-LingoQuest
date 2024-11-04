import pygame

# Colores
CAFE_OSCURO = (101, 67, 33)
CAFE_CLARO = (205, 133, 63)
BLACK = (0, 0, 0)

class Dialogue:
    def __init__(self, screen_width, screen_height, dialogue_text, font_size=36):
        self.font = pygame.font.Font(None, font_size)
        self.dialogue_text = dialogue_text
        self.dialogue_lines = dialogue_text.split("\n")
        self.current_text = ""
        self.current_char_index = 0
        self.text_display_speed = 2  # Velocidad en la que se muestran las letras (mayor número = más lento)
        self.frame_count = 0

        # Dimensiones del cuadro de diálogo
        self.dialogue_box_width = 400
        self.dialogue_box_height = 100
        self.dialogue_box_x = (screen_width - self.dialogue_box_width) // 2  # Centrar el cuadro
        self.dialogue_box_y = screen_height - self.dialogue_box_height - 20  # Abajo, con un margen de 20px

    def show(self, screen):
        # Dibujar el fondo del cuadro de diálogo (color café claro)
        pygame.draw.rect(screen, CAFE_CLARO, 
                         (self.dialogue_box_x, self.dialogue_box_y, self.dialogue_box_width, self.dialogue_box_height))

        # Dibujar el borde del cuadro de diálogo (color café oscuro)
        pygame.draw.rect(screen, CAFE_OSCURO, 
                         (self.dialogue_box_x, self.dialogue_box_y, self.dialogue_box_width, self.dialogue_box_height), 5)

        # Control del texto progresivo
        self.frame_count += 1
        if self.frame_count % self.text_display_speed == 0 and self.current_char_index < len(self.dialogue_text):
            self.current_text += self.dialogue_text[self.current_char_index]
            self.current_char_index += 1

        # Dibujar el texto progresivo
        for i, line in enumerate(self.current_text.split("\n")):
            dialogue_surface = self.font.render(line, True, BLACK)
            screen.blit(dialogue_surface, (self.dialogue_box_x + 20, self.dialogue_box_y + 20 + i * 30))  # Posición con margen

    def reset(self):
        self.current_text = ""
        self.current_char_index = 0
        self.frame_count = 0


# dialogues/dialogue.py
import pygame as pg

class InteractiveDialogue:
    def __init__(self, width, height, text):
        self.width = width
        self.height = height
        #self.text = text.split('\n')  # Divide el texto en líneas
        self.text = text.splitlines()
        self.current_line = 0
        self.showing = False

    def start(self):
        self.current_line = 0
        self.showing = True

    def update(self, event):
        if self.showing:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Avanza a la siguiente línea
                    self.current_line += 1
                    if self.current_line >= len(self.text):
                        self.showing = False
                elif event.key == pg.K_ESCAPE or event.key == pg.K_q:  # Sale del diálogo
                    self.showing = False
                    self.current_line = 0

    def draw(self, screen):
        if self.showing and self.current_line < len(self.text):
            font = pg.font.Font(None, 36)
            text_surface = font.render(self.text[self.current_line], True, (255, 255, 255))
            screen.blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, self.height // 2))

    def reset(self):
        self.current_line = 0
        self.showing = False
