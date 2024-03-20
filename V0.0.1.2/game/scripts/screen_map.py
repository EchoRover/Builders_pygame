import pygame

class ScreenGrid():
    def __init__(self,gamedata,tiles):
        
        self.gamedata = gamedata
        self.tiles = tiles
    
    def draw(self, surface, world):
        tilex = int(self.gamedata.camx // self.gamedata.tilesize)
        tiley = int(self.gamedata.camy // self.gamedata.tilesize)
        offsetX = -(self.gamedata.camx % self.gamedata.tilesize)
        offsetY = -(self.gamedata.camy % self.gamedata.tilesize)

        for y in range(self.gamedata.screen_tile_breadth):
            for x in range(self.gamedata.screen_tile_length):
                tile = world[tiley + y][tilex + x]
                if tile:
                    surface.blit(self.tiles.tile[tile], (x * self.gamedata.tilesize + offsetX, y * self.gamedata.tilesize + offsetY))
 
class MiniMap:
    def __init__(self, gamedata, tiles):
        self.gamedata = gamedata
        self.tiles = tiles
        self.calculate_offsets()

    def drawmap(self, gameworld, surf):

        for y in range(self.gamedata.worldbreadth):
            for x in range(self.gamedata.worldlength):
                surf.blit(pygame.transform.scale(self.tiles.tile[gameworld[y][x]], (self.tilesize, self.tilesize)), (x * self.tilesize + self.offsetx, y * self.tilesize + self.offsety))
    
    def calculate_offsets(self):

        self.tilesize = min(self.gamedata.canvas_height // self.gamedata.worldbreadth, self.gamedata.canvas_width // self.gamedata.worldlength)
        self.offsetx = (self.gamedata.canvas_width - self.tilesize * self.gamedata.worldlength) / 2
        self.offsety = (self.gamedata.canvas_height - self.tilesize * self.gamedata.worldbreadth) / 2

