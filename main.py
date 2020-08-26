import pygame
import random
import math
from pygame import mixer

pygame.init()
game = 0
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('./img/background.png')
mixer.music.load('./msc/back.wav')
mixer.music.play(-1)
pygame.display.set_caption("space")
icon = pygame.image.load('./img/ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('./img/spaceship.png')
playerx = 370
playery = 500
playerx_change = 0
playery_change = 0

# enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_enemies = 6
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('./img/enemy.png'))
    enemyx.append(random.randint(0, 600))
    enemyy.append(50)
    enemyx_change.append(2.2)
    enemyy_change.append(30)

# bullet
bulletImg = pygame.image.load('./img/bullet.png')
bulletx = 0
bullety = 500
bulletx_change = 0
bullety_change = 7.69
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 69)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))
    global game
    if game == 0:
        expl_sound = mixer.Sound('./msc/explosion.wav')
        expl_sound.play()
        game += 1


def show_score(x, y):
    score = font.render("SCORE:" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    # rbg
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = +5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('./msc/laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # boundry
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    # enemy mov
    for i in range(num_enemies):

        # game over
        if enemyy[i] > 100:
            for j in range(num_enemies):
                enemyy[j] = 2000
            game_over_text()
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 2.2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -2.2
            enemyy[i] += enemyy_change[i]
        # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 600)
            enemyy[i] = random.randint(30, 50)
        enemy(enemyx[i], enemyy[i], i)
    # bullet movement
    if bullety <= 0:
        bullety = 500
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
