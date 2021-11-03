import units_QBD
from math import sqrt

def adjust__energy__to__wave__vector(energy, wave__vector, effective__mass = units_QBD.SI_['m_e'][0]):
    return energy + units_QBD.H__BAR[0] * units_QBD.H__BAR[0] * wave__vector * wave__vector / effective__mass / 2.

def adjust__energy__profile__to__wave__vector(energy__profile__fence, effective__mass__profile__fence, wave__vector):
    adjusted__energy = []
    multiplier = units_QBD.H__BAR[0] * units_QBD.H__BAR[0] / 2.
    for i in range(0, len(energy__profile__fence)):
        adjusted__energy.append(energy__profile__fence[i]  + multiplier * wave__vector * wave__vector / effective__mass__profile__fence[i])
    return adjusted__energy

def adjust__energy__profile__to__wave__vector__grid(energy__profile__fence, effective__mass__profile__fence, wave__vector__grid):
    adjusted__energy__grid = []
    multiplier = units_QBD.H__BAR[0] * units_QBD.H__BAR[0] / 2.
    for k in wave__vector__grid:
        adjusted__energy = []
        for i in range(0, len(energy__profile__fence)):
            adjusted__energy.append(energy__profile__fence[i]  + multiplier * k * k / effective__mass__profile__fence[i])
        adjusted__energy__grid.append(adjusted__energy)
    return adjusted__energy__grid

def adjust__energy__profile__to__2D__wave__vector__grid(energy__profile__fence, effective__mass__profile__fence, wave__vector__grid__A, wave__vector__grid__B):
    adjusted__energy__grid = []
    multiplier = units_QBD.H__BAR[0] * units_QBD.H__BAR[0] / 2.
    for k_A in wave__vector__grid__A:
        adjusted__energy_A = []
        for k_B in wave__vector__grid__B:
            k2 = k_A * k_A + k_B * k_B
            adjusted__energy_B = []
            for i in range(0, len(energy__profile__fence)):
                adjusted__energy_B.append(energy__profile__fence[i]  + multiplier * k2 / effective__mass__profile__fence[i])
            adjusted__energy_A.append(adjusted__energy_B)
        adjusted__energy__grid.append(adjusted__energy_A)
    return adjusted__energy__grid











def fermi__level__profile(bandgap__profile, vbo__profile):
    return [(bandgap__profile[i] + vbo__profile[i]) / 2. for i in range(0,len(bandgap__profile))] 
 
def applied__voltage(profile__ground, profile__fence, dvdz = 1e-9, dvdz__offset=0):
    return [profile__fence[i] + profile__ground[i] * dvdz + dvdz__offset for i in range(0,len(profile__ground))]



# def quasi__fermi__level__profile(fermi__level__profile, ):

