# to format the code ctrl+alt+l
import pygame
import random
import math

from pygame import mixer

# initialize the pygame
pygame.init()

# create window
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background1.png')

#background Sound
mixer.music.load('backgroundMusic.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')  # instance of image captured in icon variable
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('enemy.png'))
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(4)
    EnemyY_change.append(40)

# Bullet
# ready state : you cant see the bullet on the screen
# fire state: the bullet is currently moving
#
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',70)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    OVER_TEXT = over_font.render("GAME OVER" , True,(255, 255, 255))
    screen.blit(OVER_TEXT, (200,250))

def player(X, Y):
    screen.blit(playerImg, (X, Y))

def Enemy(X, Y, i):
    screen.blit(EnemyImg[i], (X, Y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if (distance <= 27):
        return True
    else:
        return False


# game loop
running = True
while running:
    # RBG - red,green,blue
    screen.fill((0, 0, 0))
    # background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if (event.type == pygame.KEYDOWN):  # KEYDOWN is pressing any button on keyboard
            if (event.key == pygame.K_LEFT):
                playerX_change = -5
            if (event.key == pygame.K_RIGHT):
                playerX_change = 5
            if (event.key == pygame.K_SPACE):
                if (bullet_state is "ready"):  # checks if the bullet on the screen or not if it is not on the screen
                    bullet_Sound=mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX  # then its fires that is gets current state of player
                    fire_bullet(bulletX, bulletY)  # playerX=current position of spaceship and bulletY=480

        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                playerX_change = 0

    # Restricting the player so that it doesnt go outside the boundary
    playerX = playerX + playerX_change
    if (playerX < 0):  # playerX means player's X coordinate
        playerX = 0
    elif (playerX >= 736):
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        #Game Over
        if(EnemyY[i]>400):
            for j in range(num_of_enemies):
                EnemyY[j]=2000 #removing all the enemy out of the screen
            game_over_text()
            break
        EnemyX[i] = EnemyX[i] + EnemyX_change[i]
        if (EnemyX[i] < 0):  # EnemyX means Enemy's X coordinate
            EnemyX_change[i] = 4
            EnemyY[i] += EnemyY_change[i]
        elif (EnemyX[i] >= 736):
            EnemyX_change[i] = -4
            EnemyY[i] += EnemyY_change[i]

        # collision
        collision = isCollision(EnemyX[i], EnemyY[i], bulletX,
                                bulletY)  # true or false will be returning from isCollision
        if (collision):
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.play()
            bulletY = 480  # resetting bullet position to starting position of player
            bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(50, 150)
        Enemy(EnemyX[i], EnemyY[i], i)  # calling Enemy method

    # Bullet movement
    if (bulletY <= 0):
        bulletY = 480
        bullet_state = "ready"

    if (bullet_state is "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # calling player method
    show_score(textX, textY)
    pygame.display.update()
