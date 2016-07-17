#!/usr/bin/env python

# Created by Razorbreak

# INCLUDES
import pygame
import game

pygame.init() # Starts game engine

# GLOBAL VARS
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# GRAPHIC RESOURCES
graphics = []
graphics.append([pygame.image.load("Graphics/menu_logo.png"),pygame.image.load("Graphics/menu_logo2.png"),pygame.image.load("Graphics/menu_logo3.png")]) #00 01 02
im_pvp = []
im_pvp.append(pygame.image.load("Graphics/pvp_off.png")) #10
im_pvp.append(pygame.image.load("Graphics/pvp_on.png")) #11
graphics.append(im_pvp)
im_pvc = []
im_pvc.append(pygame.image.load("Graphics/pvc_off.png")) #20
im_pvc.append(pygame.image.load("Graphics/pvc_on.png")) #21
graphics.append(im_pvc)
im_cvc = []
im_cvc.append(pygame.image.load("Graphics/cvc_off.png")) #30
im_cvc.append(pygame.image.load("Graphics/cvc_on.png")) #31
graphics.append(im_cvc)
im_pieces = []
im_pieces.append(pygame.image.load("Graphics/nothing.png")) #40
im_pieces.append(pygame.image.load("Graphics/cross.png")) #41
im_pieces.append(pygame.image.load("Graphics/circle.png")) #42
graphics.append(im_pieces)
graphics.append(pygame.image.load("Graphics/gameBoard.png")) #5
graphics.append(pygame.image.load("Graphics/turnSelector.png")) #6
im_players = []
im_players.append(pygame.image.load("Graphics/human1.png")) #700
im_players.append(pygame.image.load("Graphics/human2.png")) #701
im_cpuplayers = []
im_cpuplayers.append(pygame.image.load("Graphics/cpu1.png")) #710
im_cpuplayers.append(pygame.image.load("Graphics/cpu2.png")) #711
im_cpuplayers.append(pygame.image.load("Graphics/cpu3.png")) #712
graphics.append([im_players,im_cpuplayers])
im_difficulty = []
im_difficulty.append([pygame.image.load("Graphics/easy_on.png"),pygame.image.load("Graphics/easy_off.png")]) #800 801
im_difficulty.append([pygame.image.load("Graphics/medium_on.png"),pygame.image.load("Graphics/medium_off.png")]) #810 811
im_difficulty.append([pygame.image.load("Graphics/hard_on.png"),pygame.image.load("Graphics/hard_off.png")]) #820 821
graphics.append(im_difficulty)

resolution = (256,448)
screen = pygame.display.set_mode(resolution)
caption = "TIC-TAC-TOE by Razorbreak"
pygame.display.set_caption(caption)
clock = pygame.time.Clock()
FPS = 20 # FPS
exit = False
gameModes = ["PvP","PvC","CvC"]
mode = -1 # PvP=0, PvC=1, CvC=2
cpu1Difficulty = 0 # CPU1 Difficulty: 0=easy, 1=medium, 2=hard
cpu2Difficulty = 0 # CPU2 Difficulty: 0=easy, 1=medium, 2=hard
submenu = 0
startGame = False

# WINDOW CONFIGURATIONS
def loadMenuWindow():
	resolution = (256,448)
	screen = pygame.display.set_mode(resolution)
	caption = "TIC-TAC-TOE by Razorbreak"
	pygame.display.set_caption(caption)
	clock = pygame.time.Clock()
	FPS = 20 # FPS

def loadGameWindow(mode):
	resolution = (500,320)
	screen = pygame.display.set_mode(resolution)
	caption = "TIC-TAC-TOE - "+gameModes[mode]+" - by Razorbreak"
	pygame.display.set_caption(caption)
	clock = pygame.time.Clock()
	FPS = 20 # FPS


# MAIN LOOP
while not exit:
	# FETCH EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True #Finish game
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			button = pygame.mouse.get_pressed()
			if button == (True,False,False):
				if (256<=pos[1]<320):
					if mode<0:
						mode = 0
						startGame = True
					elif (mode==1 and submenu==1):
						cpu2Difficulty=0
						startGame = True
					elif (mode==2 and submenu==1):
						cpu1Difficulty=0
						submenu=2
					elif (mode==2 and submenu==2):
						cpu2Difficulty=0
						startGame = True
				elif (320<=pos[1]<384):
					if mode<0:
						mode = 1
						submenu = 1
					elif (mode==1 and submenu==1):
						cpu2Difficulty=1
						startGame = True
					elif (mode==2 and submenu==1):
						cpu1Difficulty=1
						submenu=2
					elif (mode==2 and submenu==2):
						cpu2Difficulty=1
						startGame = True
				elif (384<=pos[1]):
					if mode<0:
						mode = 2
						submenu = 1
					elif (mode==1 and submenu==1):
						cpu2Difficulty=2
						startGame = True
					elif (mode==2 and submenu==1):
						cpu1Difficulty=2
						submenu=2
					elif (mode==2 and submenu==2):
						cpu2Difficulty=2
						startGame = True
				
				if startGame:
					print "Mode "+gameModes[mode]
					loadGameWindow(mode)
					newgame = game.Game(mode,graphics,screen)
					newgame.setCPU1Difficulty(cpu1Difficulty) #FOR CPU-PLAYER1
					newgame.setCPU2Difficulty(cpu2Difficulty) #FOR CPU-PLAYER2
					newgame.start()
					mode = -1
					submenu = 0
					startGame = False
					loadMenuWindow()
					print "Game Over\n\n*********************************\n*********************************"
	
	# RENDER MAIN MENU
	screen.fill(WHITE)
	if submenu==0:
		screen.blit(graphics[0][0],(0,0))
		screen.blit(graphics[1][0],(0,256))
		screen.blit(graphics[2][0],(0,320))
		screen.blit(graphics[3][0],(0,384))
	else:
		screen.blit(graphics[0][submenu],(0,0))
		screen.blit(graphics[8][0][0],(0,256))
		screen.blit(graphics[8][1][0],(0,320))
		screen.blit(graphics[8][2][0],(0,384))
	# MENU ANIMATIONS
	pos = pygame.mouse.get_pos()
	if(256<=pos[1]<320):
		if submenu==0:
			screen.blit(graphics[1][1],(0,256))
		else:
			screen.blit(graphics[8][0][1],(0,256))
	elif(320<=pos[1]<384):
		if submenu==0:
			screen.blit(graphics[2][1],(0,320))
		else:
			screen.blit(graphics[8][1][1],(0,320))
	elif(384<=pos[1]):
		if submenu==0:
			screen.blit(graphics[3][1],(0,384))
		else:
			screen.blit(graphics[8][2][1],(0,384))
	clock.tick(FPS)
	pygame.display.flip()
pygame.quit()
