import units_QBD
import math 
import numpy
from . import shroodinger__equation
from . import tools

# def ldos__gridded__2D(energy__grid, space__profile, energy__profile, mass__grid, wave__vector__grid_A, wave__vector__grid_B, min__energy__level = 0, max_energy__level=10e-19, energy__interval = 1e-21):
#     prefix_0 = (wave__vector__grid_A[1] - wave__vector__grid_A[0]) / 2 / math.pi

#     energy__interval__half = (energy__grid[1] - energy__grid[0]) / 2.

#     adjusted__energy__profiles = tools.adjust__energy__profile__to__2D__wave__vector__grid(energy__profile, mass__grid, wave__vector__grid_A, wave__vector__grid_B)
    
#     multi = prefix_0 * prefix_0 / (energy__grid[1] - energy__grid[0]) 

#     steps = [[0] * len(energy__grid) for i in range(0, len(space__profile))]
#     multipler = prefix_0 * prefix_0 / (energy__grid[1] - energy__grid[0])
#     for profile in adjusted__energy__profiles:
#         for profile_ in profile:
#             energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile_, mass__grid, min__energy__level, max_energy__level, energy__interval)
#             for energy__level in energy__levels:
#                 eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile_, mass__grid, energy__level)
#                 eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
#                 for i in range(0,len(energy__grid)):
#                     if energy__level - energy__interval__half < energy__grid[i]:
#                         if energy__level + energy__interval__half > energy__grid[i]:
#                             for z in range(0, len(space__profile)):
#                                 steps[z][i] += multi * eigenfunction[z] * eigenfunction[z]
#                             break
#     return steps



def ldos__gridded__2D(energy__grid, space__profile, energy__profile, mass__grid, wave__vector__grid_A, wave__vector__grid_B, min__energy__level = 0, max_energy__level=10e-19, energy__interval = 1e-21):
    prefix_0 = (wave__vector__grid_A[1] - wave__vector__grid_A[0]) / 2 / math.pi

    energy__grid__interval = energy__grid[1] - energy__grid[0] 
    xx = prefix_0 * prefix_0 / energy__grid__interval
        
    steps = [[0] * len(energy__grid) for i in range(0, len(space__profile))]
    # steps_ = [[0] * len(energy__grid) for i in range(0, len(space__profile))]

    flag = True

    for i in range(0,int(len(wave__vector__grid_A) / 2)): 
        if wave__vector__grid_A[i] != -wave__vector__grid_A[-i -1]: 
            flag = False
            break

    if wave__vector__grid_A == wave__vector__grid_B and flag:
        # for i in range(0, int(len(wave__vector__grid_A) / 2) + 1):
        #     for j in range(i + 1,int(len(wave__vector__grid_B) / 2) + 1):
        #         k = math.sqrt(wave__vector__grid_A[i] * wave__vector__grid_A[i] + wave__vector__grid_B[j] * wave__vector__grid_B[j])
        #         profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
        #         energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
        #         for energy__level in energy__levels:
        #             eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile, mass__grid, energy__level)
        #             eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
        #             for l in range(0,len(energy__grid) - 1):
        #                 if energy__level >= energy__grid[l]:
        #                     if energy__level <= energy__grid[l+1]:
        #                         for z in range(0, len(space__profile)):
        #                             steps[z][l] += 8 * eigenfunction[z] * eigenfunction[z]
        #                         break
        #                 else: break
        #             if energy__level >= energy__grid[-1]:
        #                 if energy__level < energy__grid[-1] + energy__grid__interval:
        #                     for z in range(0, len(space__profile)):
        #                         steps[z][-1] += 8 * eigenfunction[z] * eigenfunction[z]

        for i in range(0, int(len(wave__vector__grid_A) / 2)):
            for j in range(i ,int(len(wave__vector__grid_B) / 2)):
                k = math.sqrt(wave__vector__grid_A[i] * wave__vector__grid_A[i] + wave__vector__grid_B[j] * wave__vector__grid_B[j])
                profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
                energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
                for energy__level in energy__levels:
                    eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile, mass__grid, energy__level)
                    eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
                    for l in range(0,len(energy__grid) - 1):
                        if energy__level >= energy__grid[l]:
                            if energy__level <= energy__grid[l+1]:
                                for z in range(0, len(space__profile)):
                                    steps[z][l] += 8 * eigenfunction[z] * eigenfunction[z]
                                break
                        else: break
                    if energy__level >= energy__grid[-1]:
                        if energy__level < energy__grid[-1] + energy__grid__interval:
                            for z in range(0, len(space__profile)):
                                steps[z][-1] += 8 * eigenfunction[z] * eigenfunction[z]
        # else:
        #     for i in range(0, int(len(wave__vector__grid_A) / 2)):
        #         for j in range(i + 1,int(len(wave__vector__grid_B) / 2)):
        #             k = math.sqrt(wave__vector__grid_A[i] * wave__vector__grid_A[i] + wave__vector__grid_B[j] * wave__vector__grid_B[j])
        #             profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
        #             energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
        #             for energy__level in energy__levels:
        #                 eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile, mass__grid, energy__level)
        #                 eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
        #                 for l in range(0,len(energy__grid) - 1):
        #                     if energy__level >= energy__grid[l]:
        #                         if energy__level <= energy__grid[l+1]:
        #                             for z in range(0, len(space__profile)):
        #                                 steps[z][l] += eigenfunction[z] * eigenfunction[z]
        #                             break
        #                     else: break
        #                 if energy__level >= energy__grid[-1]:
        #                     if energy__level < energy__grid[-1] + energy__grid__interval:
        #                         for z in range(0, len(space__profile)):
        #                             steps[z][-1] += eigenfunction[z] * eigenfunction[z]
        # for aa in range(0,len(steps)):
        #     for bb in range(0,len(steps[aa])):
        #         steps[aa][bb] *= 8

        for i in range(0, int(len(wave__vector__grid_A) / 2)):
                k = abs(math.sqrt(2) * wave__vector__grid_A[i])
                profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
                energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
                for energy__level in energy__levels:
                    eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile, mass__grid, energy__level)
                    eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
                    for l in range(0,len(energy__grid) - 1):
                        if energy__level >= energy__grid[l]:
                            if energy__level <= energy__grid[l+1]:
                                for z in range(0, len(space__profile)):
                                    steps[z][l] += 4 * eigenfunction[z] * eigenfunction[z]
                                break
                        else: break
                    if energy__level >= energy__grid[-1]:
                        if energy__level < energy__grid[-1] + energy__grid__interval:
                            for z in range(0, len(space__profile)):
                                steps[z][-1] += 4 * eigenfunction[z] * eigenfunction[z]
        if 0 in wave__vector__grid_A:
            for ff in range(0, int(len(wave__vector__grid_A) / 2)):
                k = abs(wave__vector__grid_A[ff])
                profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
                energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
                for energy__level in energy__levels:
                    eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile, mass__grid, energy__level)
                    eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
                    for i in range(0,len(energy__grid) - 1):
                        if energy__level >= energy__grid[i]:
                            if energy__level <= energy__grid[i+1]:
                                for z in range(0, len(space__profile)):
                                    steps[z][i] += 4 * eigenfunction[z] * eigenfunction[z]
                                break
                        else: break
                    if energy__level >= energy__grid[-1]:
                        if energy__level < energy__grid[-1] + energy__grid__interval:
                            for z in range(0, len(space__profile)):
                                steps[z][-1] += 4 * eigenfunction[z] * eigenfunction[z]
#    else:
#             for i in range(0, int(len(wave__vector__grid_A) / 2)):
#                 k = math.sqrt(wave__vector__grid_A[i] * wave__vector__grid_A[i] + wave__vector__grid_B[i] * wave__vector__grid_B[i])
#                 profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
#                 energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
#                 for energy__level in energy__levels:
#                     eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile, mass__grid, energy__level)
#                     eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
#                     for l in range(0,len(energy__grid) - 1):
#                         if energy__level >= energy__grid[l]:
#                             if energy__level <= energy__grid[l+1]:
#                                 for z in range(0, len(space__profile)):
#                                     steps_[z][l] += eigenfunction[z] * eigenfunction[z]
#                                 break
#                         else: break
#                     if energy__level >= energy__grid[-1]:
#                         if energy__level < energy__grid[-1] + energy__grid__interval:
#                             for z in range(0, len(space__profile)):
#                                 steps_[z][-1] += eigenfunction[z] * eigenfunction[z]
            # for i in range(0, int(len(wave__vector__grid_A) / 2 + 1)):
            #         k = math.sqrt(2) * wave__vector__grid_A[i]
            #         profile = tools.adjust__energy__profile__to__wave__vector(energy__profile,mass__grid,k)
            #         energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
            #         for energy__level in energy__levels:
            #             eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile, mass__grid, energy__level)
            #             eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
            #             for l in range(0,len(energy__grid) - 1):
            #                 if energy__level >= energy__grid[l]:
            #                     if energy__level <= energy__grid[l+1]:
            #                         for z in range(0, len(space__profile)):
            #                             steps[z][l] += eigenfunction[z] * eigenfunction[z]
            #                         break
            #                 else: break
            #             if energy__level >= energy__grid[-1]:
            #                 if energy__level < energy__grid[-1] + energy__grid__interval:
            #                     for z in range(0, len(space__profile)):
            #                         steps[z][-1] += eigenfunction[z] * eigenfunction[z]


            # for aa in range(0,len(steps)):
            # for bb in range(0,len(steps[aa])):
            #     steps[aa][bb] *= 4

    else:
        adjusted__energy__profiles = tools.adjust__energy__profile__to__2D__wave__vector__grid(energy__profile, mass__grid, wave__vector__grid_A, wave__vector__grid_B)
        for profile in adjusted__energy__profiles:
            for profile_ in profile:
                energy__levels = shroodinger__equation.eigenvalues_1(space__profile, profile_, mass__grid, min__energy__level - energy__grid__interval , max_energy__level + energy__grid__interval, energy__interval)
                for energy__level in energy__levels:
                    eigenfunction = shroodinger__equation.eigenfunctions_1(space__profile, profile_, mass__grid, energy__level)
                    eigenfunction = shroodinger__equation.normalization(eigenfunction, space__profile)
                    for i in range(0,len(energy__grid) - 1):
                        if energy__level >= energy__grid[i]:
                            if energy__level <= energy__grid[i+1]:
                                for z in range(0, len(space__profile)):
                                    steps[z][i] += eigenfunction[z] * eigenfunction[z]
                                break
                        else: break
                    if energy__level >= energy__grid[-1]:
                        if energy__level < energy__grid[-1] + energy__grid__interval:
                            for z in range(0, len(space__profile)):
                                steps[z][-1] += 2 * eigenfunction[z] * eigenfunction[z]

    for aa in range(0,len(steps)):
        for bb in range(0,len(steps[aa])):
            # steps[aa][bb] += steps_[aa][bb]
            steps[aa][bb] *= xx
    return steps


def ldos__gridded__3D(energy__grid, space__profile, effective__mass, energy__offset):
    
    steps = [[0] * len(energy__grid) for i in range(0, len(space__profile))]

    statement = 2 * effective__mass / units_QBD.H__BAR[0] / units_QBD.H__BAR[0]
    multipler = 1 / math.pi / math.pi * \
        math.sqrt(statement * statement * statement)

    for i in range(0,len(steps)):
        for j in range(0,len(steps[i])):
            if energy__grid[j] >= energy__offset:
                steps[i][j] = multipler * numpy.real(numpy.sqrt(energy__grid[j] - energy__offset + 0j))

    return steps



def ldos__merge(space__grid, energy__grid, ldos__2D, ldos__3D, energy__offset):
    ldos__values = [[0] * len(energy__grid) for i in range(0,len(space__grid))]


    for i in range(0,len(space__grid)):
        position = 0
        for j in range(0, len(energy__grid)):
            if energy__grid[j] < energy__offset:
                ldos__values[i][j] = ldos__2D[i][j]
                position = j
            else:
                ldos__values[i][j] = ldos__2D[i][position] + ldos__3D[i][j]

    return ldos__values

def ldos__merge__reversed(space__grid, energy__grid, ldos__2D, ldos__3D, energy__offset):
    ldos__values = [[0] * len(energy__grid) for i in range(0,len(space__grid))]
    for i in range(0,len(space__grid)):
        position = 0
        for j in range(0, len(energy__grid)):
            if energy__grid[-1 -j] > energy__offset:
                ldos__values[i][-1 -j] = ldos__2D[i][-1-j]
                position = -j
            else:
                ldos__values[i][-j -1] = ldos__2D[i][position -1] + ldos__3D[i][-1-j]

    for i in range(0,len(space__grid)):
        ldos__values[i].reverse()

    return ldos__values
