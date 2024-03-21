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
        self.WL = self.gamedata.worldlength
        self.WB = self.gamedata.worldbreadth


        self.landy = int(self.WB * (1 - 2.4/3))
        self.fbm = noise.fbm
     
        
    

    def gen(self):
        off = 0.01
        for y in range(self.landy + 1):
            for x in range(self.WL):
                # Calculate fbm noise value
                hmm = (self.fbm(x * off,0, 0, 2, 1, 2) + 1) 

                # Adjust threshold based on y position
                threshold = 0.3 + (y / self.landy) * 0.2 # Increase threshold towards the bottom
                # print(threshold)

                # Set terrain type
                if hmm > threshold:
                    self.world[y][x] = "dirt_grass"  # Top layer
                else:
                    self.world[y][x] = "stone"  # Stone underneath       
            
        return self.world
    
    def set_seed(self,seed = 0):
        random.seed(seed)
    
    def getrandom(self,a = 0,b = 1):
        return random.randint(a,b)


# a = LevelGen()
# a.set_seed()
# print(a.getrandom(1,100))

