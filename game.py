#!/usr/bin/env python

# Created by Razorbreak
import pygame
import aiplayer
import random

class Game:
	"""This class creates a new match and set rules of the game"""
	def __init__(self,mode,graphics,screen):
		self.players=[0,0] # [0].player1, [1].player2... 0=human, 1=computer
		self.cpuDifficulty = [0,0] # 0=easy, 1=medium, 2=hard
		self.playerNames=[["Human1","Human2"],["D.Blue","Bender","   EDI"]]
		if(mode>=1):
			self.players[1]=1
		if(mode>=2):
			self.players[0]=1
		self.posXYgrid = (142,64)
		self.gridCellSize = 72
		self.posXYcounter = (230,-5)
		self.graphics = graphics
		self.screen = screen
		self.gameTable = [[0 for i in range(3)] for j in range(3)] # Possible content: 0=free, 1=X, 2=O
		self.selectedGameMode = mode
		self.gameModes = ["PvP","PvC","CvC"] # 0=Player.vs.Player, 1=Player.vs.Comp., 2=Comp.vs.Comp
		self.symbols = [" ","X","O"]
		self.turn = 0 # 0=Player1/CPU1, 1=Player2/CPU2
		self.turnCounter = 0
		self.winner = 0 # 0=draw, 1=p1, 2=p2
	
	def setCPU1Difficulty(self,value):
		self.cpuDifficulty[0] = value
	
	def setCPU2Difficulty(self,value):
		self.cpuDifficulty[1] = value
	
	def check(self):
		# Checks if some row,column or diagonal has equal symbols
		check = (self.checkRows() or self.checkColumns() or self.checkDiagonal())
		if check: 
			self.winner = self.turn+1
			print "\n**********\nPlayer"+str(self.winner)," wins!\n**********\n"
		if (not check) and self.turnCounter==9: print "\n**********\nDraw!\n**********\n"
		return check or self.turnCounter==9
	
	def checkRows(self):
		complete = False
		for i in range(len(self.gameTable)):
			a = self.gameTable[i][0]
			b = self.gameTable[i][1]
			c = self.gameTable[i][2]
			if not complete: complete = (a==b==c and (not a==0))
		return complete
			
	def checkColumns(self):
		complete = False
		for i in range(len(self.gameTable[0])):
			a = self.gameTable[0][i]
			b = self.gameTable[1][i]
			c = self.gameTable[2][i]
			if not complete: complete = (a==b==c and (not a==0))
		return complete
		
	def checkDiagonal(self):
		complete = False
		a = self.gameTable[0][0]
		b = self.gameTable[1][1]
		c = self.gameTable[2][2]
		d = self.gameTable[0][2]
		e = self.gameTable[2][0]
		complete = ((a==b==c or d==b==e) and (not b==0))
		return complete		
		
	def move(self,X,Y,symbol):
		# This method put a symbol (1=X, 2=O) in the XY position of the board
		if(self.gameTable[X][Y]==0):
			self.gameTable[X][Y] = symbol
			print "Put "+self.symbols[symbol]+" on ("+str(X)+","+str(Y)+")"
			return(0)
		else:
			print "You can't put an "+self.symbols[symbol]+" on ("+str(X)+","+str(Y)+")"
			return(1) #ErrorLevel(1): the move is invalid
	
	def getCurrentStatus(self):
		return self.gameTable
	
	def setFirstTurn(self):
		value = random.randrange(0,10)
		self.turn = (value>=5)
		print "\nPlayer"+str(self.turn+1)+" turn"
		
	def changeTurn(self):
		if(self.turn==0):
			self.turn=1
		else:
			self.turn=0
		print "\nPlayer"+str(self.turn+1)+" turn"
		
	def start(self):
		self.setFirstTurn()
		colors = [(255,0,0),(0,0,255)] # Defines the colour of the pieces: colors[0]=X, colors[1]=O
		aiPlayers = [aiplayer.AIPlayer(self.cpuDifficulty[0],self.getCurrentStatus(),1),aiplayer.AIPlayer(self.cpuDifficulty[1],self.getCurrentStatus(),2)]
		clock = pygame.time.Clock()
		FPS = 20 # frames por segundo (juego)
		font = pygame.font.Font("Fonts/concv2.ttf", 50)
		font2 = pygame.font.Font("Fonts/concv2.ttf", 25)
		font3 = pygame.font.Font("Fonts/concv2.ttf", 15)
		makeMove = False # Variable that allow to change turn
		exit = False # Exit the loop and return to main menu
		finish = False # Finish the game
		while not exit:
			#Human moves
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit = True #Finish game
				if event.type == pygame.KEYDOWN and finish:
					#print "Keyboard:",event.key #Debug - Keyboard codes
					if event.key == pygame.K_r: #Press R to restart board
						finish = False
						makeMove = False
						self.gameTable = [[0 for i in range(3)] for j in range(3)]
						aiPlayers = [aiplayer.AIPlayer(self.cpuDifficulty[0],self.getCurrentStatus(),1),aiplayer.AIPlayer(self.cpuDifficulty[1],self.getCurrentStatus(),2)]
						self.setFirstTurn()
						self.turnCounter = 0
						self.winner = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					if(self.players[self.turn]==0 and (not finish)): # If is turn of the human player
						pos = pygame.mouse.get_pos()
						if 142<=pos[0]<=358 and 64<=pos[1]<=280:
							row = (pos[1]-64) // self.gridCellSize
							col = (pos[0]-142) // self.gridCellSize
							print "Click detected at: ",pos," --> Grid: ",(row,col)
							if self.move(row,col,self.turn+1)==0:
								self.turnCounter += 1
								finish = self.check()
								if not finish: makeMove = not makeMove #self.changeTurn()
			
			#Computer moves
			if(self.players[self.turn]==1 and (not finish)): # If is turn of the computer player
				aiMove = aiPlayers[self.turn].makeMove(self.gameTable)
				if self.move(aiMove[0],aiMove[1],self.turn+1)==0:
					self.turnCounter += 1
					finish = self.check()
					if not finish: makeMove = not makeMove #self.changeTurn()				
			if makeMove:
				makeMove = not makeMove
				self.changeTurn()
			# RENDER GAME BOARD
			self.screen.fill((255,255,255))
			if not finish: #Turn selector
				if self.turn==0: self.screen.blit(self.graphics[6],(0,0))
				else: self.screen.blit(self.graphics[6],(250,0))
			self.screen.blit(self.graphics[5],(0,0)) #Game Board
			for i in range(len(self.gameTable)): #Game Table
				for j in range(len(self.gameTable[0])):
					self.screen.blit(self.graphics[4][self.gameTable[i][j]],(self.posXYgrid[0]+j*self.gridCellSize,self.posXYgrid[1]+i*self.gridCellSize))
			text_counter = font.render(str(self.turnCounter),True,(255,168,0)) 
			self.screen.blit(text_counter,self.posXYcounter) #Turn counter
			for i in range(len(self.players)):
				if self.players[i]==0:
					text_Player = font2.render(self.playerNames[0][i],True,colors[i])
					self.screen.blit(text_Player,(4+360*i,33)) #Name Pi
					self.screen.blit(self.graphics[7][0][i],(8+365*i,76)) #Avatar Pi
				if self.players[i]==1:
					text_Player = font2.render(self.playerNames[1][self.cpuDifficulty[i]],True,colors[i])
					self.screen.blit(text_Player,(4+360*i,33)) #Name Pi
					self.screen.blit(self.graphics[7][1][self.cpuDifficulty[i]],(8+365*i,76)) #Avatar Pi
			if finish:
				if self.winner>0:
					msg = "Player"+str(self.winner)+" wins! Press R to restart..."
				else:
					msg = "Draw! Press R to restart..."
				text_end = font3.render(msg,True,(0,0,0))
				self.screen.blit(text_end,(100,290))
			#self.screen.blit(,(0,0)) #Name P2
			#self.screen.blit(self.graphics[5],(0,0)) #Avatar P2
			clock.tick(FPS)
			pygame.display.flip()
	
	def __str__(self):
		# Use "print <Game object>" to show the entire game board
		s = "\n ----"
		s += str(self.gameModes[self.selectedGameMode])
		s += "----\n"
		s += "|===========|\n"
		for i in range(len(self.gameTable)):
			s += "|"
			for j in range(len(self.gameTable[i])):
				s += " "
				aux = self.gameTable[i][j]
				if(aux==0):
					s += " "
				else:
					if(aux==1): 
						s += "X"
					else:
						if(aux==2): s+= "O"
				s += " |"
			s += "\n|===========|\n"
		return s
		
		
		
#print "Pruebas de funcionamiento:"
#match = Game(0)
#print "\n...Turns..."
#match.move(0,0,1)
#match.move(0,1,1)
#match.move(0,2,2)
#match.move(1,1,1)
#match.move(2,2,2)
#match.move(2,1,1)
#print "\n...Checks..."
#print match.check()
#print "\n...Results..."
#print match
#print "Fin de pruebas"
