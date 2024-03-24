
# if __name__ == "__main__":
#     import noise
# else:
#     from . import noise


from . import noise

class Tiles:
    def __init__(self, t, hotbarsize):
        self.TILESIZE = t
        self.Hotbar_scale = hotbarsize

        self.tile = {"air":pygame.Surface((t,t))}
        self.Htile = dict()
        self.load_tiles()

    def load_tiles(self):
        tiles_folder = __file__[:-len("/scripts/levelgenerate.py")] + "/tiles"
        print(__file__)
        print(tiles_folder)
        for filename in os.listdir(tiles_folder):
            if filename.endswith(".png"):

                image_path = os.path.join(tiles_folder, filename)
                image = pygame.image.load(image_path).convert_alpha()

                scaled_image = pygame.transform.scale(
                    image, (self.TILESIZE, self.TILESIZE))

                self.tile[filename.rstrip('.png')] = scaled_image
                self.Htile[filename.rstrip('.png')] = pygame.transform.scale(
                    image, (self.Hotbar_scale, self.Hotbar_scale))


        

class LevelGen:
    def __init__(self,wl,wb,world = None):
        self.world = world
        self.WL = wl
        self.WB = wb


        self.surfaceH = int(self.WB * (1 - 2.7/3))
        self.waterH = int(self.WB * (1 - 2.72/3))
        self.caveH = int(self.WB * (1 - 2/3))
        self.fbm = noise.fbm
        self.seed = 0
        self.copy_dat = None
        self.helpfuldata = None
        self.readdata()
        

        tiles_to_add = ["dirt_grass","sand","dirt","stone","water","tree","coal","iron","diamond","silver","gold","lava","grass","ruby","grey_stone","gravel","redstone"]
    
    def get_block(self,x,y):
        freq1 = 0.0059
        freq2 = 0.009 
        surfaceY = self.surfaceH + self.get_noise(x,y,self.seed,self.helpfuldata[4])
        tile = "air"
        if y < surfaceY:
            if y > self.waterH:
                tile = "water"
            else:
                tile = "air"
        else:
            cave = self.get_noise(x,y,self.seed,self.helpfuldata[5])
            # if y < self.caveH:
            #     print(cave,end = " ")
            #     cave += (1/y) * 10
            #     print(cave,"\n")

            tile = "stone" if -0.5 < cave < 0.5 else "air"
           
        return tile

    
    def get_noise(self,x,y,z,data):
      
        return self.fbm(x * data[0],y * data[1],int(z * data[2]),int(data[3]),data[4],data[5]) * data[6]
    
    def genworld(self):
        for y in range(self.WB):
            for x in range(self.WL):
                self.world[y][x] = self.get_block(x,y)
        
        return self.world




    
    def set_seed(self,seed = 0):
        random.seed(seed)
        self.seed = seed
    
    def getrandom(self,a = 0,b = 1):
        return random.randint(a,b)
    
    def readdata(self):
        if self.copy_dat:
            copy = self.copy_dat

            coph = self.helpfuldata.copy()
        try:
            with open("game/scripts/noisedata.txt") as f:
                data = f.read()
                if self.copy_dat == data:
                    f.close()
                    return False
                self.copy_dat = data
                data = data.split("\n")
            
                data = [i for i in data if ("#" not in i) and i != ""]
                new = []
                for i in data:
                    for j in i:
                        if j.isdigit():
                            new.append(i)
                            break

                data = new
                


                self.helpfuldata = [list(map(float,i.split(","))) if len(i.split(",")) > 1 else float(i) for i in data ]
        

                #setin stone
                self.surfaceH = int(self.WB * (1 - self.helpfuldata[0]/3))
                self.waterH = int(self.WB * (1 - self.helpfuldata[1]/3))
                self.caveH = int(self.WB * (1 - self.helpfuldata[2]/3))
                self.seed = self.helpfuldata[3]

                return True
        except:
            self.copy_dat = copy
            self.helpfuldata = coph
            self.surfaceH = int(self.WB * (1 - self.helpfuldata[0]/3))
            self.waterH = int(self.WB * (1 - self.helpfuldata[1]/3))
            self.caveH = int(self.WB * (1 - self.helpfuldata[2]/3))
            self.seed = self.helpfuldata[3]
            return False




