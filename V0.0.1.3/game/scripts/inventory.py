import pygame

class Item:
    def __init__(self,item):
        self.item = item
        self.ismoving = False
        self.selected = False
    
    def toggle_move_and_selected_on(self):
        self.ismoving = self.selected = True
    def toggle_move_and_selected_off(self):
        self.ismoving = self.selected = False



class HotBar:
    def __init__(self, gamedata, tiles):
        self.gamedata = gamedata
        self.tiles = tiles
        self.tile_size = self.gamedata.HotBar_tile_size
        self.spacing = self.gamedata.HotBar_spacing
        self.num_tiles = self.gamedata.HotBar_num_tiles

        self.selected_tile_index = 0
 
      

        self.contain = ["dirt_grass","dirt","stone","sand","water","wood","glass",None,None,None]
        self.createslots()

        #calculation
        self.bar_width = self.num_tiles * (self.tile_size + self.spacing) + self.spacing
        self.bar_height = self.tile_size + 2 * self.spacing
        self.bar_x = (self.gamedata.canvas_width - self.bar_width) // 2
        self.bar_y = self.gamedata.canvas_height - self.bar_height - 10



       
    
    def createslots(self):
        self.slots = {i:Item(self.contain[i]) for i in range(self.num_tiles)}
        self.slots[self.selected_tile_index].selected = True



    def draw(self, surface,mx,my):
      
        pygame.draw.rect(surface, (112,128,144), (self.bar_x , self.bar_y, self.bar_width , self.bar_height))
        drag = False
    
        for i, tile in self.slots.items():

            x = self.bar_x + i * (self.tile_size + self.spacing) + self.spacing
            y = self.bar_y + self.spacing

            pygame.draw.rect(surface,(105,105,105), (x,y,self.tile_size,self.tile_size))
            if tile.selected:
                pygame.draw.rect(surface,(220,220,220) , (x - self.spacing, y - self.spacing, self.tile_size + 2 * self.spacing, self.tile_size + 2 * self.spacing), 6)
            if not tile.item:
                continue
            if not tile.ismoving:
                surface.blit(self.tiles.Htile[tile.item], (x , y))
                continue
            if not mx:
                self.slots[self.selected_tile_index].ismoving = False
                continue
            drag = tile.item
        if drag:
            surface.blit(self.tiles.Htile[drag],(mx - self.tile_size//2,my - self.tile_size//2))

          
    
    def moveItem(self,mx,my):
        for i in range(self.num_tiles):
            x = self.bar_x + i * (self.tile_size + self.spacing) + self.spacing
            y = self.bar_y + self.spacing
            if x <= mx <= x + self.tile_size and y <= my <= y + self.tile_size:
               
                self.slots[self.selected_tile_index].selected = False
                self.slots[i].toggle_move_and_selected_on()
      
                self.selected_tile_index = i
                return True

    
    def placeItem(self,mx,my):
        for i,newtile in self.slots.items():
            x = self.bar_x + i * (self.tile_size + self.spacing) + self.spacing
            y = self.bar_y + self.spacing
            if x <= mx <= x + self.tile_size and y <= my <= y + self.tile_size:
                if i == self.selected_tile_index:
                    self.slots[i].ismoving = False
                    return

                oldslot = self.selected_tile_index
                olditem = self.slots[self.selected_tile_index].item
    
                self.slots[oldslot].toggle_move_and_selected_off()
                self.slots[oldslot].item = newtile.item

                newtile.item = olditem
                newtile.selected = True
                self.selected_tile_index = i
            
                
      
    
    def touchingmouse(self,mx,my):
        if self.bar_x <= mx <= self.bar_x + self.bar_width:
            if self.bar_y <= my <= self.bar_y + self.bar_height:   
                return True
        return False
    
    def handle_not_touching(self):
        self.slots[self.selected_tile_index].ismoving = False
       

