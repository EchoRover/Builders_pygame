import random

# if __name__ == "__main__":
#     import noise
# else:
#     from . import noise
# import noise

from . import noise
class LevelGen:
    def __init__(self,world = None,gamedata = None):
        self.world = world
        self.gamedata = gamedata
    

    def gen(self):
        for y in range(self.gamedata.worldbreadth//3, self.gamedata.worldbreadth):
            for x in range(self.gamedata.worldlength):
                self.world[y][x] = "stone"
        
        return self.world
    
    def set_seed(self,seed = 0):
        random.seed(seed)
    
    def getrandom(self,a = 0,b = 1):
        return random.randint(a,b)


a = LevelGen()
a.set_seed()
print(a.getrandom(1,100))

