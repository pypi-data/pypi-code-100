import vnoise

class PerlinNoise:
    def __init__(self, seed=None):
        self.noise = vnoise.Noise(seed)

    def noise2d(self, x, y):
        return self.noise.noise2d(x, y)

    def noise3d(self, x, y, z):
        return self.noise.noise3d(x, y, z)
