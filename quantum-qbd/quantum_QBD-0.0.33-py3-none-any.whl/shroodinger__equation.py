import units_QBD
from math import sqrt

def eigenvalues_1(space__grid, energy__grid, mass__grid,min__energy__level, max__energy__level, level__resolution):
    energy__grid = [energy / units_QBD.SI_['eV'][0] for energy in energy__grid]
    mass__grid = [mass / units_QBD.SI_['m_e'][0] for mass in mass__grid]
    level__resolution_ = level__resolution / units_QBD.SI_['eV'][0]
    min__energy__level_ = min__energy__level / units_QBD.SI_['eV'][0]
    max__energy__level_ = max__energy__level / units_QBD.SI_['eV'][0]

    interval = space__grid[1] - space__grid[0]
    as2 = 2.0 * units_QBD.M_E[0] * units_QBD.E[0] * interval * interval / units_QBD.H__BAR[0] / units_QBD.H__BAR[0]
 
    grid__points__count = len(space__grid)

    AZW_D = [0]
    AZW_U = [0]
    for i in range(1, grid__points__count - 1):
        value =  energy__grid[i] * as2 + 2.0 / (mass__grid[i - 1] + mass__grid[i]) + 2.0 / (mass__grid[i + 1] + mass__grid[i])
        AZW_D.append(value)
    for i in range(1, grid__points__count - 2):
        AZW_U.append(-2.0 / (mass__grid[i + 1] + mass__grid[i]))
    AZW_D.append(0)
    AZW_U.append(0)
    AZW_U.append(0)

    eigenvalues = []
    level = 1
    me = min(energy__grid)
    while(True):
        E_min = me
        E_max = max__energy__level_
        E_ave = 0

        while E_max - E_min > level__resolution_:
            E_ave = (E_max + E_min) / 2
            eta = 0
            u = AZW_D[1] - E_ave * as2
            if u < 0: eta += 1
            for i in range(2, grid__points__count):
                u = AZW_D[i] - E_ave * as2 - AZW_U[i-1] * AZW_U[i-1] / u
                if u < 0: eta += 1

            if eta < level:   
                E_min = E_ave
            else:                           
                E_max = E_ave

        eigenvalues.append(E_ave * units_QBD.SI_['eV'][0])
        level +=1

        if len(eigenvalues) > 1:
            if eigenvalues[-2] == eigenvalues[-1]: 
                break



    c1 = min__energy__level_ * units_QBD.SI_['eV'][0]
    c2 = (me + level__resolution_) * units_QBD.SI_['eV'][0]
    c3 = level__resolution_ * units_QBD.SI_['eV'][0]
    te = []
    for i in eigenvalues[:-2]:
        if i >= c1:
            if i > c2:
                if abs(i) > c3: 
                    te.append(i)
    return te

def eigenfunctions_1(space__grid, energy__grid, mass__grid, energy, k_ii):
    energy__grid = [energy / units_QBD.SI_['eV'][0] for energy in energy__grid]
    mass__grid = [mass / units_QBD.SI_['m_e'][0] for mass in mass__grid]
    energy = energy / units_QBD.SI_['eV'][0]

    interval = space__grid[1] - space__grid[0]
    as2 = 2.0 * units_QBD.M_E[0] * units_QBD.E[0] * interval * interval / units_QBD.H__BAR[0] / units_QBD.H__BAR[0]
 
    grid__points__count = len(space__grid)

    AZW_D = [0]
    AZW_U = [0]
    for i in range(1, grid__points__count - 1):
        value =  energy__grid[i] * as2 + 2.0 / (mass__grid[i - 1] + mass__grid[i]) + 2.0 / (mass__grid[i + 1] + mass__grid[i])
        AZW_D.append(value)
    for i in range(1, grid__points__count - 2):
        AZW_U.append(-2.0 / (mass__grid[i + 1] + mass__grid[i]))
    AZW_D.append(0)
    AZW_U.append(0)
    AZW_U.append(0)

    ThetaM = [0] * grid__points__count
    ThetaM[1] = 1. / (AZW_D[1] - energy * as2)
    for i in range(2,grid__points__count):
        ThetaM[i] = 1 / (AZW_D[i] - energy * as2 - AZW_U[i - 1] * AZW_U[i - 1] * ThetaM[i - 1])

    ThetaP = [0] * grid__points__count
    ThetaP[-1] = 1. / (AZW_D[-1] - energy * as2)
    for i in range(2, grid__points__count - 1):
        i = grid__points__count - i
        ThetaP[i] = 1 / (AZW_D[i] - energy * as2 - AZW_U[i] * AZW_U[i] * ThetaP[i + 1])

    wave__vector = [0] * grid__points__count
    k = k_ii # int(grid__points__count / 2)

    wave__vector[k] = 1
    for i in range(k + 1, grid__points__count - 1):
        wave__vector[i] = -AZW_U[i - 1] * ThetaP[i] * wave__vector[i - 1]
    for i in range(1, k):
        i = k - i
        wave__vector[i] = -AZW_U[i] * ThetaM[i] * wave__vector[i + 1]


    for i in range(1, grid__points__count - 1):
        if abs(wave__vector[k]) < abs(wave__vector[i]): k = i

    wave__vector[k] = 1
    for i in range(k + 1, grid__points__count - 1):
        wave__vector[i] = -AZW_U[i - 1] * ThetaP[i] * wave__vector[i - 1]
    for i in range(1, k):
        i = k - i
        wave__vector[i] = -AZW_U[i] * ThetaM[i] * wave__vector[i + 1]

    # Norma = 0.

    # for i in range(1, grid__points__count): 
    #     Norma += wave__vector[i] * wave__vector[i]
    # Norma *= interval

    # for i in range(1, grid__points__count):
    #     wave__vector[i] /= sqrt(Norma)

    return wave__vector

def normalization(wave__vector, space__grid):
    Norma = 0.

    for wv in wave__vector: 
        Norma += wv * wv
    Norma *= space__grid[1] - space__grid[0]

    return [wv / sqrt(Norma) for wv in wave__vector]
