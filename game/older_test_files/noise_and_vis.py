import ctypes
import pygame
import random
import sys


from platform import system
from os import path


try:
    script_dir = path.dirname(path.abspath(__file__))
except:
    script_dir = os.getcwd()

noise_dir = path.join(script_dir)

if system() == 'Windows':
    lib_extension = '.dll'
    lib_path1 = path.join(noise_dir, "noise32" + lib_extension)
    lib_path2 = path.join(noise_dir, "noise64" + lib_extension)
else:
    lib_extension = '.so'
    lib_path = path.join(noise_dir, "noise" + lib_extension)

if lib_extension == ".dll":
    try:
        lib = ctypes.CDLL(lib_path2)
    except:
        lib = ctypes.CDLL(lib_path1)
else:
    lib = ctypes.CDLL(lib_path)


lib.init()
lib.noise.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
lib.noise.restype = ctypes.c_double
lib.fbm.argtypes = [ctypes.c_double, ctypes.c_double,
                    ctypes.c_double, ctypes.c_int, ctypes.c_double, ctypes.c_double]
lib.fbm.restype = ctypes.c_double

fbm = lib.fbm
noise = lib.noise


class NoiseSee:
    def __init__(self):

        pygame.init()

        self.SW, self.SH = 400, 400

        self.screen = pygame.display.set_mode(
            (self.SW, self.SH), pygame.RESIZABLE + pygame.SCALED)

        self.noise = fbm
        self.seed = 1
        self.octave = 1
        self.amplitude = 1
        self.frequency = 2
        self.clock = pygame.time.Clock()
        self.amplitude_increment = 0.001
        self.frequency_increment = 0.001
        self.off_inc = 0.001
        self.slider_inc = 0.001
        self.reg = 8
        self.off = 0.01
        self.shift = self.reg
        self.slider_left = 0
        self.slider_right = 1

    def draw(self):
        if self.change == 2:
            self.screen.fill((0, 0, 0))

            surface = pygame.Surface((self.SW, self.SH))
            for y in range(self.SH):
                for x in range(self.SW):
                    if self.slider_left == 0 and self.slider_right == 1 :
                        color = int(self.noise(x * self.off, y * self.off, self.seed,
                                    self.octave, self.amplitude, self.frequency) * 255 // 2 + 127)
                        color = max(0, min(255, color))
                    else:
                        noise = (self.noise(x * self.off, y * self.off, self.seed,
                                    self.octave, self.amplitude, self.frequency) + 1 )/2
                        if self.slider_left <= noise <= self.slider_right:
                            # color = 255
                            color = int(self.noise(x * self.off, y * self.off, self.seed,
                                    self.octave, self.amplitude, self.frequency) * 255 // 2 + 127)
                            color = max(0, min(255, color))
                            
                        else:
                            color = 0

                    surface.set_at((x, y), (color, color, color))
            self.screen.blit(surface, (0, 0))
            self.change = 0
            pygame.display.flip()
            print("Done")
            print({"oc": self.octave, "am": self.amplitude,
                  "fr": self.frequency, "seed": self.seed,"offset":self.off, "slider_left":self.slider_left,"slider_right":self.slider_right})
    def instructions(self):
        a = """

        LOADING (allow you to load a specfic noise at start)
        _________________________________________________
        a = NoiseSee()
        a.loader({dict with all values})
        a.run()

        IMMEDIATE SCREEN CHANGE
        --------------------------------------------------
        R key random seed (-1000000 to 1000000)
        T key seed + 1
        E key seed - 1
        1 - 8 number key octave change

        SCREEN CHANGE AFTER ALL BELOW KEYS ARE NOT PRESSED
        --------------------------------------------------
        *Frequency [0,inf)
        W key increase frequency 
        S key decrease frequency 

        *Amplitude [0,inf)
        D key increase amplitude 
        A key decrease amplitude 

        *OFFSET [0.000001,inf)
        UP key increase offset (similar to frequency) 
        DOWN key decreser offset (similar to frequency) 

        *Slider_Left [0,slider_right]
        B key decrease slider_left till 0
        N key increase slider_left value from 0  

        *Slider_Right [slider_left,1]
        N key decrease slider_right from 1 
        M key increase slider_left  till 1

        THESE sliders will show value as:
        *** sliderleft <= noise <= sliderright
        *** all other values are black
        
        **SHIFT decreaese the speed of (W,A,S,D,V,B,N,M,UP_ARROW,DOWN_ARROW) by 700%

        """

        print(a)

    def run(self):
        self.instructions()
        self.change = 2
        keys_pressed = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False,
                        pygame.K_d: False, pygame.K_RSHIFT: False, pygame.K_LSHIFT: False,
                        pygame.K_UP:False,pygame.K_DOWN:False,pygame.K_v:False,pygame.K_b:False,
                        pygame.K_n:False,pygame.K_m:False}

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.WINDOWRESIZED:
                    self.change = 2

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        self.seed = random.randint(-1000000, 1000000)

                        print(self.seed)
                        self.change = 2
                    if event.key == pygame.K_t:
                        self.seed += 1

                        print(self.seed)
                        self.change = 2

                    if event.key == pygame.K_e:
                        self.seed -= 1

                        print(self.seed)
                        self.change = 2

                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                       pygame.K_6, pygame.K_7, pygame.K_8]:
                        self.octave = int(pygame.key.name(event.key))
                        self.change = 2
                        print("oc ", self.octave)

                    elif event.key in keys_pressed:
                        keys_pressed[event.key] = True
                        self.change = 1
                        if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                            self.shift = 1

                elif event.type == pygame.KEYUP:

                    if event.key in keys_pressed:
                        keys_pressed[event.key] = False
                        if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                            self.shift = self.reg
                    if self.change == 1 and (True not in keys_pressed.values()):

                        self.change = 2

            if keys_pressed[pygame.K_w]:
                self.frequency = max(0, self.frequency +
                                     self.frequency_increment * self.shift)
                print("fr", self.frequency)
            elif keys_pressed[pygame.K_s]:
                self.frequency = max(0, self.frequency -
                                     self.frequency_increment * self.shift)
                print("fr", self.frequency)
            elif keys_pressed[pygame.K_a]:
                self.amplitude = max(0, self.amplitude -
                                     self.amplitude_increment * self.shift)
                print("am", self.amplitude)
            elif keys_pressed[pygame.K_d]:
                self.amplitude = max(0, self.amplitude +
                                     self.amplitude_increment * self.shift)
                print("am", self.amplitude)
            elif keys_pressed[pygame.K_DOWN]:
                self.off = max(0.0000001, self.off -
                                     self.off_inc * self.shift)
                print("offset", self.off)
            elif keys_pressed[pygame.K_UP]:
                self.off = max(0.000001, self.off +
                                     self.off_inc * self.shift)
                print("offset", self.off)
            elif keys_pressed[pygame.K_v]:
             
                self.slider_left = round(max(0, self.slider_left - self.slider_inc * self.shift),6)
               
                print("slider_left", self.slider_left)
            elif keys_pressed[pygame.K_b]:
             
                self.slider_left = round(min(self.slider_right, self.slider_left + self.slider_inc * self.shift),6)
                print("slider_left", self.slider_left)
            
            elif keys_pressed[pygame.K_n]:
             
                self.slider_right = round(max(self.slider_left, self.slider_right - self.slider_inc * self.shift),6)
               
                print("slider_right", self.slider_left)
            elif keys_pressed[pygame.K_m]:
             
                self.slider_right = round(min(1, self.slider_right + self.slider_inc * self.shift),6)
                print("slider_right", self.slider_right)

            self.draw()

            self.clock.tick(30)

    
    def loader(self,data):
        self.octave = data["oc"]
        self.amplitude = data["am"]
        self.frequency = data["fr"]
        self.seed = data["seed"]
        self.off = data["offset"]
        self.slider_left = data["slider_left"]
        self.slider_right = data["slider_right"]


a = NoiseSee()
# a.loader({'oc': 1, 'am': 1, 'fr': 2, 'seed': 516309, 'offset': 0.01, 'slider_left': 0.552, 'slider_right': 1})
a.run()
