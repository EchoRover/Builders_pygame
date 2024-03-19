SIZE = 255
import random

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
