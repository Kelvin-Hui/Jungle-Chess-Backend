class River():
    def __init__(self,x,y,team):
        self.pos_x = x
        self.pos_y = y
        self.team = 100
        self.rank = 15
    def __repr__(self):
        return str(self.rank)


class Den():
    def __init__(self,x,y,team):
        self.pos_x = x
        self.pos_y = y
        self.team = team
        self.rank = -10   #CHANGEDEN
    def __repr__(self):
        return str(self.rank)


class Trap():
    def __init__(self,x,y,team):
        self.pos_x = x
        self.pos_y = y
        self.team = team
        self.rank = -9
    def __repr__(self):
        return str(self.rank)