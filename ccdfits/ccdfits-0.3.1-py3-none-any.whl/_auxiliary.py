import numpy as np

def binCenters(binLimits):
	# define los x como los centros de los bins
	return 0.5*(binLimits[1:]+binLimits[:-1])

def gaussian(x, amplitude, mu, sigma):
    return amplitude * np.exp(-0.5*((x-mu)/sigma)**2)

def recta(x, a, b):
    return a*x +b

class N_gaussians:
    def __init__(self, N):
        self.gaussian_list = []
        self.N = N
        for n in range(N):
            self.gaussian_list.append(gaussian)

    def __call__(self, x, *params):
        evaluated_gaussians = []
        for n in range(self.N):
            this_params = params[n*3:(n+1)*3]
            evaluated_gaussians.append(self.gaussian_list[n](x, *this_params))
        return sum(evaluated_gaussians)
