import units_QBD
import numpy

def profile__plain(thicknesses, values):
    """
    thicknesses = [3,4,5]
    values = [2,3,4]
    """
    ground = [0.]
    fence = [values[0]]

    for i in range(0,len(thicknesses) - 1):
        ground.append(thicknesses[i] + ground[i * 2])
        fence.append(values[i])

        ground.append(thicknesses[i] + ground[i * 2])
        fence.append(values[i + 1])

    ground.append(thicknesses[-1] + ground[-1])
    fence.append(values[-1])

    return ground, fence

def profile__gridded(thicknesses, values, interval=0.1e-10):
    """
    thicknesses = [3,4,5]
    values = [2,3,4]
    """
    total__thickness = 0
    for thickness in thicknesses:   total__thickness += thickness

    profile__ground = numpy.arange(0, total__thickness, interval)

    # if profile__ground[-1] % interval != 0:
    #     profile__ground = numpy.append(profile__ground, [total__thickness])

    profile__breaks = [thicknesses[0]]
    for thickness in thicknesses[1:]: profile__breaks.append(thickness + profile__breaks[-1])

    profile__fence = numpy.array([])
    thicknesses__iterator = 0
    for i in profile__ground:
        if i <= profile__breaks[thicknesses__iterator]: 
            profile__fence = numpy.append(profile__fence, [values[thicknesses__iterator]])
        else: 
            if profile__breaks[thicknesses__iterator] != total__thickness:
                thicknesses__iterator += 1
                profile__fence = numpy.append(profile__fence, [values[thicknesses__iterator]])
                
    return profile__ground, profile__fence






def external__potential__profile__gridded(V__0, V__L, thicknesses, resolution):
    total__thickness = 0
    for thickness in thicknesses:   total__thickness += thickness

    space__grid = [0]
    while space__grid[-1] < total__thickness:
        space__grid.append(space__grid[-1] + resolution)

    ev = []
    a = (V__L - V__0) * units_QBD.E[0] / total__thickness
    V0 = V__0 * units_QBD.E[0]
    for step in space__grid:
        ev.append(a * step + V0)

    return ev