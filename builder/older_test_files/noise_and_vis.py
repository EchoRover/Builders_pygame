import ctypes
import pygame
import random
import sys
lib = ctypes.CDLL("noise.so")  


lib.init()
lib.noise.argtypes = [ctypes.c_double, ctypes.c_double,ctypes.c_double]
lib.noise.restype = ctypes.c_double
lib.fbm.argtypes = [ctypes.c_double, ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_double,ctypes.c_double]
lib.fbm.restype = ctypes.c_double

fbm = lib.fbm
noise = lib.noise


class NoiseSee:
    def __init__(self):
    
        pygame.init()

        self.SW, self.SH = 800, 800

        self.screen = pygame.display.set_mode(
            (self.SW, self.SH), pygame.RESIZABLE + pygame.SCALED)

        self.noise = fbm
        self.seed = 1
        self.octave = 1
        self.amplitude = 1
        self.frequency = 2

    def draw(self):
        if self.change:
            self.screen.fill((0, 0, 0))

            surface = pygame.Surface((self.SW, self.SH))
            for y in range(self.SH):
                for x in range(self.SW):
                    color = int(self.noise(x * 0.01,y * 0.01,self.seed,self.octave,self.amplitude,self.frequency) * 255 // 2 + 127)
                    color = max(0, min(255, color))
                    surface.set_at((x, y), (color, color, color))
            self.screen.blit(surface, (0, 0))
            self.change = 0
            pygame.display.flip()
            print("Done")

    def run(self):
        self.change = 1
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        self.seed = random.randint(1, 1000)
                   
                        print(self.seed)
                        self.change = 1

                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                     pygame.K_6, pygame.K_7, pygame.K_8]:
                        self.octave = int(pygame.key.name(event.key))
                        self.change = 1
                        print("oc " ,self.octave)
                    
                    elif event.key == pygame.K_d:
                        self.amplitude = max(0, self.amplitude + 0.02)
                        print("am", self.amplitude)
                        self.change = 1
                    elif event.key == pygame.K_a:
                        self.amplitude = max(0, self.amplitude - 0.02)
                        print("am", self.amplitude)
                        self.change = 1
                    elif event.key == pygame.K_w:
                        self.frequency = max(0.001, self.frequency + 0.02)
                        print("fr", self.frequency)
                        self.change = 1
                    elif event.key == pygame.K_s:
                        self.frequency = max(0.001, self.frequency - 0.02)
                        print("fr", self.frequency)
                        self.change = 1


            self.draw()


a = NoiseSee().run()
