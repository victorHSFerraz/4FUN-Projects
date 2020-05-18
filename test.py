import math
import pygame
from random import randint
from pygame import mixer


# Inicializa o programa
pygame.init()

# Cria a tela do jogo
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("bg.jpg")

# Background sound
mixer.music.load("backgroundsound.mp3")
mixer.music.play(-1)

# Titulo e icone
pygame.display.set_caption("Project One")
icon = pygame.image.load("save.png")
pygame.display.set_icon(icon)

# Player img e posicionamento inicial
playerImg = pygame.image.load("playerRocket.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy img, posicionamento inicial randomico e movimentação
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(randint(0, 736))
    enemyY.append(randint(50, 150))
    enemyX_change.append(0.7)
    enemyY_change.append(35)


# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# GAME OVER
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render(f"Score {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (round(x), round(y)))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (round(200), round(250)))


def player(x, y):
    screen.blit(playerImg, (round(x), round(y)))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (round(x), round(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (round(x + 25), round(y - 45)))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 30:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB background
    screen.fill((1, 17, 28))

    # Background
    screen.blit(background, (0, 0))

    # Fechar o jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left arrow is pressed...")
                playerX_change = -1.3
            if event.key == pygame.K_RIGHT:
                print("Right arrow is pressed...")
                playerX_change = 1.3
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("lasersound.wav")
                bullet_sound.play()
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Released...")
                playerX_change = 0

    # Mover o player
    playerX += playerX_change

    # Limitar tela
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = randint(0, 736)
            enemyY[i] = randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    # Chamar a função player/enemy para desenha-lo na tela
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
