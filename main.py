import pygame
import random
import math
from pygame import mixer

# intialize the pygame 
pygame.init()

# create a game screen 
screen = pygame.display.set_mode((800, 600))
#Background image
background = pygame.image.load('Background_img.jpg')

#backgroung music
mixer.music.load('background.wav')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon  = pygame.image.load('space.png')
pygame.display.set_icon(icon)

#player 
playerImg = pygame.image.load('spaceship.png')
playerX = 370 #value of x axis of img
playerY = 480 #value of y axis of img
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change  = []
enemyY_change  = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append (pygame.image.load('space_enemy.png'))
    enemyX.append (random.randint(0, 736)) #value of x axis of img
    enemyY.append (random.randint(50, 150)) #value of y axis of img
    enemyX_change.append (1.2)
    enemyY_change.append (40)

#bullet
#Ready state is -> we cant see the bullet on the screen
#Fire state is -> The bullet is currently moving
bulletImg = pygame.image.load('weapon.png')
bulletX = 0 #value of x axis of img
bulletY = 480 #value of y axis of img
bulletX_change = 0
bulletY_change = 3

bullet_state = "ready"  
score_value = 0

font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score,( x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))

def player(x,y):
    #to draw
    screen.blit(playerImg,( x, y))

def enemy(x,y,i):
    #to draw
    screen.blit(enemyImg[i],( x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10)) #for perfect center

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False






#Game loop (to run game !)
running = True
while running:

    #setting game display colour using rgb 
    screen.fill((0,0,0))
    #background_img
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        #checks the quit button is pressed or not
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check weather its right or left 
        #keydown -> is pressing the key
        #keyup -> is relesing the key 
            

        if event.type == pygame.KEYDOWN:
            # print("Keystroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("Leftarrow is pressed")
                playerX_change = -2.5

            if event.key == pygame.K_RIGHT:
                # print("Rightarrow is pressed")
                playerX_change = 2.5

            if event.key == pygame.K_SPACE:
                # print("Buller being fired is pressed")
                if bullet_state == "ready":
                    #get the current x cordinate of the spaceship (kinna lock !)
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke is being realesed")
                playerX_change = 0


    playerX += playerX_change

    #setting up boundries of player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"  
        #resets the bullet for next fire 
    
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    #setting up boundries of enemy
    for i in range(num_of_enemies):
        
        #Game over 
        if enemyY[i] > 455:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1.9
            enemyY[i]+= enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.9
            enemyY[i] += enemyY_change[i]



        #setting up collision module
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)

        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    

    player(playerX, playerY)
    show_score(textX,textY)
    #imp that is used to update display when said/needed 
    pygame.display.update()