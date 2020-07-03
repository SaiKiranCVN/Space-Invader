import pygame as pg
import random
import math
from pygame import mixer

# Initialize th pygame
pg.init()

# Creating the screen
screen = pg.display.set_mode((800, 600))

# Background Image
background = pg.image.load('background.png')

# Background Sounds
mixer.music.load('background.wav') # Mixer.music since we need it in loop
mixer.music.play(-1) # Play in loop, so add -1

# Title and Caption Icon - 32x32
pg.display.set_caption('Space Invaders')
icon = pg.image.load('spaceship.png')
pg.display.set_icon(icon)

# Adding Player
playerImg = pg.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Adding Enemy
# enemyImg = pg.image.load('enemy.png')
# enemyX = random.randint(0, 735)
# enemyY = random.randint(50, 150)
# enemyX_change = 4
# enemyY_change = 40

# Multiple Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pg.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Adding Bullet
bulletImg = pg.image.load('bullet.png')
bulletX = 0
bulletY = 480  # Since, initially our spaceship is at 480px
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'  # Ready - You can't see the bullet, Fire - Bullet is currently moving

#score = 0

# Score
score_value = 0
font = pg.font.Font('freesansbold.ttf',32)

textX = 10
testY = 10

# Game Over Text
over_font = pg.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render('Score : ' + str(score_value), True,(255,255,255)) # True - Display on the screen
    screen.blit(score,(x,y))

def game_over_text():
    over = over_font.render('GAME OVER', True, (255, 255, 255))  # True - Display on the screen
    screen.blit(over, (200, 250))


def player(x, y):
    # blit ==> Draw
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit ==> Draw
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))  # Just to seem bullet comes from the center and front of the spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:  # 27 px
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # Add RGB color
    screen.fill((0, 0, 0))

    # Add Background Image
    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # If key is pressed, check if its left or right
        if event.type == pg.KEYDOWN:
            # print('A key is pressed')
            if event.key == pg.K_LEFT:
                # print('Left Key Pressed')
                playerX_change = -5
            if event.key == pg.K_RIGHT:
                # print('Right Key Pressed')
                playerX_change = 5
            if event.key == pg.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,
                                bulletY)  # If we use playerX instead of bulletX, our bullet follows the spaceship
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                # print('Key Released')
                playerX_change = 0
    playerX += playerX_change
    # Avoid going out of screen
    if playerX <= 0:  # Why didn't we subtract 64 here - since player image pixels start from left hand side
        playerX = 0
    elif playerX >= 736:  # 800 - 64 (since our image is 64*64)
        playerX = 736

    # enemyX += enemyX_change
    # Boundaries of enemy - Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # Why didn't we subtract 64 here - since player image pixels start from left hand side
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800 - 64 (since our image is 64*64)
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # Collision Detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            #print(score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # # Collision Detection
    # collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    # if collision:
    #     bulletY = 480
    #     bullet_state = 'ready'
    #     score += 1
    #     print(score)
    #     enemyX = random.randint(0, 735)
    #     enemyY = random.randint(50, 150)

    player(playerX, playerY)
    # enemy(enemyX, enemyY)
    show_score(textX,testY)
    pg.display.update()
