'''
# @Author      : Darwin Neira Carrasco 
# @Email       : dneirac@unsa.edu.pe
# @File        : ball
#
# @Description : 
'''
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.5
BOUNCE_FACTOR = 0.7  # Bounce factor
SCORE_ZONE_COLOR = (50, 150, 255)  # Color for score zones
CORRECT_ANSWER = "-kuna"  # Set the correct answer to OP4 (for -kuna)

# Define positions for scoring zones
score_zone_width, score_zone_height = 80, 80  # Size of answer boxes
score_zone_labels = ["-wan", "-kama", "-paq", "-kuna", "-pi"]  # Labels for each box
score_zone_positions = [
    (WIDTH // 2 - 2 * (score_zone_width + 20), HEIGHT // 4),
    (WIDTH // 2 - score_zone_width - 20, HEIGHT // 4),
    (WIDTH // 2, HEIGHT // 4),  
    (WIDTH // 2 + score_zone_width + 20, HEIGHT // 4),
    (WIDTH // 2 + 2 * (score_zone_width + 20), HEIGHT // 4),
]

# Ball class
class Ball:
    def __init__(self, x, y):
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 15)
        self.rect = self.image.get_rect(center=(x, y))
        self.start_pos = (x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.is_moving = False
        self.message = ""
        self.message_color = WHITE
        self.message_rect = pygame.Rect(0, 0, 0, 0)
        self.message_display_time = 0  # Time to display message
        self.display_message_duration = 1000  # 1 second in milliseconds

    def push(self, force):
        self.velocity += force

    def update(self, point_controller, score_zones):
        if self.is_moving:
            self.velocity.y += GRAVITY
            self.rect.move_ip(self.velocity.x, self.velocity.y)

            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.velocity.y *= -BOUNCE_FACTOR
                if abs(self.velocity.y) < 1:
                    self.velocity.y = 0
                    self.is_moving = False

            for zone in score_zones:
                if self.rect.colliderect(zone.rect):
                    if zone.label == CORRECT_ANSWER:
                        point_controller.add_points(50)
                        self.message = "¡Excelente!"
                        self.message_color = (0, 255, 0)  # Green for correct answer
                    else:
                        self.message = "UPS, te equivocaste"
                        self.message_color = (255, 0, 0)  # Red for incorrect answer
                    self.is_moving = False
                    self.velocity = pygame.Vector2(0, 0)
                    self.update_message_rect()
                    self.message_display_time = pygame.time.get_ticks() + self.display_message_duration  # Set the display time
                    break

            if self.rect.left < 0:
                self.rect.left = 0
                self.velocity.x = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.velocity.x = 0
            if self.rect.top < 0:
                self.rect.top = 0
                self.velocity.y = 0

        # Reset position if message display time is over
        if self.message and pygame.time.get_ticks() >= self.message_display_time:
            self.reset_position()

    def reset_position(self):
        self.rect.center = self.start_pos
        self.velocity = pygame.Vector2(0, 0)
        self.is_moving = False
        self.message = ""  # Clear message when resetting

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.message:
            pygame.draw.rect(surface, (30, 144, 255), self.message_rect, border_radius=10)
            message_text = font.render(self.message, True, self.message_color)
            surface.blit(message_text, (self.message_rect.x + 10, self.message_rect.y + 10))

    def update_message_rect(self):
        # Create a new rect based on the message size
        message_surface = font.render(self.message, True, self.message_color)
        self.message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

# Answer box class
class AnswerBox:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label

    def draw(self, surface, font):
        pygame.draw.rect(surface, SCORE_ZONE_COLOR, self.rect)
        text = font.render(self.label, True, WHITE)
        surface.blit(text, (self.rect.x + 10, self.rect.y + 10))

# Point controller class
class PointController:
    def __init__(self):
        self.score = 0

    def add_points(self, points):
        self.score += points
        print(f"Points added: {points}, Total score: {self.score}")

# Trajectory class
class Trajectory:
    def __init__(self):
        self.dots = []

    def update_dots(self, ball_pos, force, dot_spacing=0.1):
        self.dots.clear()
        for i in range(20):
            time = i * dot_spacing
            x = ball_pos[0] + force.x * time
            y = ball_pos[1] + force.y * time - (0.5 * GRAVITY * time**2)
            self.dots.append((x, y))

    def draw(self, surface):
        for dot in self.dots:
            pygame.draw.circle(surface, WHITE, (int(dot[0]), int(dot[1])), 3)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ball = Ball(WIDTH // 2, HEIGHT - 200)
trajectory = Trajectory()
point_controller = PointController()

# Initialize answer boxes
font = pygame.font.Font(None, 36)
answer_boxes = [AnswerBox(x, y, score_zone_width, score_zone_height, label) 
                for label, (x, y) in zip(score_zone_labels, score_zone_positions)]

# Dragging variables
dragging = False
start_pos = None
show_question = True

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click
                dragging = True
                start_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left-click
                dragging = False
                end_pos = pygame.mouse.get_pos()
                force = pygame.Vector2(start_pos[0] - end_pos[0], start_pos[1] - end_pos[1])
                ball.push(force * 0.1)
                ball.is_moving = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Skip question
                show_question = False

    if dragging:
        end_pos = pygame.mouse.get_pos()
        force = pygame.Vector2(start_pos[0] - end_pos[0], start_pos[1] - end_pos[1])
        trajectory.update_dots(ball.rect.center, force * 0.1)

    # Update ball and answer boxes
    ball.update(point_controller, answer_boxes)

    # Drawing
    screen.fill((0, 0, 0))  # Background
    ball.draw(screen)
    trajectory.draw(screen)

    if show_question:
        pygame.draw.rect(screen, (30, 144, 255), pygame.Rect(WIDTH // 2 - 200, 50, 400, 50), border_radius=10)
        question_text = font.render("¿Cuál es el sufijo que denota plural en el idioma quechua?", True, BLACK)
        screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 65))

    for box in answer_boxes:
        box.draw(screen, font)

    pygame.display.flip()
    clock.tick(60)

