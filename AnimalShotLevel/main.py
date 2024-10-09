import pygame
import math
import random
from pygame import mixer
import os
pygame.init()

#mixer.music.load('assets/music.mp3')  # Reemplaza con el archivo de música que desees
game_won = False
mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/music.mp3'))

mixer.music.play(-1)
screen = pygame.display.set_mode((800, 600))

#background = pygame.transform.scale(pygame.image.load('assets/background.jpg'), (800, 600))
background = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/background.jpg')), (800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
#icon = pygame.image.load('assets/ufo.png')
icon = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/ufo.png'))

pygame.display.set_icon(icon)

# Player
#playerImg = pygame.image.load('assets/ufo.png')
playerImg = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/ufo.png'))

player_width = playerImg.get_width()
player_height = playerImg.get_height()
player_scaled = pygame.transform.scale(playerImg, (int(player_width * 0.2), int(player_height * 0.2)))
playerX = 300
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# static positions
static_positions = [(20, 100), (100, 120), (200, 140), (300, 160), (450, 180), (600, 200)]


animal_images = [os.path.join(os.path.dirname(__file__), 'assets/cat.png'),
                 os.path.join(os.path.dirname(__file__), 'assets/dog.png'),
                 os.path.join(os.path.dirname(__file__), 'assets/fox.png'),
                 os.path.join(os.path.dirname(__file__), 'assets/dove.png'),
                 os.path.join(os.path.dirname(__file__), 'assets/star.png'),
                 os.path.join(os.path.dirname(__file__), 'assets/full-moon.png')]
#animal_images = ['assets/cat.png', 'assets/dog.png', 'assets/fox.png', 'assets/dove.png', 'assets/star.png', 'assets/full-moon.png']


# animal names in Quechua
animal_names = ['michi', 'alqo', 'atoq', 'urpi', 'chaska', 'killa']


# Crear el diccionario
animal_dict = dict(zip(animal_names, animal_images))


# random animal to show
current_animal = random.choice(animal_names)
current_animal_index = animal_names.index(current_animal)

# counts
correct_counter = 0
incorrect_counter = 0
#lives
lives = 3 

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Nueva función para mostrar el contador de vidas
def show_lives():
    lives_text = font.render("Lives: " + str(lives), True, (255, 0, 0))
    screen.blit(lives_text, (350, 10))  # Posicionada en el centro superior de la pantalla


for i, (animal_name, image_path) in enumerate(animal_dict.items()):
    enemy_original = pygame.image.load(animal_images[i])
    enemy_width = enemy_original.get_width()
    enemy_height = enemy_original.get_height()
    #resize img
    enemy_scaled = pygame.transform.scale(enemy_original, (int(enemy_width * 0.1), int(enemy_height * 0.1)))
    enemyImg.append(enemy_scaled)
    enemyX.append(static_positions[i][0])  # x position
    enemyY.append(static_positions[i][1])  # y position
    #movement speed
    enemyX_change.append(0.05)  #right
    enemyY_change.append(5)  #descenso de 5 píxeles cuando llega al borde

# Bullet
bulletImg = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/bullet.png'))

#bulletImg = pygame.image.load('assets/bullet.png')
bullet_width = bulletImg.get_width()
bullet_height = bulletImg.get_height()
bullet_scaled = pygame.transform.scale(bulletImg, (int(bullet_width * 0.1), int(bullet_height * 0.1)))

bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))
    time.sleep(2)
    subprocess.run(["python", "QuechuaGame/main.py"])  # Restart if lost

def player(x, y):
    screen.blit(player_scaled, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_scaled, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return  distance < 27

#current_animal = random.choice(animal_names)
#current_animal_index = animal_names.index(current_animal)

def show_animal_name():
    #random word in the screen
    if current_animal != None:
        animal_text = font.render("Find -> " + current_animal, True, (255, 255, 255))
        screen.blit(animal_text, (550, 10))
    else:
        show_victory_text()

used_animals = []
# choose new word
def choose_new_animal():
    if animal_dict:
        current_animal = random.choice(list(animal_dict.keys()))
        return current_animal
    else:
        return None

    
# winner sms
def show_victory_text():
    global game_won
    victory_text = over_font.render("Game won!", True, (0, 255, 0))
    screen.blit(victory_text, (200, 250))
    game_won = True  # Set the flag when the game is won


# Game Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
    
                # key A to change the word
            if event.key == pygame.K_a:
                if animal_names:  
                    current_animal, current_animal_index = choose_new_animal()
                    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    i = 0
    while i < len(enemyX):
        # Game Over
        if lives == 0:
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.05
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.05
            enemyY[i] += enemyY_change[i]

        # Manejando colisiones
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #explosion_Sound = mixer.Sound('assets/explosion.mp3')
            explosion_Sound = mixer.Sound(os.path.join(os.path.dirname(__file__), 'assets/explosion.mp3'))

            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"

            if list(animal_dict.keys()).index(current_animal) == i:
                correct_counter += 1  # correcto
                score_value = correct_counter
                print(f"¡Correcto! Contador: {correct_counter}")
                del animal_dict[current_animal]  # Eliminar la palabra del diccionario
                # Elegir un nuevo animal
                if animal_dict:
                    current_animal = choose_new_animal()
                else:
                    print("¡Todas las palabras han sido adivinadas!")

                    show_victory_text()
                    running= False
                    break
                            # Eliminar el enemigo y actualizar listas
                enemyImg.pop(i)
                enemyX.pop(i)
                enemyY.pop(i)
                enemyX_change.pop(i)
                enemyY_change.pop(i)
                num_of_enemies -= 1

                # No incrementar `i`, ya que el siguiente enemigo ahora está en la misma posición
                continue
            else:
                lives -= 1
                                # Eliminar el enemigo incorrecto
                del animal_dict[list(animal_dict.keys())[i]]
                enemyImg.pop(i)
                enemyX.pop(i)
                enemyY.pop(i)
                enemyX_change.pop(i)
                enemyY_change.pop(i)
                num_of_enemies -= 1
                            # Elegir un nuevo animal para reemplazar al incorrecto
                if animal_dict:
                    current_animal = choose_new_animal()
                else:
                    print("¡Todas las palabras han sido adivinadas!")
                    show_victory_text()
                    running= False
                    break
                continue


        enemy(enemyX[i], enemyY[i], i)
        i += 1

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_lives()

    show_score(textX, textY)
    show_animal_name()  
    pygame.display.update()

if game_won:
    print("You won the game! Returning to the main program...")
