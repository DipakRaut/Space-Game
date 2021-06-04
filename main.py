import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Screen Dimension
screen = pygame.display.set_mode((500,400)) # 500 is the width and 400 is the height

# Adding Background Image
background = pygame.image.load("back.png")

# Title and Icon
pygame.display.set_caption("Space Guardians")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Adding BackGround Sound
mixer.music.load("BackGround.mp3")
mixer.music.play(-1)

# Player
playerimg = pygame.image.load("player.png")
playerX = 235
playerY = 350
velocity = 0


# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemy_velocity_X = []
enemy_velocity_Y = []
no_of_enemies = 6

for i in range(no_of_enemies):
	enemyimg.append(pygame.image.load("alien.png"))
	enemyX.append(random.randint(0,480))
	enemyY.append(random.randint(50,150))
	enemy_velocity_X.append(0.5)
	enemy_velocity_Y.append(40)

# Bullet
# Ready State -> You can't see the bullets on the screen 
# Fire -> The Bullet is Currently moving
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 350
bullet_velocity_X = 0
bullet_velocity_Y = 2
bullet_state = "Ready"

# Counting the score
score = 0
font = pygame.font.Font("freesansbold.ttf", 24) # dafont visit this sites for various fonts 

textX = 10
textY = 10

# Game over Text
over_font = pygame.font.Font("freesansbold.ttf", 32)


def show_score(x, y):
	counting_score = font.render("Score: " + str(score), True, (255,255,0))
	screen.blit(counting_score, (x, y))

def game_over():
	over_text = over_font.render("GAME OVER", True, (255,255,255))
	screen.blit(over_text, (200,200))
	
def player(x,y):
		screen.blit(playerimg, (x, y))


def enemy(x,y,i):
		screen.blit(enemyimg[i], (x, y))

def bullet(x,y):
	global bullet_state
	bullet_state = "Fire"
	screen.blit(bulletimg, (x,y))

def IsCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
	if distance < 27:
		return True
	else:
		return False

running = True

while running:
	screen.fill((255,255,255))
	screen.blit(background,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# if keystroke is pressed check wheather it is rigt or left
		if event.type == pygame.KEYDOWN: # check if any key is pressed means pressing

				if event.key == pygame.K_LEFT:
					velocity = -2

				if event.key == pygame.K_RIGHT:
					velocity = 2

				if event.key == pygame.K_SPACE:
					if bullet_state is "Ready":
						bullet_Sound = mixer.Sound("laser.mp3")
						bullet_Sound.play()
						bulletX = playerX
						bullet(bulletX, bulletY)

		if event.type == pygame.KEYUP: # check if any key is pressed means pressing
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					velocity = 0

# For The Player checking it should not go out of bounce i.e for Boundaries
	playerX += velocity

	if playerX >=450:
		playerX = 450

	elif playerX <= 0:
		playerX = 0

# For The Enemy Movement
	
	for i in range(no_of_enemies):

		# Game Over Logic
		if enemyY[i] > 200:
			for j in range(no_of_enemies):
				enemyY[j] = 2000
			game_over()
			break

		enemyX[i] += enemy_velocity_X[i]
		if enemyX[i] >=460:
			enemy_velocity_X [i]= -0.5
			if enemyY[i] <= 280:
				enemyY[i] += enemy_velocity_Y[i]

		elif enemyX[i] <= 0:
			enemy_velocity_X[i] = 0.5  
			if enemyY[i] <= 280:
				enemyY[i]+= enemy_velocity_Y[i]

		# Code for Bullet Collision
	
		collision = IsCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			Collision_Sound = mixer.Sound("explosion.mp3")
			Collision_Sound.play()
			bulletY = 350
			bullet_state = "Ready"
			score += 1
			enemyX[i] = random.randint(0,480)
			enemyY[i] = random.randint(50,100)

		enemy(enemyX[i], enemyY[i], i)

# To create Another Bullet
	if bulletY <= 0:
		bulletY = 350
		bullet_state = "Ready"


# For the Bullet Movement
	if bullet_state == "Fire":
		bullet(bulletX, bulletY)
		bulletY -= bullet_velocity_Y

	player(playerX, playerY)
	show_score(textX, textY)
	pygame.display.update() # its getting update every loop