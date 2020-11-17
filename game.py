import numpy as np
import random
from board import *
from pprint import pprint

testing =  [["{}{}".format(chr(65+i),j+1)  for j in range(7)] for i in range(9)]

def notation_index(notation):
    notation = notation.strip()
    
    if (not notation[0].islower()):
        return(ord(notation[0])-65 , int(notation[1]) -1)

def askInput():
    eval("Game.display()")
    player1_move = notation_index(str(input("Enter the notation of the pieces that you want to move (eg: A1): ")))
    player1_target = notation_index(str(input("Enter the notation of the location that you want your peices to move (eg: A1): ")))
    return player1_move,player1_target

def checkLegit(board,move,target,team):
    if not(move[0] in range(9) and target[0] in range(9)):
        print("\n\n Inputs out of bounds! Please Re-Enter your choice! \n\n")
        return False
    if not(move[1] in range(7) and target[1] in range(7)):
        print("\n\n Inputs out of bounds! Please Re-Enter your choice! \n\n")
        return False
    if board[move[0]][move[1]].team != team:
        print("\n\n You dont have access to this piece! Please Re-enter your choice! \n\n")
        return False
    return True


print("Game Starts!")
Game = Board()
print("We will use random number generator to decide team 0 or 1 go first \n")
print("0 indicate the top of the board!")
print("1 indicate the bottom of the board! \n")
rand = random.randint(0,1)
print("{} will go first \n\n".format(rand))

player1_move , player1_target = askInput()

while not checkLegit(Game.board,player1_move,player1_target,rand):
    player1_move , player1_target = askInput()
    
Game.move(player1_move[0],player1_move[1],player1_target[0],player1_target[1])
    
while (not Game.checkGameover()):
    rand = abs(rand-1)
    
    player1_move , player1_target = askInput()

    while not checkLegit(Game.board,player1_move,player1_target,rand):
        player1_move , player1_target = askInput()
        
    Game.move(player1_move[0],player1_move[1],player1_target[0],player1_target[1])    