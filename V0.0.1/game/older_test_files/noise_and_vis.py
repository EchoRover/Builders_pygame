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
        self.reg = 8
        self.shift = self.reg

    def draw(self):
        if self.change == 2:
            self.screen.fill((0, 0, 0))

            surface = pygame.Surface((self.SW, self.SH))
            for y in range(self.SH):
                for x in range(self.SW):
                    color = int(self.noise(x * 0.01, y * 0.01, self.seed,
                                self.octave, self.amplitude, self.frequency) * 255 // 2 + 127)
                    color = max(0, min(255, color))
                    surface.set_at((x, y), (color, color, color))
            self.screen.blit(surface, (0, 0))
            self.change = 0
            pygame.display.flip()
            print("Done")
            print({"oc": self.octave, "am": self.amplitude,
                  "fr": self.frequency, "seed": self.seed})
    def instructions(self):
        a = """
        R key random seed (-1000000 to 1000000)
        1 - 8 number key octave change


        W key increase frequency 
        S key decrease frequency

        D key increase frequencey
        A key decrease frequencey

        SHIFT decreaese the speed of (WASD) by 700%

        After all keys are pressed the image updates

        """

        print(a)

    def run(self):
        self.instructions()
        self.change = 2
        keys_pressed = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False,
                        pygame.K_d: False, pygame.K_RSHIFT: False, pygame.K_LSHIFT: False}

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
                        self.change = 1

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

            self.draw()

            self.clock.tick(30)


a = NoiseSee().run()
