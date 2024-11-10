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
        self.text_display_speed = 15  # Velocidad en la que se muestran las letras (mayor número = más lento)
        self.frame_count = 0

        # Dimensiones del cuadro de diálogo
        self.dialogue_box_width = 780
        self.dialogue_box_height = 300
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

import pygame as pg
from .dialogue import Dialogue

class InteractiveDialogue(Dialogue):
    def __init__(self, width, height, text, font_size=30):
        super().__init__(width, height, text, font_size)
        self.text = text.splitlines()  # Divide el texto en líneas
        self.current_line = 0
        self.showing = False  # Indicador de si el diálogo está visible

    def start(self):
        self.current_line = 0
        self.showing = True

    def update(self, event):
        if self.showing:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Al presionar espacio, mostrar todo el diálogo y luego cerrarlo
                    self.current_line = len(self.text)  # Mostrar todo el texto
                    self.showing = False  # Salir del diálogo

    def draw(self, screen):
        # Si el diálogo está activo, muestra el cuadro de diálogo
        if self.showing or self.current_line < len(self.text):
            self.show(screen)
            # Renderizar todo el diálogo de una vez
            for i, line in enumerate(self.text):
                dialogue_surface = self.font.render(line, True, BLACK)
                screen.blit(dialogue_surface, (self.dialogue_box_x + 10, self.dialogue_box_y + 10 + i * 15))

    def reset(self):
        super().reset()  # Reinicia el diálogo
        self.current_line = 0
        self.showing = False
