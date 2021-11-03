import units_QBD
import math 
from . import shroodinger__equation
from . import tools
import numpy
# import scipy.optimize
# import scipy.interpolate


def dos__elementary(energy, space__profile, energy__grid, mass__grid, wave__vector__grid, min__energy__level = 0, max_energy__level=12e-19, energy__interval = 1e-21):
    prefix_0 = (wave__vector__grid[1] - wave__vector__grid[0]) / 2 / math.pi

    counter = 0
    energy__interval__half = energy__interval / 2.

    adjusted__energy__profiles = tools.adjust__energy__profile__to__wave__vector__grid(energy__grid, mass__grid,wave__vector__grid)
    for profile in adjusted__energy__profiles:
        energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level, max_energy__level, energy__interval)
        for energy__level in energy__levels:
            if energy__level - energy__interval__half < energy:
                if energy__level + energy__interval__half > energy:
                    counter += 1
    return prefix_0 * prefix_0 * counter / energy__interval

# def dos__gridded(energy__grid, space__profile, energy__profile, mass__grid, wave__vector__grid, min__energy__level = 0, max_energy__level=12e-19, energy__interval = 1e-21):
#     prefix_0 = (wave__vector__grid[1] - wave__vector__grid[0]) / 2 / math.pi

#     energy__interval__half = (energy__grid[1] - energy__grid[0]) / 2.

#     adjusted__energy__profiles = tools.adjust__energy__profile__to__wave__vector__grid(energy__profile, mass__grid,wave__vector__grid)
    
#     steps = [0] * len(energy__grid)

#     counter = 0
#     for profile in adjusted__energy__profiles:
#         energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level, max_energy__level, energy__interval)
#         for energy__level in energy__levels:
#             for i in range(0,len(energy__grid)):
#                 if energy__level - energy__interval__half < energy__grid[i]:
#                     if energy__level + energy__interval__half > energy__grid[i]:
#                         steps[i] += 1

#     return [prefix_0 * prefix_0 * counter / (energy__grid[1] - energy__grid[0]) for counter in steps]

def dos__gridded(energy__grid, space__profile, energy__profile, mass__grid, wave__vector__grid, min__energy__level = 0, max_energy__level=12e-19, energy__interval = 1e-21):
    prefix_0 = (wave__vector__grid[1] - wave__vector__grid[0]) / 2 / math.pi

    energy__interval__half = (energy__grid[1] - energy__grid[0]) / 2.

    adjusted__energy__profiles = tools.adjust__energy__profile__to__wave__vector__grid(energy__profile, mass__grid,wave__vector__grid)
    
    steps = [0] * len(energy__grid)

    counter = 0
    for profile in adjusted__energy__profiles:
        energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level, max_energy__level, energy__interval)
        for energy__level in energy__levels:
            for i in range(0,len(energy__grid)):
                if energy__level - energy__interval__half < energy__grid[i]:
                    if energy__level + energy__interval__half > energy__grid[i]:
                        steps[i] += 1

    return [prefix_0 * prefix_0 * counter / (energy__grid[1] - energy__grid[0]) for counter in steps]


def dos__gridded__2D(energy__grid, space__profile, energy__profile, mass__grid, wave__vector__grid_A, wave__vector__grid_B, min__energy__level = 0, max_energy__level=10e-19, energy__interval = 1e-21):
    prefix_0 = (wave__vector__grid_A[1] - wave__vector__grid_A[0]) / 2 / math.pi

    energy__grid__interval = energy__grid[1] - energy__grid[0] 
    xx = prefix_0 * prefix_0 / energy__grid__interval
        
    steps = [0] * len(energy__grid)
    steps_ = [0] * len(energy__grid)

    
    flag = True
    for i in range(0,int(len(wave__vector__grid_A) / 2)): 
        if wave__vector__grid_A[i] != -wave__vector__grid_A[-i -1]: 
            flag = False
            break

    if wave__vector__grid_A == wave__vector__grid_B and flag:
        if 0 in wave__vector__grid_A:
            for i in range(0, int(len(wave__vector__grid_A) / 2) + 1):
                for j in range(i + 1,int(len(wave__vector__grid_B) / 2) + 1):
                    k = math.sqrt(wave__vector__grid_A[i] * wave__vector__grid_A[i] + wave__vector__grid_B[j] * wave__vector__grid_B[j])
                    profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
                    energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
                    for energy__level in energy__levels:
                        for l in range(0,len(energy__grid) - 1):
                            if energy__level >= energy__grid[l]:
                                if energy__level <= energy__grid[l+1]:
                                    steps[l] += 1
                                    break
                            else: break
                        if energy__level >= energy__grid[-1]:
                            if energy__level < energy__grid[-1] + energy__grid__interval:
                                steps[-1] += 1
        else:
            for i in range(0, int(len(wave__vector__grid_A) / 2)):
                for j in range(i + 1,int(len(wave__vector__grid_B) / 2)):
                    k = math.sqrt(wave__vector__grid_A[i] * wave__vector__grid_A[i] + wave__vector__grid_B[j] * wave__vector__grid_B[j])
                    profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
                    energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
                    for energy__level in energy__levels:
                        for l in range(0,len(energy__grid) - 1):
                            if energy__level >= energy__grid[l]:
                                if energy__level <= energy__grid[l+1]:
                                    steps[l] += 1
                                    break
                            else: break
                        if energy__level >= energy__grid[-1]:
                            if energy__level < energy__grid[-1] + energy__grid__interval:
                                steps[-1] += 1
        steps = [8 * i for i in steps]
        for i in range(0, int(len(wave__vector__grid_A) / 2)):
            k = math.sqrt(wave__vector__grid_A[i] * wave__vector__grid_A[i] + wave__vector__grid_B[i] * wave__vector__grid_B[i])
            profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
            energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
            for energy__level in energy__levels:
                for l in range(0,len(energy__grid) - 1):
                    if energy__level >= energy__grid[l]:
                        if energy__level <= energy__grid[l+1]:
                            steps_[l] += 1
                            break
                    else: break
                if energy__level >= energy__grid[-1]:
                    if energy__level < energy__grid[-1] + energy__grid__interval:
                        steps_[-1] += 1
    
        if 0 in wave__vector__grid_A:
            for ff in range(0, int(len(wave__vector__grid_A) / 2)):
                k = wave__vector__grid_A[ff]
                profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
                energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
                for energy__level in energy__levels:
                    for i in range(0,len(energy__grid) - 1):
                        if energy__level >= energy__grid[i]:
                            if energy__level <= energy__grid[i+1]:
                                steps_[i] += 1
                                break
                        else: break
                    if energy__level >= energy__grid[-1]:
                        if energy__level < energy__grid[-1] + energy__grid__interval:
                            steps_[-1] += 2
        steps_ = [4 * i for i in steps_]

    else:
        adjusted__energy__profiles = tools.adjust__energy__profile__to__2D__wave__vector__grid(energy__profile, mass__grid, wave__vector__grid_A, wave__vector__grid_B)
        for profile in adjusted__energy__profiles:
            for profile_ in profile:
                energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile_, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
                for energy__level in energy__levels:
                    for i in range(0,len(energy__grid) - 1):
                        if energy__level >= energy__grid[i]:
                            if energy__level <= energy__grid[i+1]:
                                steps[i] += 1
                                break
                        else: break
                    if energy__level >= energy__grid[-1]:
                        if energy__level < energy__grid[-1] + energy__grid__interval:
                            steps[-1] += 1

    return [xx * (steps[i] + steps_[i]) for i in range(0,len(steps))]



# def dos__gridded__2D(energy__grid, space__profile, energy__profile, mass__grid, wave__vector__grid_A, wave__vector__grid_B, min__energy__level = 0, max_energy__level=10e-19, energy__interval = 1e-21):
#     prefix_0 = (wave__vector__grid_A[1] - wave__vector__grid_A[0]) / 2 / math.pi

#     energy__grid__interval = energy__grid[1] - energy__grid[0] 

#     adjusted__energy__profiles = tools.adjust__energy__profile__to__2D__wave__vector__grid(energy__profile, mass__grid, wave__vector__grid_A, wave__vector__grid_B)
    

#     xx = prefix_0 * prefix_0 / energy__grid__interval
#     steps = [0] * len(energy__grid)

#     for profile in adjusted__energy__profiles:
#         for profile_ in profile:
#             energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile_, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
#             for energy__level in energy__levels:
#                 for i in range(0,len(energy__grid) - 1):
#                     if energy__level >= energy__grid[i]:
#                         if energy__level <= energy__grid[i+1]:
#                             steps[i] += 1
#                             break
#                     else: break
#                 if energy__level >= energy__grid[-1]:
#                     if energy__level < energy__grid[-1] + energy__grid__interval:
#                         steps[-1] += 1
#     return [xx * counter for counter in steps]



def dos__gridded__3D(dos__ground, effective__mass, energy__offset, structure__length):
    dos__values = []
    multipler = 1 / math.pi / math.pi * \
        numpy.float_power(2 * effective__mass / units_QBD.H__BAR[0] / units_QBD.H__BAR[0], 1.5)

    for i in range(0,len(dos__ground)):
        if dos__ground[i] < energy__offset:
            dos__values.append(0)
            continue
        else:
            dos__values.append(multipler * numpy.real(numpy.sqrt(dos__ground[i] - energy__offset + 0j) * structure__length))
    
    return dos__ground, dos__values


def dos__merge(dos__ground, dos__2D, dos__3D, energy__offset):
    dos__values = []
    position = 0
    for i in range(0,len(dos__ground)):
        if dos__ground[i] < energy__offset: 
            dos__values.append(dos__2D[i])
            position = i
        else:
            dos__values.append(dos__2D[position] + dos__3D[i])

    return dos__ground, dos__values




def dos__merge__reversed(dos__ground, dos__2D, dos__3D, energy__offset):
    dos__values = []
    position = 0
    for i in range(0,len(dos__ground)):
        if dos__ground[-i -1] > energy__offset: 
            dos__values.append(dos__2D[-i -1])
            position = -i
        else:
            dos__values.append(dos__2D[position -1] + dos__3D[-i -1])

    dos__values.reverse()
    return dos__ground, dos__values














def get__thresholds(dos__ground, dos__fence, eigenvalues, de):

    thresholds = []
    values = []

    for energy in eigenvalues:
        lower__limit = energy - de
        upper__limit = energy + de

        lower__limit__index = ...
        energy__index = ...
        upper__limit__index = ...

        for i in range(0,len(dos__ground[:-1])):
            if dos__ground[i] <= lower__limit:
                if dos__ground[i + 1] > lower__limit:
                    lower__limit__index = i
            if dos__ground[i] <= energy:
                if dos__ground[i + 1] > energy:
                    energy__index = i
            if dos__ground[i] <= upper__limit:
                if dos__ground[i + 1] > upper__limit:
                    upper__limit__index = i
        
        if lower__limit__index == ...: lower__limit__index = 0
        if upper__limit__index == ...: upper__limit__index = len(dos__ground) - 1

        thresholds.append(energy__index)
        max_ = dos__fence[lower__limit__index]
        for i in range(lower__limit__index, upper__limit__index):
            if dos__fence[i] > max_:
                max_ = dos__fence[i]
                thresholds[-1] = i

    values = [dos__fence[i] for i in thresholds]
    thresholds = [dos__ground[i] for i in thresholds]
    return thresholds, values



def get__threshold__height(dos__ground, dos__fence, eigenvalues):

    heights = []
    ind = 0
    for i in range(0,len(dos__ground)):
        if ind < len(eigenvalues):
            if dos__ground[i] >= eigenvalues[ind]:  ind += 1
        if ind != 0:    heights.append(dos__fence[i] / ind)

    threshold = sum(heights) / len(heights)

    return threshold





def dos__gridded__3D__approx(dos__ground, thresholds__ground, thresholds__values, threshold__height, length):

    def dos_3D(energy, offset):
        return  1 / math.pi / math.pi * \
                numpy.float_power(threshold__height * 2. * math.pi, 1.5) * \
                numpy.real(numpy.sqrt(energy - offset + 0j)) * length

    a, b = scipy.optimize.curve_fit(dos_3D, thresholds__ground, thresholds__values, p0=thresholds__ground[0])
    dos__values = []
    print('a:')
    print(a)

    for i in range(0,len(dos__ground)):
        if dos__ground[i] < a:  dos__values.append(0)
        else: dos__values.append(dos_3D(dos__ground[i], a))
    return dos__ground, dos__values
