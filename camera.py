import pygame


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
   
