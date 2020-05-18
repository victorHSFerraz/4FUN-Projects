import pygame
from random import randint

# Inicializa o programa
pygame.init()

# Cria a tela do jogo
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("bg.jpg")

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
enemyImg = pygame.image.load("enemy.png")
enemyX = randint(0, 736)
enemyY = randint(50, 150)
enemyX_change = 0.7
enemyY_change = 35

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"


def player(x, y):
    screen.blit(playerImg, (round(x), round(y)))


def enemy(x, y):
    screen.blit(enemyImg, (round(x), round(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (round(x + 25), round(y - 45)))


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

    # Mover o enemy
    enemyX += enemyX_change

    # Enemy Movement
    if enemyX <= 0:
        enemyX_change = 1.2
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -1.2
        enemyY += enemyY_change

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Chamar a função player/enemy para desenha-lo na tela
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
