class LevelGen:
    def __init__(self,world,gamedata):
        self.world = world
        self.gamedata = gamedata
    

    def gen(self):
        for y in range(self.gamedata.worldbreadth//3, self.gamedata.worldbreadth):
            for x in range(self.gamedata.worldlength):
                self.world[y][x] = "stone"
        
        return self.world