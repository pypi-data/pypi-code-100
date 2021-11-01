import opensimplex

class SimplexNoise:
    def __init__(self, seed=None):
        if seed is None:
            seed = 0
        self.noise = opensimplex.OpenSimplex(seed)

    def noise2d(self, x, y):
        return self.noise.noise2d(x, y)

    def noise3d(self, x, y, z):
        return self.noise.noise3d(x, y, z)
