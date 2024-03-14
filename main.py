import pygame
import random
import math
import os
pygame.init()



class Gamedata:
    def __init__(self):
        

        ...
    def setup_cam(self,camx,camy):
        self.camx = camx
        self.camy = camy
   
    def setup_main(self,tilesize,ratio):
        self.aspect_ratio = ratio
        self.tilesize = tilesize
    
   
    def setup_screen(self,screen_width,screen_height):
        self.screen_height = screen_height
        self.screen_width = screen_width

    def setup_screen_tile_lengths(self):
        self.screen_tile_length = math.ceil(
            self.screen_width/self.tilesize) + 1
        self.screen_tile_breadth = math.ceil(
            self.screen_height/self.tilesize) + 1
    
    
    def setupworld(self,worldlength,worldbreadth):
        self.worldlength = worldlength
        self.worldbreadth = worldbreadth
    
    def setup_max_borders(self):
        self.max_length_border = self.tilesize * (self.worldlength - self.screen_tile_length)
        self.max_breadth_border = self.tilesize * (self.worldbreadth - self.screen_tile_breadth)

    
    


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

  


    



class Tiles:
    def __init__(self, t):
        self.TILESIZE = t
        self.Hotbar_scale = 48
   

        self.tile = dict()
        self.Htile = dict()
        self.load_tiles()
    
    def load_tiles(self):
        tiles_folder = "tiles"
        for filename in os.listdir(tiles_folder):
            if filename.endswith(".png"):  
          
                image_path = os.path.join(tiles_folder, filename)
                image = pygame.image.load(image_path).convert_alpha()


                scaled_image = pygame.transform.scale(image, (self.TILESIZE, self.TILESIZE))


                self.tile[filename.rstrip('.png')] = scaled_image
                self.Htile[filename.rstrip('.png')] = pygame.transform.scale(image, (self.Hotbar_scale, self.Hotbar_scale))
        
        

class Cameraold:
    def __init__(self,gamedata):
       
        self.gamedata = gamedata
        self.allowborders = True

        self.direction = pygame.math.Vector2()
        self.resistance = 0.8
        self.acceleration = 3
        self.vx = self.vy = 0
        self.x = self.y = 0

    def inputs(self):
        keys = pygame.key.get_pressed()
        self.direction.y = -(keys[pygame.K_UP] or keys[pygame.K_w]) + \
            (keys[pygame.K_DOWN] or keys[pygame.K_s])
        self.direction.x = (keys[pygame.K_RIGHT] or keys[pygame.K_d]
                            ) - (keys[pygame.K_LEFT] or keys[pygame.K_a])

    def update(self):
        self.inputs()
        if self.direction.length() != 0:
            self.direction.normalize_ip()
        self.vx = round((self.resistance * self.vx) +
                        (self.acceleration * self.direction.x), 3)
        self.vy = round((self.resistance * self.vy) +
                        (self.acceleration * self.direction.y), 3)
        self.x += self.vx
        self.y += self.vy
       
        if self.allowborders:
            self.x = max(0,self.x)
            self.y = max(0,self.y)
            self.x = min(self.x,self.gamedata.max_length_border)
            self.y = min(self.y,self.gamedata.max_breadth_border)
        self.gamedata.camx = self.x
        self.gamedata.camy = self.y

class Camera:
    def __init__(self, gamedata):
        self.gamedata = gamedata
        self.direction = pygame.math.Vector2()
        self.resistance = 0.8
        self.acceleration = 3
        self.velocity = pygame.math.Vector2()  
        self.position = pygame.math.Vector2()  

    def inputs(self):
        keys = pygame.key.get_pressed()
        self.direction.y = -(keys[pygame.K_UP] or keys[pygame.K_w]) + \
            (keys[pygame.K_DOWN] or keys[pygame.K_s])
        self.direction.x = (keys[pygame.K_RIGHT] or keys[pygame.K_d]
                            ) - (keys[pygame.K_LEFT] or keys[pygame.K_a])

    def update(self):
        self.inputs()
        if self.direction.length() != 0:
            self.direction.normalize_ip()
        self.velocity += self.direction * self.acceleration
        self.velocity *= self.resistance
        self.position += self.velocity

        self.position.x = max(0, min(self.position.x, self.gamedata.max_length_border))
        self.position.y = max(0, min(self.position.y, self.gamedata.max_breadth_border))
        
        self.gamedata.camx = self.position.x
        self.gamedata.camy = self.position.y
   


class Editor:
    def __init__(self, gamedata):
    
        self.gamedata = gamedata
    

        self.tiles = Tiles(self.gamedata.tilesize)

        self.createmap()
    
    def addhotbar(self,hotbar):
        self.hotbar = hotbar

    def createmap(self, sizex=100, sizey=100):
        #random.choice(list(self.tiles.tile.keys()))
        self.gameworld = [
            [ "dirt" for _ in range(sizex)] for __ in range(sizey)]
        self.gamedata.setupworld(sizex,sizey)
        self.gamedata.setup_max_borders()
        


    def copymap(self):
        return [row.copy() for row in self.gameworld]

    def get_tile(self):
        #if self.tile_x >= 0 and self.tile_y >= 0 and self.tile_x < self.gamedata.worldlength and self.tile_y < self.gamedata.worldbreadth:
        mx, my = pygame.mouse.get_pos()
        self.tile_x = int((mx + self.gamedata.camx) / self.gamedata.tilesize)
        self.tile_y = int((my + self.gamedata.camy) / self.gamedata.tilesize)
        self.tile = self.gameworld[self.tile_y][self.tile_x]
       

    def handlemouse(self):
     
        if pygame.mouse.get_pressed()[0]:
            self.gameworld[self.tile_y][self.tile_x] = None
        elif pygame.mouse.get_pressed()[2]:

            self.gameworld[self.tile_y][self.tile_x] = self.tiles.tile["stone"]
    
    

    def saveworld(self):
        ...
    
    def mousepress(self):
        self.get_tile()
     
        if pygame.key.get_pressed()[pygame.K_e]:
            newtile = None
        else:
            newtile = self.hotbar.selected_tile
            
        self.gameworld[self.tile_y][self.tile_x] = newtile
        
            

    def update(self):
        self.get_tile()
        self.handlemouse()

class HotBar:
    def __init__(self, gamedata, tiles):
        self.gamedata = gamedata
        self.tiles = tiles
        self.tile_size = 64  
        self.spacing = 5  
        self.num_tiles = 10
      

        self.contain = ["dirt_grass","dirt","stone","sand","water","wood","glass",None,None,None]
        self.bar_width = self.num_tiles * (self.tile_size + self.spacing) + self.spacing
        self.bar_height = self.tile_size + 2 * self.spacing
        self.bar_x = (self.gamedata.screen_width - self.bar_width) // 2
        self.bar_y = self.gamedata.screen_height - self.bar_height - 10

        self.tilespacing = (self.tile_size - 48 )//2
        self.selected_tile_index = 0
        self.selected_tile = self.contain[self.selected_tile_index]

    def draw(self, surface):
        # (105,105,105)
        pygame.draw.rect(surface, (192,192,192), (self.bar_x , self.bar_y, self.bar_width , self.bar_height))
    
        for i, tile in enumerate(self.contain):

            x = self.bar_x + i * (self.tile_size + self.spacing) + self.spacing
            y = self.bar_y + self.spacing
            pygame.draw.rect(surface,(105,105,105), (x,y,self.tile_size,self.tile_size))
            if i == self.selected_tile_index:
                pygame.draw.rect(surface, (220,220,220), (x - self.spacing, y - self.spacing, self.tile_size + 2 * self.spacing, self.tile_size + 2 * self.spacing), 6)

            if tile == None:
                continue

            surface.blit(self.tiles.Htile[tile], (x + self.tilespacing , y + self.tilespacing ))
            

    def ifmouseclick(self):

      
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i in range(self.num_tiles):
            x = self.bar_x + i * (self.tile_size + self.spacing) + self.spacing
            y = self.bar_y + self.spacing
            if x <= mouse_x <= x + self.tile_size and y <= mouse_y <= y + self.tile_size:
                self.selected_tile_index = i
                self.selected_tile = self.contain[i]

                return True
        return False
                


class Game:
    def __init__(self):
 
        self.gamedata = Gamedata()

        self.gamedata.setup_main(32,(16,9))
        self.gamedata.setup_screen(1280,720)
        self.gamedata.setup_screen_tile_lengths()


        self.clock = pygame.time.Clock()
        self.screen = pygame.Surface((self.gamedata.screen_width, self.gamedata.screen_height))
        self.main_screen = pygame.display.set_mode(
            (self.gamedata.screen_width, self.gamedata.screen_height), pygame.RESIZABLE)

        self.editor = 1

        if self.editor == 1:
            self.editor = Editor(self.gamedata)
            self.cam = Camera(self.gamedata)
            self.screengrid = ScreenGrid(self.gamedata,self.editor.tiles)
            self.hotbar = HotBar(self.gamedata, self.editor.tiles)
            self.editor.addhotbar(self.hotbar)



    def run_editor(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.VIDEORESIZE:
                    self.gamedata.screen_width = event.w
                    self.gamedata.screen_height = event.h
                    self.gamedata.setup_screen_tile_lengths()
                    self.gamedata.setup_max_borders()
                
                    screen = pygame.display.set_mode(
                        (self.gamedata.screen_width, self.gamedata.screen_height), pygame.RESIZABLE,pygame.SCALED)
                elif pygame.mouse.get_pressed()[0]:
                    if not self.hotbar.ifmouseclick():
                        self.editor.mousepress()
                 
            self.cam.update()
       
        


            self.screen.fill((255, 255, 255))

            self.screengrid.draw(self.screen, self.editor.gameworld)
            self.hotbar.draw(self.screen)

            self.main_screen.blit(self.screen,(0,0))

            pygame.display.flip()
            self.clock.tick(30)



game = Game()
game.run_editor()
