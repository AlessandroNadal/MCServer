
import numpy as np
from PIL import Image
import noise


shape = (1024, 1024)
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

world = np.zeros(shape)
for x in range(1024):
    for z in range(1024):
        world[x][z] = noise.pnoise2(
            x/scale,
            z/scale,
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity
        )

img = Image.new("L", shape)
for x, arr in enumerate(world):
    for z, value in enumerate(arr):
        img.putpixel((x, z), int(( (value + 1) / 2 ) * 255))

img.show()
