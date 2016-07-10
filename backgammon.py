#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

# prints the current state of the board
def printBoard():
	print ("╭──────────────────┬──────────────────╮")
	print ("│ 1  2  3  4  5  6 ╎ 7  8  9 10 11 12 │")
	print ("├─⌄──⌄──⌄──⌄──⌄──⌄─┼─⌄──⌄──⌄──⌄──⌄──⌄─┤")
	for row in range (1, max(max(board), min(board) * -1, 7)+1):
		line = "│"
		for col in range(0,12):
			if col == 6:
				line += "╎"
			if abs(board[col]) >= row:
				if board[col] > 0:
					line += " ○ "
				else:
					line += " ● "
			else:
				line += "   "
		line += "│"	
		print line
	print ("├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤")
	for row in range (max(max(board), min(board) * -1, 7),0,-1):
		line = "│"
		for col in range(23,11,-1):
			if col == 17:
				line += "╎"
			if abs(board[col]) >= row:
				if board[col] > 0:
					line += " ○ "
				else:
					line += " ● "
			else:
				line += "   "
		line += "│"	
		print line
	print ("├─⌃──⌃──⌃──⌃──⌃──⌃─┼─⌃──⌃──⌃──⌃──⌃──⌃─┤")
	print ("│24 23 22 21 20 19 ╎18 17 16 15 14 13 │")
	print ("╰──────────────────┴──────────────────╯")

# creates two random values and returns them (4 values if both are equal)
def throwDice():
	rand = []
	rand.append(random.randrange(1,7,1))
	rand.append(random.randrange(1,7,1))
	print ("The dices show " + str(rand[0]) + " and " + str(rand[1]))
	# both values are equal, return 4 times the same
	if rand[0] == rand[1]:
		rand.append(rand[0])
		rand.append(rand[0])
	return rand

# check if game is finished
# returns true if finished, false if not finished
def finished():
	pos = 0
	neg = 0
	for i in range(len(board)):
		if board[i] > 0:
			pos += board[i]
		elif board[i] < 0:
			neg += board[i]
	if pos == 0 or neg == 0:
		return True
	else:
		return False

# check if a player has all checkers in his home-base
# takes (1) a boolean telling if it should check for positive (white) if passed true 
# 		or for negative (black) if passed false
# returns true if the player has all checkers in the home-base, false if not
def isHome(positive):
	# white player
	if positive == True:
		if outpositive > 0:
			return False
		for i in range(0, 18):
			if board[i] > 0:
				return False
		return True
	# black player
	else:
		if outnegative > 0:
			return False
		for i in range(6, 24):
			if board[i] > 0:
				return False
		return True

# checks if a move is valid
# takes (1) a boolean telling if it should check for positive (white) if passed true 
# 		or for negative (black) if passed false
#		(2) a position (1-24) on the board
#		(3) a dice-value (1-6)
# returns true if move is valid, false if not
def validMove(positive, position, dice):
	# check if position is in range
	if position < 1 or position > 24:
		print "g1 ", position
		return False
	# check if dice-value is in range (0 for re-entry allowed)
	if dice < 0 or dice > 6:
		print "g2 ", dice
		return False
	# check if a move on the board is valid
	if isHome(positive) == False:
		if positive == True:
			if position + dice > 24:
				print "nh p ", position + dice
				return False
		else:
			if position - dice < 1:
				print "nh n ", position - dice
				return False
		if positive == True and board[position - 1 + dice] < -1:
			print "nh p negative ", board[position - 1 + dice]
			return False
		elif positive == False and board[position - 1 - dice] > 1:
			print "nh n positive ", board[position - 1 - dice]
			return False
		else:
			print "nh else "
			return True
	# check if a move for removing a checker is valid for a player who has all checkers in the home-base
	else:
		if positive == True and position + dice > 24:
			print "h p ", position + dice
			return True
		elif positive == False and position - dice < 1:
			print "h n ", position - dice
			return True
		else: 
			print "h else "
			return False

# cheks if player is able to move
# takes (1) a boolean telling if it should check for positive (white) if passed true 
# 		or for negative (black) if passed false
#		(2) a list of dice values
# returns true if player can make any move
def moveable(positive, values):
	canmove = False
	# check all dice values
	for i in values:
		# white player
		if positive == True:
			# check if re-enter is possible
			if outpositive > 0:
				if validMove(positive, 1, i - 1) == True:
					canmove = True
					break
			# check if normal move is possible
			else:
				for f in range(len(board)):
					if board[f] > 0:
						if validMove(positive, f + 1, i) == True:
							canmove = True
							break
				if canmove == True:
					break
		# black player
		else:
			# check if re-enter is possible
			if outnegative > 0:
				if validMove(positive, 24, i - 1) == True:
					canmove = True
					break
			# check if normal move is possible
			else:
				for f in range(len(board)):
					if board[f] < 0:
						if validMove(positive, f + 1, i) == True:
							canmove = True
							break
				if canmove == True:
					break
	return canmove

# collects all possible moves
# takes (1) a boolean telling if it should check for positive (white) if passed true 
# 		or for negative (black) if passed false
#		(2) a list of dice values
# returns a list of all possible moves in form (position, dice-value)
def getAllPossibleMoves(positive, values):
	moves = []
	# check all dice values
	for i in values:
		# white player
		if positive == True:
			# re-enter needed
			if outpositive > 0:
				if validMove(positive, 1, i - 1) == True:
					moves.append([1,i - 1])
			# normal moves
			else:
				for f in range(len(board)):
					if board[f] > 0:
						if validMove(positive, f + 1, i) == True:
							moves.append([f + 1,i])
		# black player
		else:
			# re-enter needed
			if outnegative > 0:
				if validMove(positive, 24, i - 1) == True:
					moves.append([24, i - 1])
			# normal moves:
			else:
				for f in range(len(board)):
					if board[f] < 0:
						if validMove(positive, f + 1, i) == True:
							moves.append([f + 1,i])

# evaluates possible moves and returns an ordered descending list of theevaluated moves
# takes (1) a boolean telling if it should check for positive (white) if passed true 
# 		or for negative (black) if passed false
#		(2) a list of possible moves in form (position, dice-value)
# returns a list of evaluated possible moves in form (position, dice-value, value)
def evaluateMoves():
	print ""


##########################################################################

# positive = white (empty circle), home 19-24, player
# negative = black (filled circle), home 1-6
board = [2,0,0,0,0,-5,0,-3,0,0,0,5,-5,0,0,0,3,0,5,0,0,0,0,-2]
outpositive = 0
outnegative = 0
dices = []
printBoard()

while not finished():
	dices = throwDice()
	while outpositive > 0 and dices:
		if moveable(True, dices) == False:
			print ("Moving not possible")
			printBoard()
			break
		print ("You play ○.")
		reenter = input("You need to re-enter " + str(outpositive) + " checkers. Which dice-value do you want to use " + str(dices) + "? ")
		if reenter == "" :
			continue
		if not reenter in dices:
			printBoard()
			print("Please choose a dice-value!")
		else:
			if validMove(True, 1, reenter - 1) == False:
				print ("Invalid move. Please try again.")
				continue

		if board[reenter - 1] == -1:
			outnegative = outnegative + 1
			board[reenter - 1] = 1
		else:
			board[reenter - 1] = board[reenter - 1] + 1
		outpositive = outpositive - 1
		dices.remove(reenter)
		printBoard()
	while dices:
		if outpositive > 0:
			print "not able to re-enter, next player"
			break
		if moveable(True, dices) == False:
			print ("Moving not possible")
			printBoard()
			break
		print ("You play ○.")
		if len(dices) > 1 and dices[0] != dices[1]:
			dice = input("Which dice-value do you want to move " + str(dices) + "? ")
			if dice == "":
				continue
		else:
			dice = dices[0]
		if not dice in dices:
			printBoard()
			print("Please choose a dice-value!")
			continue
		else:
			position = input("Which checker do you want to move " + str(dice) + "? ")
			if position == "":
				continue
			if validMove(True, position, dice) == False:
				print ("Invalid move. Please try again.")
				continue

		board[position - 1] = board[position - 1] - 1
		if position + dice > 24:
			if board[position - 1 + dice] == -1:
				board[position - 1 + dice] = 1
				outnegative = outnegative + 1
			else:
				board[position - 1 + dice] = board[position - 1 + dice] + 1
		dices.remove(dice)
		printBoard()



	dices = throwDice()
	while outnegative > 0 and dices:
		if moveable(False, dices) == False:
			print ("Moving not possible")
			printBoard()
			break
		print ("You play ●.")
		reenter = input("You need to re-enter " + str(outnegative) + " checkers. Which dice-value do you want to use " + str(dices) + "? ")
		if reenter == "":
			continue
		if not reenter in dices:
			printBoard()
			print("Please choose a dice-value!")
		else:
			if validMove(False, 24, reenter - 1) == False:
				print ("Invalid move. Please try again.")
				continue

		if board[23 - reenter + 1] == 1:
			outpositive = outpositive + 1
			board[23 - reenter + 1] = -1
		else:
			board[23 - reenter + 1] = board[23 - reenter + 1] - 1
		outnegative = outnegative - 1
		dices.remove(reenter)
		printBoard()
	while dices:
		if outnegative > 0:
			print "not able to re-enter, next player"
			break
		if moveable(False, dices) == False:
			print ("Moving not possible")
			printBoard()
			break
		print ("You play ●.")
		if len(dices) > 1 and dices[0] != dices[1]:
			dice = input("Which dice-value do you want to move " + str(dices) + "? ")
			if dice == "":
				continue
		else:
			dice = dices[0]
		if not dice in dices:
			printBoard()
			print("Please choose a dice-value!")
			continue
		else:
			position = input("Which checker do you want to move " + str(dice) + "? ")
			if position == "":
				continue
			if validMove(False, position, dice) == False:
				print ("Invalid move. Please try again.")
				continue

		board[position - 1] = board[position - 1] + 1
		if position - dice < 1:
			if board[position - 1 - dice] == 1:
				board[position - 1 - dice] = -1
				outpositive = outpositive + 1
			else:
				board[position - 1 - dice] = board[position - 1 - dice] - 1
		dices.remove(dice)
		printBoard()














