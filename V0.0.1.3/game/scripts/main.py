import pygame
import random
import sys

if __name__ == '__main__':

    from inventory import Item, HotBar
    from editor import Editor
    from screen_map import ScreenGrid, MiniMap
    from camera import Camera
    from levelgenerate import LevelGen

else:
    
    from .inventory import Item, HotBar
    from .editor import Editor
    from .screen_map import ScreenGrid, MiniMap
    from .camera import Camera
    from .levelgenerate import LevelGen




from math import ceil
import os


class Gamedata:
    def __init__(self):
        pygame.init()
        self.gamestate = None

    def setup_cam(self, camx, camy):
        self.camx = camx
        self.camy = camy

    def setup_main(self, tilesize, ratio):
        self.aspect_ratio = ratio
        self.tilesize = tilesize
        self.screen = None
    
    def setup_hotbar(self,tilesize,spacing,num_tiles):
        self.HotBar_tile_size = tilesize
        self.HotBar_spacing = spacing 
        self.HotBar_num_tiles = num_tiles

    def setup_screen(self, canvas_width, canvas_height):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.target_canvas_height = canvas_height
        self.target_canvas_width = canvas_width


    def update_screensize(self):
        newmainw = self.screen.get_width()
        newmainh = self.screen.get_height()

        new_canvas_width = newmainw
        new_canvas_height = newmainw / self.aspect_ratio

        if new_canvas_height > newmainh:
            new_canvas_height = newmainh
            new_canvas_width = newmainh * self.aspect_ratio

        self.canvas_offsetx = (newmainw - new_canvas_width) / 2
        self.canvas_offsety = (newmainh - new_canvas_height) / 2

        self.canvas_width = new_canvas_width
        self.canvas_height = new_canvas_height

        self.mousemaxW = self.canvas_width + self.canvas_offsetx
        self.mouseminH = self.canvas_height + self.canvas_offsety

        self.mouse_x_multiplier = self.target_canvas_width / self.canvas_width
        self.mouse_y_multiplier = self.target_canvas_height / self.canvas_height

    def setup_screen_tile_lengths(self):
        self.screen_tile_length = ceil(
            self.canvas_width/self.tilesize) + 1
        self.screen_tile_breadth = ceil(
            self.canvas_height/self.tilesize) + 1

    def setupworld(self, worldlength, worldbreadth):
        self.worldlength = worldlength
        self.worldbreadth = worldbreadth

    def setup_max_borders(self):
        self.max_length_border = self.tilesize * \
            (self.worldlength - self.screen_tile_length)
        self.max_breadth_border = self.tilesize * \
            (self.worldbreadth - self.screen_tile_breadth)


class Tiles:
    def __init__(self, t, hotbarsize):
        self.TILESIZE = t
        self.Hotbar_scale = hotbarsize

        self.tile = {"air": pygame.Surface((t,t))}
        self.Htile = dict()
        self.load_tiles()

    def load_tiles(self):
        tiles_folder = __file__[:-len("/scripts/main.py")] + "/tiles"
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


class Game:
    def __init__(self):

        self.gamedata = Gamedata()

        self.gamedata.setup_main(64, 16/9)
        self.gamedata.setup_screen(1280, 720)
        self.gamedata.setup_hotbar(48,5,10)

        self.gamedata.setup_screen_tile_lengths()
        self.clock = pygame.time.Clock()
        self.canvas = pygame.Surface(
            (self.gamedata.canvas_width, self.gamedata.canvas_height))
        self.screen = pygame.display.set_mode(
            (self.gamedata.canvas_width, self.gamedata.canvas_height), pygame.RESIZABLE)
        self.gamedata.screen = self.screen
        self.gamedata.update_screensize()
        self.mouse_state = None
        self.change = True

        self.editor = 1

        if self.editor == 1:
            self.editor = Editor(self.gamedata, Tiles(
                self.gamedata.tilesize, self.gamedata.HotBar_tile_size),LevelGen)
            self.cam = Camera(self.gamedata)
            self.screengrid = ScreenGrid(self.gamedata, self.editor.tiles)
            self.hotbar = HotBar(self.gamedata, self.editor.tiles)
            self.editor.addhotbar(self.hotbar)
            self.minemap = MiniMap(self.gamedata, self.editor.tiles)

    def handlemouse(self):
        x, y = pygame.mouse.get_pos()
        if (self.gamedata.canvas_offsetx <= x <= self.gamedata.mousemaxW and self.gamedata.canvas_offsety <= y <= self.gamedata.mouseminH):
            self.mx = (x - self.gamedata.canvas_offsetx) * \
                self.gamedata.mouse_x_multiplier
            self.my = (y - self.gamedata.canvas_offsety) * \
                self.gamedata.mouse_y_multiplier
        else:
            self.mx = self.my = None

    def runmap(self):
        if self.change:
            self.canvas.fill((225, 255, 255))
            self.screen.fill((0, 0, 0))
            self.minemap.drawmap(self.editor.gameworld, self.canvas)

    def runnormal(self):

        if self.mouse_state == "place" and self.mx:
            self.editor.placeItem(self.mx, self.my)

        self.cam.update()

        self.canvas.fill((255, 255, 255))
        self.screen.fill((0, 0, 0))

        self.screengrid.draw(self.canvas, self.editor.gameworld)
        self.hotbar.draw(self.canvas, self.mx, self.my)

    def run_editor(self):

        while True:

            self.handlemouse()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.WINDOWRESIZED:

                    self.gamedata.update_screensize()
                    self.change = True

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mx:

                    if self.hotbar.touchingmouse(self.mx, self.my):
                        self.hotbar.moveItem(self.mx, self.my)
                        self.mouse_state = None
                    else:
                        self.mouse_state = "place"

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouse_state = None
                    if self.mx:
                        if self.hotbar.touchingmouse(self.mx, self.my):
                            self.hotbar.placeItem(self.mx, self.my)
                        else:
                            self.hotbar.handle_not_touching()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        if self.gamedata.gamestate == None:
                            self.gamedata.gamestate = "map"
                        else:
                            self.gamedata.gamestate = None

      

            if self.gamedata.gamestate == "map":
                self.runmap()
            else:
                self.runnormal()

            if self.change:
                self.screen.blit(pygame.transform.scale(self.canvas, (self.gamedata.canvas_width,
                                 self.gamedata.canvas_height)), (self.gamedata.canvas_offsetx, self.gamedata.canvas_offsety))
                pygame.display.flip()

            if self.gamedata.gamestate == "map":
                self.change = False
            else:
                self.change = True

            self.clock.tick(30)


game = Game()
game.run_editor()

