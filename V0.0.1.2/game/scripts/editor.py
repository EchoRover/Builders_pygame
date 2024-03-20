import random



    

class Editor:
    def __init__(self, gamedata, tiles,levelgen):

        self.gamedata = gamedata
        self.tiles = tiles
        self.LevelGen = levelgen
        self.createmap()
        self.generate()

    def addhotbar(self, hotbar):
        self.hotbar = hotbar

    def createmap(self, sizex=100, sizey=100):

        self.gameworld = [
            [self.givetile() for _ in range(sizex)] for __ in range(sizey)]
        self.gamedata.setupworld(sizex, sizey)
        self.gamedata.setup_max_borders()

    def givetile(self):
        tile = random.choice(list(self.tiles.tile.keys()))
        return tile

    def copymap(self):
        return [row.copy() for row in self.gameworld]

    def generate(self):
        self.gameworld = self.LevelGen(self.gameworld,self.gamedata).gen()
       

    def get_tile(self, x, y):
        # if self.tile_x >= 0 and self.tile_y >= 0 and self.tile_x < self.gamedata.worldlength and self.tile_y < self.gamedata.worldbreadth:
        mx, my = x, y
        self.tile_x = int((mx + self.gamedata.camx) / self.gamedata.tilesize)
        self.tile_y = int((my + self.gamedata.camy) / self.gamedata.tilesize)
        try:
            self.tile = self.gameworld[self.tile_y][self.tile_x]
        except:
            print(f" tile x and y {self.tile_x,self.tile_y}")
            self.tile = None

    def placeItem(self, mx, my):
        self.get_tile(mx, my)

        self.gameworld[self.tile_y][self.tile_x] = self.hotbar.slots[self.hotbar.selected_tile_index].item

  
    def mousepress(self, x, y):
        self.get_tile(x, y)

        if pygame.key.get_pressed()[pygame.K_e]:
            newtile = None
        else:
            newtile = self.hotbar.selected_tile
        try:

            self.gameworld[self.tile_y][self.tile_x] = newtile
        except:
            print("error")

    def update(self):
        self.get_tile()
        self.handlemouse()
