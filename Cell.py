import random
class Cell:
    def __init__(self, location, alive=False):
        self.alive = alive
        self.pressed = False
        self.location = location
        self.ziarno = 0
        self.ziarnotobe = 0
        self.to_be = False
        self.srodex = random.random() - 0.5
        self.srodeky = random.random() - 0.5
        self.energia = 0
        self.energiatobe = 0
