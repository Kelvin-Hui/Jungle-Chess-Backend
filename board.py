# Importing Library
import numpy as np
import copy
from pprint import pprint
from animal import *
from dentrapriver import *


def notation_index(notation):
    notation = notation.strip()
    
    if (not notation[0].islower()):
        return(ord(notation[0])-65 , int(notation[1]) -1)


class Board():
    def __init__(self):
        self.height = 9
        self.width = 7
        self.board = self.setup()
        self.isEnd = False
    
    def setBoard(self,x,y,value):
        self.board[x][y] = value


    def setIsEnd(self):
        self.isEnd = True

    def to2Darray(self):
        temp = copy.deepcopy(self.board)
        
        for i in temp:
            for j in i:
                if type(j) not in [int,Den,Trap,River]:
                    if j.team == 0 and j.rank > 0:
                        j.rank *= -1

        return [[j if type(j)== int else j.rank for j in i] for i in temp]


    def setup(self) -> list:
        board = np.array([[0]*self.width for _ in range(self.height//2)] , dtype = object)
        setuplist = {(0,0) : 7 , (0,-1) : 6 ,                                #Animals
                     (1,1) : 4 , (1,-2) : 2, 
                     (2,0) : 1 , (2,2) : 5,
                     (2,4) : 3 , (2,-1) : 8,

                     (0,3) : -10 ,  #CHANGEDEN                                          #Den

                     (0,2) : -9 , (0,4) : -9 , (1,3) : -9,                      #Trap

                     (-1,1) : 15 , (-1,2) : 15 , (-1,4) : 15 ,(-1,5) : 15 ,  #River
                    }
        for i in setuplist:
            board[i[0]][i[1]] = setuplist[i]

        middle = [0,15,15,0,15,15,0]

        board = np.vstack([board,middle,np.flipud(np.fliplr(board))])

        return self.addanimals(board)

    def addanimals(self,board) :
        numtopiece = {
                        15 : "River",
                        -9 : "Trap",
                        8 : "Elephant",
                        7 : "Lion",
                        6 : "Tiger",
                        5 : "Leopard",
                        4 : "Dog",
                        3 : "Wolf",
                        2 : "Cat",
                        1 : "Rat",
                        -10 : "Den"  #CHANGEDEN
                    }
        team = 0
        for i in range(len(board)):
            if i > 4:
                team = 1
            for j in range(len(board[i])):
                if board[i][j] != 0:
                    temp = numtopiece[board[i][j]]
                    board[i][j] = eval(temp)(i,j,team)
                    
        return board
    

    def move(self , x , y , target_x , target_y) -> None:
        if self.board[x][y].validate_move(self.board,target_x,target_y):
            self.setBoard(target_x,target_y, self.board[x][y])
            self.setBoard(x,y,0)
            self.restoreRiver()
            self.restoreTrap()
            return True
        else:
            print("Invalid!")
            return False

    def checkGameover(self):
        if self.board[0][3].rank != -10:  #CHANGEDEN
            #print ("GameOver! Team {} won!".format(self.board[0][3].team))
            return (True,1)
        elif self.board[8][3].rank != -10: #CHANGEDEN
            #print ("GameOver! Team {} won!".format(self.board[8][3].team))
            return (True,0)
        else:
            return (False,3)
    
    def checkTeam(self,x,y,team):
        if self.board[x][y].team != team:
            return False
        return True

    def getName(self,x,y):
        return self.board[x][y].name

    def restoreTrap(self):
        checklist0 = [(0,2),(0,4),(1,3)]
        checklist1 = [(8,2),(8,4),(7,3)]
        for i in checklist0:
            if self.board[i[0]][i[1]]==0:
                self.setBoard(i[0],i[1],Trap(i[0],i[1],0)) 
                break
        for i in checklist1:
            if self.board[i[0]][i[1]]==0:
                self.setBoard(i[0],i[1],Trap(i[0],i[1],1)) 
                break

    def restoreRiver(self):
        checklist = [(3,1),(3,2),(3,4),(3,5),(4,1),(4,2),(4,4),(4,5),(5,1),(5,2),(5,4),(5,5)]
        for i in checklist:
            if self.board[i[0]][i[1]]==0:
                self.setBoard(i[0],i[1],River(i[0],i[1],100))
                break 

    def display(self) -> None:
        pprint(self.board)

    def reset(self):
        self.board = self.setup()
        
