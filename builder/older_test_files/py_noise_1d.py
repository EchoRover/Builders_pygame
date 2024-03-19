
import random
import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
size = (200, 200)
screen = pygame.display.set_mode(size,pygame.RESIZABLE + pygame.SCALED)
pygame.display.set_caption("Perlin Noise Visualization")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def perlin1d(count, seed, octave, scalebias=2):
    out = [None for i in range(count)]
    for i in range(count):
        fnoise = 0.0
        fscale = 1.0
        fscaleacc = 0.0

        for j in range(octave):
            pitch = count >> j
            sample1 = int(i / pitch) * pitch
            sample2 = (sample1 + pitch) % count
            blend = (i - sample1) / pitch

            fsample = (1 - blend) * seed[sample1] + blend * seed[sample2]
            fnoise += fsample * fscale
            fscaleacc += fscale
            fscale /= scalebias

        out[i] = fnoise / fscaleacc
    return out

def perlin2d_old(width,height, seed, octave, scale=2):
    out = [[None for x in range(width)] for y in range(height)]

    for x in range(width):
        for y in range(height):
            fnoise = 0.0
            fscale = 1.0
            fscaleacc = 0.0
            for j in range(octave):
                pitch = width >> j
                samplex1 = int(x / pitch) * pitch
                sampley1 = int(y / pitch) * pitch

                samplex2 = (samplex1 + pitch) % width
                sampley2 = (sampley1 + pitch) % height

                blendx = (x - samplex1) / pitch
                blendy = (y - sampley1) / pitch

                fsamplet = (1 - blendx) * seed[sampley1][samplex1] + blendx * seed[sampley1][samplex2]
                fsampleb = (1 - blendx) * seed[sampley2][samplex1] + blendx * seed[sampley2][samplex2]

                fnoise += (blendy * (fsampleb - fsamplet) + fsamplet) * fscale
                fscaleacc += fscale
                fscale /= scale

            out[y][x] = fnoise / fscaleacc
        
    return out

import numpy as np

def create_seed_array(width, height):
    # Generate random values between 0 and 1 for the seed array
    seed_array = np.random.rand(height, width)
    return seed_array

def perlin2d(width, height, seed, octave, scale=2):
    seed_array = np.array(seed)
    out = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            fnoise = 0.0
            fscale = 1.0
            fscaleacc = 0.0
            for j in range(octave):
                pitch = width >> j
                samplex1 = (x // pitch) * pitch
                sampley1 = (y // pitch) * pitch
                samplex2 = (samplex1 + pitch) % width
                sampley2 = (sampley1 + pitch) % height

                blendx = (x - samplex1) / pitch
                blendy = (y - sampley1) / pitch

                fsamplet = (1 - blendx) * seed[sampley1, samplex1] + blendx * seed[sampley1, samplex2]
                fsampleb = (1 - blendx) * seed[sampley2, samplex1] + blendx * seed[sampley2, samplex2]

                fnoise += (blendy * (fsampleb - fsamplet) + fsamplet) * fscale
                fscaleacc += fscale
                fscale /= scale

            out[y, x] = fnoise / fscaleacc
        
    return out.tolist()




def draw_graph(data):
    if isinstance(data[0], list):  # 2D Perlin noise
        surface = pygame.Surface((len(data[0]), len(data)))
        for x in range(len(data[0])):
            for y in range(len(data)):
                if data[y][x] is not None:
                    color = int(data[y][x] * 255)
                    color = max(0, min(255, color))
                    surface.set_at((x, y), (color, color, color))
        screen.blit(surface, (0, 0))
    else:  # 1D Perlin noise
        screen.fill(BLACK)
        for i in range(len(data) - 1):
            if data[i] is not None:
                pygame.draw.line(screen, WHITE, (i, size[1]), (i, size[1] - int(data[i] * size[1])), 1)

    pygame.display.flip()



def main():
    # Generate seed data
    seed = [random.random() for _ in range(size[0])]
    seed2 = create_seed_array(size[0],size[1])
    octave = 4
    scale = 2

    # 1D or 2D mode flag
    mode = 1  # Default to 1D

    # Generate initial Perlin noise data
    perlin_data = perlin1d(size[0], seed, octave, scale)

    draw_graph(perlin_data)
    change = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                change = 1
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    if mode == 1:
                        seed = [random.random() for _ in range(size[0])]
                    else:
                        seed2 = create_seed_array(size[0],size[1])
                elif event.key == pygame.K_w:
                    mode = 1
                elif event.key == pygame.K_s:
                    mode = 2
                elif event.key == pygame.K_d:
                    scale += 0.02
                    print(scale)
                elif event.key == pygame.K_a:
                    scale = max(scale - 0.02, 0.02)
                    print(scale)
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                     pygame.K_6, pygame.K_7, pygame.K_8]:
                    octave = int(pygame.key.name(event.key))
                    print("oc " ,octave)
   

        if change == 1:

            if mode == 1:     
                perlin_data = perlin1d(size[0], seed, octave, scale)
            elif mode == 2:     
                perlin_data = perlin2d(size[0], size[1], seed2, octave, scale)
                # perlin_data = perlin2d(seed[0],seed[1],scale,seed,octave)

            draw_graph(perlin_data)
            change = 0
        

if __name__ == "__main__":
    main()

