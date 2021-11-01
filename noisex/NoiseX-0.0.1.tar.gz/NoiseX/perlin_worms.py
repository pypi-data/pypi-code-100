from simplex_noise import *
import random
import math

class PerlinWorm:
    def __init__(self,coords=(0,0,0)):
        self.coords = coords
        self.noise = SimplexNoise()

    def make_worm(self):
        length = random.randint(10,100)
        worm = []
        for i in range(length):
            data = {}

            data['radius'] = self.noise.noise3d(self.coords[0],self.coords[1],i)*10
            data['angle'] = self.noise.noise3d(self.coords[0],self.coords[1],i)*360
            data['coords'] = (self.coords[0]+data['radius']*math.cos(data['angle']),self.coords[1]+data['radius']*math.sin(data['angle']))

            worm.append(data)
