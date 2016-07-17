#!/usr/bin/env python
# Created by Razorbreak
import random

class AIPlayer:
	"""This class defines the computer players and its inteligence"""
	def __init__(self,difficulty,currentStatus,symbol):
		self.cpuLevel = difficulty # Values: 0,1,2
		self.currentGameStatus = currentStatus
		#self.currentGameStatus = self.__copyListOfLists(currentStatus)
		#self.possibleMoves = []
		self.nextMove = []
		self.mySymbol = symbol # 1=X, 2=O
		self.opositeSymbol = 1
		if self.mySymbol==1: self.opositeSymbol = 2
		
	def __getPossibleMoves(self,state):
		possibleMoves = []
		for i in range(len(state)):
			for j in range(len(state[0])):
				if state[i][j]==0:
					possibleMoves.append([i,j])
		#print "Moves:",self.__printState(state)
		print "Possible moves:\n",possibleMoves
		return possibleMoves
	
	def __copyListOfLists(self,origin):
		destination = []
		for i in range(len(origin)):
			destination.append(origin[i][:])
		return destination
			
	
	def __printState(self,state):
		s = "\n\n"
		s += "|===========|\n"
		for i in range(len(state)):
			s += "|"
			for j in range(len(state[i])):
				s += " "
				aux = state[i][j]
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
	
	####################################################
	#### AI FUNCTIONS
	
	##########################
	# CPU RANDOM
	##########################
	def __cpuEasy(self): # Random move
		possibleMoves = self.__getPossibleMoves(self.currentGameStatus)
		self.nextMove = possibleMoves[random.randrange(0,len(possibleMoves))]
	
	##########################
	# CPU HEURISTIC
	##########################
	def __cpuMedium(self):
		possibleMoves = self.__getPossibleMoves(self.currentGameStatus)
		if([1,1] in possibleMoves): #First best move is center
			self.nextMove = [1,1]
		else:
			self.__checkNextPossiblePuts(possibleMoves)
	
	def __checkNextPossiblePuts(self,possibleMoves):
		defensiveMoves = []
		ofensiveMoves = []
		for i in range(3): #Test every row and column
			# Row i
			r = []
			r.append(self.currentGameStatus[i][0])
			r.append(self.currentGameStatus[i][1])
			r.append(self.currentGameStatus[i][2])
			# Check row
			if sum(r)==2 and (not 2 in r): # X|_|X or other combination
				move = [i,r.index(0)]
				if(self.mySymbol==1): ofensiveMoves.append(move)
				else: defensiveMoves.append(move)
			if sum(r)==4 and (not 1 in r): # O|_|O or other combination
				move = [i,r.index(0)]
				if(self.mySymbol==2): ofensiveMoves.append(move)
				else: defensiveMoves.append(move)
			# Column i
			c = []
			c.append(self.currentGameStatus[0][i])
			c.append(self.currentGameStatus[1][i])
			c.append(self.currentGameStatus[2][i])
			# Check column
			if sum(c)==2 and (not 2 in c): # X|_|X or other combination
				move = [c.index(0),i]
				if(self.mySymbol==1): ofensiveMoves.append(move)
				else: defensiveMoves.append(move)
			if sum(c)==4 and (not 1 in c): # O|_|O or other combination
				move = [c.index(0),i]
				if(self.mySymbol==2): ofensiveMoves.append(move)
				else: defensiveMoves.append(move)				
		
		# Diagonal i
		di = []
		di.append(self.currentGameStatus[0][0])
		di.append(self.currentGameStatus[1][1])
		di.append(self.currentGameStatus[2][2])
		if sum(di)==2 and (not 2 in di): # X|_|X or other combination
			move = [di.index(0),di.index(0)]
			if(self.mySymbol==1): ofensiveMoves.append(move)
			else: defensiveMoves.append(move)
		if sum(di)==4 and (not 1 in di): # O|_|O or other combination
			move = [di.index(0),di.index(0)]
			if(self.mySymbol==2): ofensiveMoves.append(move)
			else: defensiveMoves.append(move)
		# Diagonal r
		dr = []
		dr.append(self.currentGameStatus[0][2])
		dr.append(self.currentGameStatus[1][1])
		dr.append(self.currentGameStatus[2][0])
		if sum(dr)==2 and (not 2 in dr): # X|_|X or other combination
			move = [dr.index(0),2-dr.index(0)]
			if(self.mySymbol==1): ofensiveMoves.append(move)
			else: defensiveMoves.append(move)
		if sum(dr)==4 and (not 1 in dr): # O|_|O or other combination
			move = [dr.index(0),2-dr.index(0)]
			if(self.mySymbol==2): ofensiveMoves.append(move)
			else: defensiveMoves.append(move)
		
		# Random movement if there isn't a defensive/ofensive move
		self.nextMove = possibleMoves[random.randrange(0,len(possibleMoves))]
		if len(defensiveMoves)>0: self.nextMove = defensiveMoves[0]
		if len(ofensiveMoves)>0: self.nextMove = ofensiveMoves[0]
		print "Defensive Moves:\n",defensiveMoves
		print "Ofensive Moves:\n",ofensiveMoves
		
	##########################
	# CPU with COMPLEX HEURISTIC
	##########################
	def __cpuHard(self):
		possibleMoves = self.__getPossibleMoves(self.currentGameStatus)
		if([1,1] in possibleMoves): #First best move is center
			self.nextMove = [1,1]
		else:
			self.nextMove = self.__checkNextPossiblePutsV2(self.currentGameStatus,possibleMoves)
			
	def __checkNextPossiblePutsV2(self,state,possibleMoves):
		defensiveMoves = []
		ofensiveMoves = []
		for i in range(3): #Test every row and column
			# Row i
			r = []
			r.append(state[i][0])
			r.append(state[i][1])
			r.append(state[i][2])
			# Check row
			if sum(r)==2 and (not 2 in r): # X|_|X or other combination
				move = [i,r.index(0)]
				if(self.mySymbol==1): ofensiveMoves.append(move)
				else: defensiveMoves.append(move)
			if sum(r)==4 and (not 1 in r): # O|_|O or other combination
				move = [i,r.index(0)]
				if(self.mySymbol==2): ofensiveMoves.append(move)
				else: defensiveMoves.append(move)
			# Column i
			c = []
			c.append(state[0][i])
			c.append(state[1][i])
			c.append(state[2][i])
			# Check column
			if sum(c)==2 and (not 2 in c): # X|_|X or other combination
				move = [c.index(0),i]
				if(self.mySymbol==1): ofensiveMoves.append(move)
				else: defensiveMoves.append(move)
			if sum(c)==4 and (not 1 in c): # O|_|O or other combination
				move = [c.index(0),i]
				if(self.mySymbol==2): ofensiveMoves.append(move)
				else: defensiveMoves.append(move)				
		
		# Diagonal i
		di = []
		di.append(state[0][0])
		di.append(state[1][1])
		di.append(state[2][2])
		if sum(di)==2 and (not 2 in di): # X|_|X or other combination
			move = [di.index(0),di.index(0)]
			if(self.mySymbol==1): ofensiveMoves.append(move)
			else: defensiveMoves.append(move)
		if sum(di)==4 and (not 1 in di): # O|_|O or other combination
			move = [di.index(0),di.index(0)]
			if(self.mySymbol==2): ofensiveMoves.append(move)
			else: defensiveMoves.append(move)
		# Diagonal r
		dr = []
		dr.append(state[0][2])
		dr.append(state[1][1])
		dr.append(state[2][0])
		if sum(dr)==2 and (not 2 in dr): # X|_|X or other combination
			move = [dr.index(0),2-dr.index(0)]
			if(self.mySymbol==1): ofensiveMoves.append(move)
			else: defensiveMoves.append(move)
		if sum(dr)==4 and (not 1 in dr): # O|_|O or other combination
			move = [dr.index(0),2-dr.index(0)]
			if(self.mySymbol==2): ofensiveMoves.append(move)
			else: defensiveMoves.append(move)
		
		# Improved movement if there isn't a defensive/ofensive move
		corners = [[0,0],[0,2],[2,0],[2,2]]
		possibleCorners = []
		for i in range(len(corners)):
				if self.__isValidMove(state,corners[i]): possibleCorners.append(corners[i])
		
		if len(possibleCorners)>0: nextMove = possibleCorners[random.randrange(0,len(possibleCorners))]
		else: nextMove = possibleMoves[random.randrange(0,len(possibleMoves))]
		
		if self.mySymbol==state[1][1]:
			if state[0][1]==self.opositeSymbol: 
				if [2,0] in possibleCorners: nextMove = [2,0]
				elif [2,2] in possibleCorners: nextMove = [2,2]
			if state[2][1]==self.opositeSymbol:
				if [0,0] in possibleCorners: nextMove = [0,0]
				elif [0,2] in possibleCorners: nextMove = [0,2]
			if state[1][0]==self.opositeSymbol:
				if [0,2] in possibleCorners: nextMove = [0,2]
				elif [2,2] in possibleCorners: nextMove = [2,2]
			if state[1][2]==self.opositeSymbol:
				if [0,0] in possibleCorners: nextMove = [0,0]
				elif [2,0] in possibleCorners: nextMove = [2,0]
		
		if len(defensiveMoves)>0: nextMove = defensiveMoves[0]
		if len(ofensiveMoves)>0: nextMove = ofensiveMoves[0]
		print "Defensive Moves:\n",defensiveMoves
		print "Ofensive Moves:\n",ofensiveMoves
		return nextMove
	
	def __isValidMove(self,state,move):
		return (state[move[0]][move[1]]==0)
	
		
	#### END AI FUNCTIONS
	######################################################
	
	# Function called from Game class to put a piece on the game board
	def makeMove(self,gameTable):
		self.gameCurrentStatus = gameTable
		#self.gameCurrentStatus = self.__copyListOfLists(gameTable)
		print "\n\nCurrent Status:",self.__printState(self.gameCurrentStatus)
		if self.cpuLevel==0:
			self.__cpuEasy()
			return self.nextMove
		elif self.cpuLevel==1:
			self.__cpuMedium()
			return self.nextMove
		elif self.cpuLevel==2:
			self.__cpuHard()
			return self.nextMove
	
