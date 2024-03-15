import pygame
import random
import math
import os
pygame.init()



class Gamedata:
    def __init__(self):
        self.gamestate = None
        

        ...
    def setup_cam(self,camx,camy):
        self.camx = camx
        self.camy = camy
   
    def setup_main(self,tilesize,ratio,Hsize):
        self.aspect_ratio = ratio
        self.tilesize = tilesize
        self.hotbarsize = Hsize
        self.screen = None
  
    
   
    def setup_screen(self,canvas_width,canvas_height):
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
        self.screen_tile_length = math.ceil(
            self.canvas_width/self.tilesize) + 1
        self.screen_tile_breadth = math.ceil(
            self.canvas_height/self.tilesize) + 1
    
    
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
    def __init__(self, t,hotbarsize):
        self.TILESIZE = t
        self.Hotbar_scale = hotbarsize
   

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
        self.acceleration = 4
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
   

class minimap:
    def __init__(self,gamedata,tiles):
        self.gamedate = gamedata
        self.tiles = tiles
        pass
    def drawmap(self,map,surf):
        tilesize = max(self.gamedate.canvas_height//self.gamedate.worldbreadth,self.gamedate.canvas_width//self.gamedate.worldlength)
        tilesize = 1
        
       
        offsetx = self.gamedate.canvas_width - tilesize * self.gamedate.worldlength
        offsetx /= 2
        offsety = self.gamedate.canvas_height - tilesize * self.gamedate.worldbreadth
        offsety /= 2

    
        for y in range(self.gamedate.worldbreadth):
            for x in range(self.gamedate.worldlength):
                surf.blit(pygame.transform.scale(self.tiles.tile[map[y][x]],(tilesize,tilesize)),(tilesize * x + offsetx,tilesize * y + offsety))

class Editor:
    def __init__(self, gamedata):
    
        self.gamedata = gamedata
    

        self.tiles = Tiles(self.gamedata.tilesize,self.gamedata.hotbarsize)

        self.createmap()
        self.generate()
    
    def addhotbar(self,hotbar):
        self.hotbar = hotbar

    def createmap(self, sizex=300, sizey=300):
        #random.choice(list(self.tiles.tile.keys()))
        self.gameworld = [
            [ "dirt" for _ in range(sizex)] for __ in range(sizey)]
        self.gamedata.setupworld(sizex,sizey)
        self.gamedata.setup_max_borders()
        


    def copymap(self):
        return [row.copy() for row in self.gameworld]
    
    def generate(self):
        for y in range(self.gamedata.worldbreadth//3,self.gamedata.worldbreadth):
            for x in range(self.gamedata.worldlength):
                self.gameworld[y][x] = "stone"


    def get_tile(self,x,y):
        #if self.tile_x >= 0 and self.tile_y >= 0 and self.tile_x < self.gamedata.worldlength and self.tile_y < self.gamedata.worldbreadth:
        mx, my = x,y
        self.tile_x = int((mx + self.gamedata.camx) / self.gamedata.tilesize)
        self.tile_y = int((my + self.gamedata.camy) / self.gamedata.tilesize)
        try:
            self.tile = self.gameworld[self.tile_y][self.tile_x]
        except:
            print(f" tile x and y {self.tile_x,self.tile_y}")
            self.tile = None
      
       

    def handlemouse(self):
     
        if pygame.mouse.get_pressed()[0]:
            self.gameworld[self.tile_y][self.tile_x] = None
        elif pygame.mouse.get_pressed()[2]:

            self.gameworld[self.tile_y][self.tile_x] = self.tiles.tile["stone"]
    
    

    def saveworld(self):
        ...
    
    def mousepress(self,x,y):
        self.get_tile(x,y)
     
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

class HotBar:
    def __init__(self, gamedata, tiles,mouse):
        self.gamedata = gamedata
        self.mouse = mouse
        self.tiles = tiles
        self.tile_size = 48
        self.spacing = 5  
        self.num_tiles = 10
      

        self.contain = ["dirt_grass","dirt","stone","sand","water","wood","glass",None,None,None]
        self.bar_width = self.num_tiles * (self.tile_size + self.spacing) + self.spacing
        self.bar_height = self.tile_size + 2 * self.spacing
        self.bar_x = (self.gamedata.canvas_width - self.bar_width) // 2
        self.bar_y = self.gamedata.canvas_height - self.bar_height - 10

        self.tilespacing = (self.tile_size - 48 )//2
        self.selected_tile_index = 0
        self.selected_tile = self.contain[self.selected_tile_index]

    def draw(self, surface):
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
            

    def ifmouseclick(self,mx,my):
        for i in range(self.num_tiles):
            x = self.bar_x + i * (self.tile_size + self.spacing) + self.spacing
            y = self.bar_y + self.spacing
            if x <= mx <= x + self.tile_size and y <= my <= y + self.tile_size:
                self.selected_tile_index = i
                self.selected_tile = self.contain[i]
                if self.mouse.state == "leave":
                    if self.selected_tile == None:
                        self.contain[i] = self.mouse.tile
                        self.contain[self.mouse.index] = None
                        self.selected_tile_index = self.mouse.index
                        self.selected_tile = self.mouse.tile
                        self.mouse.state = None
                        self.mouse.index = None
                        self.mouse.tile = None
                    else:
                        break


                else:
                    self.mouse.drag(self.selected_tile,self.selected_tile_index)
            

                return True
        if self.mouse.state == "leave":
            self.mouse.state = None
            self.mouse.index = None
            self.mouse.tile = None
        return False
    
    def drawdrag(self,surf):
     
        if self.mouse.state == "drag" and self.mouse.tile:
            print(self.mouse.state)
            surf.blit(self.tiles.Htile[self.mouse.tile],(self.mouse.x - self.tile_size//2,self.mouse.y - self.tile_size//2))



class Mouse:
    def __init__(self):
        self.state = None
        self.x,self.y = None,None
        self.tile = None
        self.index = None

    def setpos(self,x,y):
        self.x = x
        self.y = y
    
    def drag(self,tile,idx):
        self.state = "drag"
        self.tile = tile
        self.index = idx
class Game:
    def __init__(self):
 
        self.gamedata = Gamedata()

        self.gamedata.setup_main(64,16/9,48)
        self.gamedata.setup_screen(1280,720)
        self.gamedata.setup_screen_tile_lengths()


        self.clock = pygame.time.Clock()
        self.canvas = pygame.Surface((self.gamedata.canvas_width, self.gamedata.canvas_height))
        self.screen = pygame.display.set_mode(
            (self.gamedata.canvas_width, self.gamedata.canvas_height), pygame.RESIZABLE)
        self.gamedata.screen = self.screen
        self.gamedata.update_screensize()

        self.editor = 1

        if self.editor == 1:
            self.editor = Editor(self.gamedata)
            self.cam = Camera(self.gamedata)
            self.mouse = Mouse()
            self.screengrid = ScreenGrid(self.gamedata,self.editor.tiles)
            self.hotbar = HotBar(self.gamedata, self.editor.tiles,self.mouse)
            self.editor.addhotbar(self.hotbar)
            self.minemap = minimap(self.gamedata,self.editor.tiles)
        

    
    def handlemouse(self,mx = None,my = None):
        self.mouse.setpos(mx,my)
        if self.mouse.state == "leave":
            self.hotbar.ifmouseclick(mx,my)

        if self.mouse.state == "drag":
            return


        

        if not self.hotbar.ifmouseclick(mx,my):
            self.editor.mousepress(mx,my)
       


    




 





    def run_editor(self):
        bef = None
 
      
        while True:
            if bef != self.mouse.state:

                print(self.mouse.state)
                bef = self.mouse.state

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.WINDOWRESIZED:
            
                 
                    self.gamedata.update_screensize()
                
                elif pygame.mouse.get_pressed()[0]:
                    x,y = pygame.mouse.get_pos()
                    if (self.gamedata.canvas_offsetx <=  x <= self.gamedata.mousemaxW and  self.gamedata.canvas_offsety <= y <= self.gamedata.mouseminH):
                        mx = (x - self.gamedata.canvas_offsetx) * self.gamedata.mouse_x_multiplier
                        my = (y - self.gamedata.canvas_offsety) * self.gamedata.mouse_y_multiplier
                        self.handlemouse(mx,my)
                    
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    x,y = pygame.mouse.get_pos()
                    if (self.gamedata.canvas_offsetx <=  x <= self.gamedata.mousemaxW and  self.gamedata.canvas_offsety <= y <= self.gamedata.mouseminH):
                        mx = (x - self.gamedata.canvas_offsetx) * self.gamedata.mouse_x_multiplier
                        my = (y - self.gamedata.canvas_offsety) * self.gamedata.mouse_y_multiplier
                        self.mouse.state = "leave"
                        self.handlemouse(mx,my)
                    else:
                        self.mouse.state = None
                    


            
                     
         
                      
                 
            self.cam.update()
            
       
        
            self.canvas.fill((255, 255, 255))
            self.screen.fill((0,0,0))

            self.screengrid.draw(self.canvas, self.editor.gameworld)
            self.hotbar.draw(self.canvas)
            self.hotbar.drawdrag(self.canvas)
            # self.minemap.drawmap(self.editor.gameworld,self.canvas)
         

              
            self.screen.blit(pygame.transform.scale(self.canvas, (self.gamedata.canvas_width,self.gamedata.canvas_height)),(self.gamedata.canvas_offsetx,self.gamedata.canvas_offsety))
        
        

            pygame.display.flip()
            self.clock.tick(30)




    

game = Game()
game.run_editor()


