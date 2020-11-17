import numpy as np

class Animal():
    def __init__(self,x,y,rank,team,name):
        self.pos_x = x
        self.pos_y = y
        self.rank = rank
        self.team = team                  #Team to prevent Team kill
        self.name = name

    def __repr__(self):
        return str(self.rank)

    def setRank(self , target):
        self.rank = target

    def setPosition(self, pos):
        self.pos_x = pos[0]
        self.pos_y = pos[1]
 
    def isCaptureable (self , enemy) -> bool:
        if self.rank >= enemy.rank  and self.team != enemy.team:
            return True
        elif (self.team == 0 and self.team != enemy.team):
            if (enemy.pos_x,enemy.pos_y) in [(0,2),(0,4),(1,3)]:
                return True
        elif (self.team == 1 and self.team != enemy.team):
            if (enemy.pos_x,enemy.pos_y) in [(8,2),(8,4),(7,3)]:
                return True
        else:
            if enemy.rank == -9:
                return True
            return False
        
    

    # def validate_move(self , board : np.array , move_x : int ,move_y : int) -> bool:
    #     if (board[move_x][move_y]) == 0:
    #         if move_x in range(self.pos_x -1 , self.pos_x +1+1) and move_y == self.pos_y:
    #             self.setPosition((move_x,move_y))
    #             return True
    #         elif  move_y in range(self.pos_y -1 , self.pos_y +1+1) and move_x == self.pos_x:
    #             self.setPosition((move_x,move_y))
    #             return True
    #     else:
    #         if self.isCaptureable(board[move_x][move_y]):
    #             self.setPosition((move_x,move_y))
    #             return True
    #         else:
    #             return False
    

    def validate_move(self , board : np.array , move_x : int ,move_y : int) -> bool:
        if (move_x in range(self.pos_x -1 , self.pos_x +1+1) and move_y == self.pos_y) or (move_y in range(self.pos_y -1 , self.pos_y +1+1) and move_x == self.pos_x) :
            if (board[move_x][move_y]) == 0:
                    self.setPosition((move_x,move_y))
                    return True
            else:
                if self.isCaptureable(board[move_x][move_y]):
                    self.setPosition((move_x,move_y))
                    return True
                else:
                    return False
        return False

    



class Elephant(Animal):
    def __init__(self,x,y,team):
        super().__init__(x,y,8,team,"Elephant")
    
    def isCaptureable (self , enemy) -> bool:
        if self.rank >= enemy.rank  and self.team != enemy.team:
            if enemy.rank == 1:
                return False
            return True
        elif (self.team == 0 and self.team != enemy.team):
            if (enemy.pos_x,enemy.pos_y) in [(0,2),(0,4),(1,3)]:
                return True
        elif (self.team == 1 and self.team != enemy.team):
            if (enemy.pos_x,enemy.pos_y) in [(8,2),(8,4),(7,3)]:
                return True
        else:
            if enemy.rank == -9:
                return True
            return False


class Lion(Animal):
    def __init__(self,x,y,team):
        super().__init__(x,y,7,team,"Lion")
    
    def acrossRiver(self,board,move_x,move_y):
        if (self.pos_y  and move_y in [1,2,4,5]) and self.pos_y == move_y:
            if abs(self.pos_x - move_x) == 4:
                if (board[3][move_y].rank + board[4][move_y].rank + board[5][move_y].rank == 45):
                    return True
            return False

        else:
            if(self.pos_x and move_x in [3,4,5] and self.pos_x == move_x):
                if (self.pos_y - move_y) == 3:
                    if(board[self.pos_x][self.pos_y-1].rank + board[self.pos_x][self.pos_y-2].rank) == 30:
                        return True
                elif (self.pos_y - move_y) == -3:
                    if(board[self.pos_x][self.pos_y+1].rank + board[self.pos_x][self.pos_y+2].rank) == 30:
                        return True
                elif (self.pos_y - move_y) == 6:
                    if(board[self.pos_x][self.pos_y-1].rank + board[self.pos_x][self.pos_y-2].rank)+(board[self.pos_x][self.pos_y-4].rank + board[self.pos_x][self.pos_y-5].rank) == 60:
                        return True
                elif (self.pos_y - move_y) == -6:
                    if(board[self.pos_x][self.pos_y+1].rank + board[self.pos_x][self.pos_y+2].rank)+(board[self.pos_x][self.pos_y+4].rank + board[self.pos_x][self.pos_y+5].rank) == 60:
                        return True
                                             
            return False

    def validate_move(self , board : np.array , move_x : int ,move_y : int):
        if (board[move_x][move_y]) == 0:
            if self.acrossRiver(board,move_x,move_y):
                self.setPosition((move_x,move_y))
                return True
            elif move_x in range(self.pos_x -1 , self.pos_x +1+1) and move_y == self.pos_y:
                self.setPosition((move_x,move_y))
                return True
            elif  move_y in range(self.pos_y -1 , self.pos_y +1+1) and move_x == self.pos_x:
                self.setPosition((move_x,move_y))
                return True
        else:
            if self.acrossRiver(board,move_x,move_y):
                if self.isCaptureable(board[move_x][move_y]):
                    self.setPosition((move_x,move_y))
                    return True
                else:
                    return False
            else:
                if (move_x in range(self.pos_x -1 , self.pos_x +1+1) and move_y == self.pos_y) or (move_y in range(self.pos_y -1 , self.pos_y +1+1) and move_x == self.pos_x) :
                    if self.isCaptureable(board[move_x][move_y]):
                        self.setPosition((move_x,move_y))
                        return True
                    else:
                        return False
                return False
    

        

class Tiger(Animal):
    def __init__(self,x,y,team):
        super().__init__(x,y,6,team,"Tiger")

    def acrossRiver(self,board,move_x,move_y):
        # if self.pos_x and move_x in [3,4,5]:
        #     if self.pos_y in [0,6] and move_y == 3:
        #         if self.pos_y == 0 and (board[self.pos_x][1].rank+board[self.pos_x][2].rank) == 30:
        #             return True
        #         elif self.pos_y == 6 and (board[self.pos_x][4].rank+board[self.pos_x][5].rank) == 30:
        #             return True
        #         return False
        #     elif self.pos_y == 3 and move_y in [0,6]:
        #         if move_y == 0 and (board[self.pos_x][1].rank+board[self.pos_x][2].rank) == 30:
        #             return True
        #         elif move_y == 6 and (board[self.pos_x][4].rank+board[self.pos_x][5].rank) == 30:
        #             return True
        #         return False
        #     else:
        #         return False
        if(self.pos_x and move_x in [3,4,5] and self.pos_x == move_x):
                if (self.pos_y - move_y) == 3:
                    if(board[self.pos_x][self.pos_y-1].rank + board[self.pos_x][self.pos_y-2].rank) == 30:
                        return True
                elif (self.pos_y - move_y) == -3:
                    if(board[self.pos_x][self.pos_y+1].rank + board[self.pos_x][self.pos_y+2].rank) == 30:
                        return True               
        return False

    def validate_move(self , board : np.array , move_x : int ,move_y : int):
        if (board[move_x][move_y]) == 0:
            if self.acrossRiver(board,move_x,move_y):
                self.setPosition((move_x,move_y))
                return True
            elif move_x in range(self.pos_x -1 , self.pos_x +1+1) and move_y == self.pos_y:
                self.setPosition((move_x,move_y))
                return True
            elif  move_y in range(self.pos_y -1 , self.pos_y +1+1) and move_x == self.pos_x:
                self.setPosition((move_x,move_y))
                return True
        else:
            if self.acrossRiver(board,move_x,move_y):
                if self.isCaptureable(board[move_x][move_y]):
                    self.setPosition((move_x,move_y))
                    return True
                else:
                    return False
            else:
                if (move_x in range(self.pos_x -1 , self.pos_x +1+1) and move_y == self.pos_y) or (move_y in range(self.pos_y -1 , self.pos_y +1+1) and move_x == self.pos_x) :
                    if self.isCaptureable(board[move_x][move_y]):
                        self.setPosition((move_x,move_y))
                        return True
                    else:
                        return False
                return False


class Leopard(Animal):
    def __init__(self,x,y,team):
        super().__init__(x,y,5,team,"Leopard")

class Dog(Animal):
    def __init__(self,x,y,team):
        super().__init__(x,y,4,team,"Dog")

class Wolf(Animal):
    def __init__(self,x,y,team):
        super().__init__(x,y,3,team,"Wolf")

class Cat(Animal):
    def __init__(self,x,y,team):
        super().__init__(x,y,2,team,"Cat")   

class Rat(Animal):
    def __init__(self,x,y,team):
        self.inRiver = False
        super().__init__(x,y,1,team,"Rat")
    
    def isCaptureable(self, enemy):
        if (enemy.rank == 8 or enemy.rank == 15) and (self.team != enemy.team):
            return True
        if self.rank >= enemy.rank  and self.team != enemy.team:
            return True

        elif (self.team == 0 and self.team != enemy.team):
            if (enemy.pos_x,enemy.pos_y) in [(0,2),(0,4),(1,3)]:
                return True
        elif (self.team == 1 and self.team != enemy.team):
            if (enemy.pos_x,enemy.pos_y) in [(8,2),(8,4),(7,3)]:
                return True
        else:
            if enemy.rank == -9:
                return True
            return False
