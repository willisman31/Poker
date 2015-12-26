from constants import *

class Player():
    def __init__(self,id,name="John"):
        self.id = id
        self.name = name
        self.reset()

    def reset(self):
        self.fold = False
        #self.turn = -1
        self.money = INITMONEY
        self.pot = 0

    def bet(self,amount):
        self.money -= amount
        self.pot += amount

    def fold(self):
        self.fold = True

if __name__ == '__main__':
    obj = Player(0)
