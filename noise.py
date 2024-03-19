import random
import pygame
import sys
import multiprocessing
import numpy as np
SIZE = 255


def permutation_table(num):
    a = list(range(num))
    random.shuffle(a)
    return a * 2


class vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, other):
        return self.x * other.x + self.y * other.y


def constraint(v):
    a = v & 3
    if a == 0:
        return vector2(1, 1)
    elif a == 1:
        return vector2(-1, 1)
    elif a == 2:
        return vector2(-1, -1)
    else:
        return vector2(1, -1)


def lerp(t, a1, a2):
    return (a2 - a1) * t + a1


# 6t5-15t4+10t3
def fade(t):
    return ((6 * t - 15) * t + 10) * t ** 3


def Noise2d(x, y):

    X = int(x) % (256)
    Y = int(y) % (256)
    xf = x - int(x)
    yf = y - int(y)

    topright = vector2(xf - 1, yf - 1)
    topleft = vector2(xf, yf - 1)
    bottomright = vector2(xf - 1, yf)
    bottomleft = vector2(xf, yf)

    valtopright = P[P[X + 1] + Y + 1]
    valtopleft = P[P[X] + Y + 1]
    valbottomright = P[P[X + 1] + Y]
    valbottomleft = P[P[X] + Y]

    dottopright = topright.dot(constraint(valtopright))
    dottopleft = topleft.dot(constraint(valtopleft))
    dotbottomright = bottomright.dot(constraint(valbottomright))
    dotbottomleft = bottomleft.dot(constraint(valbottomleft))

    u = fade(xf)
    v = fade(yf)

    result = lerp(u, lerp(v, dotbottomleft, dottopleft),
                  lerp(v, dotbottomright, dottopright))

    return result


def FractalBrownianMotion(x, y, octave):
    result = 0
    amplitude = 1
    frequency = 0.005
    for o in range(octave):
        result += amplitude * Noise2d(x * frequency, y * frequency)
        amplitude *= 0.5
        frequency *= 2
    return result


P = permutation_table(256)


class Noise3D:
    def __init__(self):
        self.P = [151, 160, 137, 91, 90, 15,
                  131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23,
                  190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33,
                  88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166,
                  77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244,
                  102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196,
                  135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123,
                  5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42,
                  223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
                  129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228,
                  251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107,
                  49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254,
                  138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180] * 2

    def __lerp(self, t, a1, a2):
        return a1 + t * (a2 - a1)

    def __fade(self, t):
        # 6t5-15t4+10t3
        return (((6 * t - 15) * t) + 10) * t ** 3

    def __grad(self, hashh, x, y, z):
        h = hashh & 15
        u = x if h < 8 else y
        v = y if h < 4 else x if h in {12, 14} else z
        return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)

    def noise(self, x, y, z):
        X = int(x) & 255
        Y = int(y) & 255
        Z = int(z) & 255

        x -= int(x)
        y -= int(y)
        z -= int(z)

        u = self.__fade(x)
        v = self.__fade(y)
        w = self.__fade(z)

        A = self.P[X] + Y
        AA = self.P[A] + Z
        AB = self.P[A + 1] + Z

        B = self.P[X + 1] + Y
        BA = self.P[B] + Z
        BB = self.P[B + 1] + Z

        return self.__lerp(w, self.__lerp(v, self.__lerp(u,  self.__grad(self.P[AA], x, y, z),
                                                         self.__grad(self.P[BA], x - 1, y, z)),
                                          self.__lerp(u,  self.__grad(self.P[AB], x, y - 1, z),
                                                      self.__grad(self.P[BB], x - 1, y - 1, z))),
                           self.__lerp(v, self.__lerp(u,  self.__grad(self.P[AA + 1], x, y, z - 1),
                                                      self.__grad(self.P[BA + 1], x - 1, y, z - 1)),
                                       self.__lerp(u,  self.__grad(self.P[AB + 1], x, y - 1, z - 1),
                                                   self.__grad(self.P[BB + 1], x - 1, y - 1, z - 1))))

    def FractalBrownianMotion(self, x, y, z, octave):
        result = 0
        amplitude = 1
        frequency = 0.005
        test = []
        for o in range(octave):
            result += amplitude * \
                self.noise(x * frequency, y * frequency, z * frequency)
            test.append(x, y, z)

            amplitude *= 0.5
            frequency *= 2
        return result


class NoiseSee:
    def __init__(self):
        pygame.init()

        self.SW, self.SH = 300, 300

        self.screen = pygame.display.set_mode(
            (self.SW, self.SH), pygame.RESIZABLE + pygame.SCALED)

        self.noise = Noise3D()
        self.seed = 1
        self.octave = 1

    def draw(self):
        if self.change:
            self.screen.fill((0, 0, 0))

            surface = pygame.Surface((self.SW, self.SH))
            for y in range(self.SH):
                for x in range(self.SW):
                    color = int(self.noise.FractalBrownianMotion(
                        x, y, self.seed, self.octave) * 255 // 2 + 127)
                    color = max(0, min(255, color))
                    surface.set_at((x, y), (color, color, color))
            self.screen.blit(surface, (0, 0))
            self.change = 0
            pygame.display.flip()

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
                        print("oc " ,self.octave)

            self.draw()


a = NoiseSee().run()
# a = Noise3D()
# print(a.noise(0.1,0.2,1))
