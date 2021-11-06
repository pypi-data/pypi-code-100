# -*- coding: utf-8 -*-
"""
Created on Sun May  2 15:10:11 2021

@author: 184277J
"""

import math
import sys
import copy
import pdiffutils as du


def first_last_index(lst, val):
    """
    Returns a tuple containing the first and last indicies

    If the number doesn't appear at the end, then len(lst)
    is returned in it's place

    These are the test cases:
        t1 = [1,1,2,2,2,3,3,3,4,4,5,5,5,4,4,3,3,3,2,1] # totally balanced
        t2 = [1,1,2,2,2,3,3,3,4,4,5,5,5,4,4,3,3,3,2,2] # 1 not balanced at the end of array
        t3 = [1,1,2,2,2,3,3,3,4,4,5,5,5,4,4,2,2,2,2,2] # 3 doesn't appear on the right side
        t4 = [1,1,2,2,2,2,2,4,4,4,5,5,5,4,4,3,3,3,2,2] # 3 doesn't appear on the left side
        t5 = [1,1,2,2,2,3,3,3,4,4,5,6,5,4,4,3,3,3,2,1] # 6 appears just once
        t6 = [1,1,2,2,2,2,2,4,4,4,5,5,5,4,4,4,4,2,2,2] # 3 doesn't appear at all
        t7 = [1,1,2,2,2,2,3,4,4,4,5,5,5,4,4,2,2,2,2,2] # 3 appears once

        a1 = (5, 17)
        a2 = (5, 17)
        a3 = (5, 14)
        a4 = (7, 17)
        a5 = (5, 17)
        a6 = (7, 16)
        a7 = (6, 14)

        print(first_last_index(t1,3) == a1, first_last_index(t1,3),a1)
        print(first_last_index(t2,3) == a2, first_last_index(t2,3),a2)
        print(first_last_index(t3,3) == a3, first_last_index(t3,3),a3)
        print(first_last_index(t4,3) == a4, first_last_index(t4,3),a4)
        print(first_last_index(t5,3) == a5, first_last_index(t5,3),a5)
        print(first_last_index(t6,3) == a6, first_last_index(t6,3),a6)
        print(first_last_index(t7,3) == a7, first_last_index(t7,3),a7)

    Parameters
    ----------
    lst : list of floats or ints
    val : the value to find in the list

    Returns
    -------
    tuple containing indicies first and last appearances, inclusive on both sides

    """
    max_ = max(lst)

    if val > max_:
        raise ValueError(f"{val} is bigger than maximum value.")

    # get the first
    while val <= max_:
        try:
            first = lst.index(val)
            break
        except ValueError:
            val += 1

    if first > 0:
        while lst[first - 1] > lst[first]:
            first -= 1

    while first > 0:
        if lst[first - 1] > lst[lst.index(val)]:
            first -= 1
        else:
            break

    # get the last
    if lst[-1] > val:
        last = len(lst)
    else:
        last = len(lst) - lst[::-1].index(val)

    while last < len(lst):
        if lst[last] < lst[first]:  # then there really is only one
            break
        try:
            val += 1
            last = len(lst) - lst[::-1].index(val)
        except ValueError:
            val -= 1
            last = len(lst) - lst[::-1].index(val)

    return first, last - 1


def removeExtension(filename):
    """
    Removes the extension on a filename

    Parameters
    ----------
    filename : String
        the name of a file

    Returns
    -------
    string without an extension
    """
    return filename[0:filename.rindex(".")]


def group(lst, n):
    """
    Splits a list into tuples of length n
    https://stackoverflow.com/a/15480610/36061

    eg
    a = 'Moscow|city|London|city|Royston Vasey|vilage'
    list(group(a.split('|'), 2))
    gives
    [('Moscow', 'city'), ('London', 'city'), ('Royston Vasey', 'vilage')]


    Parameters
    ----------
    lst : a list
    n : int, number of entries per tuple

    Returns
    ------
    list of tuples, each of length n
    """
    r = []
    for i in range(0, len(lst), n):
        val = lst[i:i + n]
        if len(val) == n:
            r.append(tuple(val))
    return r


# all values and functions for the I_n-L_n functions taken from
# Macleod, A. J. 1993. "Chebyshev Expansions for Modified Struve and Related Functions." Mathematics of Computation 60 (202). doi: 10.2307/2153112.
# MacLeod, A. J. 1996. "Algorithm 757 MISCFUN, a Software Package to Compute Uncommon Special Functions." ACM Transactions on Mathematical Software 22 (3): 288-301. doi: 10.1145/232826.232846.
# https://people.sc.fsu.edu/~jburkardt/f77_src/toms757/toms757.f
TWOBPI = 0.63661977236758134308

g2 = (0.52468736791485599138e0,
      -0.35612460699650586196e0,
      0.20487202864009927687e0,
      -0.10418640520402693629e0,
      0.4634211095548429228e-1,
      -0.1790587192403498630e-1,
      0.597968695481143177e-2,
      -0.171777547693565429e-2,
      0.42204654469171422e-3,
      -0.8796178522094125e-4,
      0.1535434234869223e-4,
      -0.219780769584743e-5,
      0.24820683936666e-6,
      -0.2032706035607e-7,
      0.90984198421e-9,
      0.2561793929e-10,
      -0.710609790e-11,
      0.32716960e-12,
      0.2300215e-13,
      -0.292109e-14,
      -0.3566e-16,
      0.1832e-16,
      -0.10e-18,
      -0.11e-18)

g3 = (2.00326510241160643125e0,
      0.195206851576492081e-2,
      0.38239523569908328e-3,
      0.7534280817054436e-4,
      0.1495957655897078e-4,
      0.299940531210557e-5,
      0.60769604822459e-6,
      0.12399495544506e-6,
      0.2523262552649e-7,
      0.504634857332e-8,
      0.97913236230e-9,
      0.18389115241e-9,
      0.3376309278e-10,
      0.611179703e-11,
      0.108472972e-11,
      0.18861271e-12,
      0.3280345e-13,
      0.565647e-14,
      0.93300e-15,
      0.15881e-15,
      0.2791e-16,
      0.389e-17,
      0.70e-18,
      0.16e-18)

g5 = (0.67536369062350576137e0,
      -0.38134971097266559040e0,
      0.17452170775133943559e0,
      -0.7062105887235025061e-1,
      0.2517341413558803702e-1,
      -0.787098561606423321e-2,
      0.214814368651922006e-2,
      -0.50862199717906236e-3,
      0.10362608280442330e-3,
      -0.1795447212057247e-4,
      0.259788274515414e-5,
      -0.30442406324667e-6,
      0.2720239894766e-7,
      -0.158126144190e-8,
      0.1816209172e-10,
      0.647967659e-11,
      -0.54113290e-12,
      -0.308311e-14,
      0.305638e-14,
      -0.9717e-16,
      -0.1422e-16,
      0.84e-18,
      0.7e-19,
      -0.1e-19)

g6 = (1.99679361896789136501e0,
      -0.190663261409686132e-2,
      -0.36094622410174481e-3,
      -0.6841847304599820e-4,
      -0.1299008228509426e-4,
      -0.247152188705765e-5,
      -0.47147839691972e-6,
      -0.9020819982592e-7,
      -0.1730458637504e-7,
      -0.33232367015e-8,
      -0.63736421735e-9,
      -0.12180239756e-9,
      -0.2317346832e-10,
      -0.439068833e-11,
      -0.82847110e-12,
      -0.15562249e-12,
      -0.2913112e-13,
      -0.543965e-14,
      -0.101177e-14,
      -0.18767e-15,
      -0.3484e-16,
      -0.643e-17,
      -0.118e-17,
      -0.22e-18,
      -0.4e-19,
      -0.1e-19)


def diff0_small(x):
    t = (6.0 * x - 40.0) / (x + 40.0)
    return cheval(len(g2), g2, t)


def diff0_large(x):
    t = (800 - x * x) / (288 + x * x)
    return cheval(22, g3, t) * TWOBPI / x


def diff1_small(x):
    t = (6 * x - 40) / (x + 40)
    return cheval(21, g5, t) * x / 2.0


def diff1_large(x):
    t = (800 - x * x) / (288 + x * x)
    return cheval(23, g6, t) * TWOBPI


def IL0(x):
    XLOW = 1.11022303e-16
    XHIGH = 1.8981253e9
    if x < 0.0:
        return 0.0
    elif x < XLOW:
        return 1.0
    elif x <= 16.0:
        return diff0_small(x)
    elif x > XHIGH:
        return TWOBPI / x
    else:
        return diff0_large(x)


def IL1(x):
    XLOW = 2.22044605e-16
    XHIGH = 1.8981253e9
    if x < 0.0:
        return float('nan')
    elif x < XLOW:
        return x / 2.0
    elif x <= 16.0:
        return diff1_small(x)
    elif x > XHIGH:
        return TWOBPI
    else:
        return diff1_large(x)


def AL(z):
    return 2 * (IL0(z) - (IL1(z) / z))


def AB(z):
    return IL1(2 * z) / z


def cheval(N, A, T):
    """
    This function evaluates a Chebyshev series, using the
    Clenshaw method with Reinsch modification, as analysed
    in the paper by Oliver.

    REFERENCES
         "An error analysis of the modified Clenshaw method for
          evaluating Chebyshev and Fourier series" J. Oliver,
          J.I.M.A., vol. 20, 1977, pp379-391

      AUTHOR:  Dr. Allan J. MacLeod,
               Dept. of Mathematics and Statistics,
               University of Paisley ,
               High St.,
               PAISLEY,
              SCOTLAND

     LATEST MODIFICATION:   21 December , 1992

    Parameters
    ----------
    N : INTEGER - The no. of terms in the sequence
    A : FLOAT LIST, dimension 0 to N - The coefficients of
        the Chebyshev series
    T : FLOAT - The value at which the series is to be
        evaluated

    Returns
    -------
    The value of the chebyshev polynomial.

    """
    ZERO = 0.0
    HALF = 0.5
    TWO = 2.0
    TEST = 0.6

    U0 = ZERO
    U1 = ZERO
    U2 = ZERO
    D2 = ZERO

    # If ABS ( T )  < 0.6 use the standard Clenshaw method
    if abs(T) < TEST:
        TT = T + T
        for i in range(N - 1, 0 - 1, -1):  # the 0 -1 is there to make the end point >=0
            U2 = U1
            U1 = U0
            U0 = TT * U1 + A[i] - U2
        l_cheval = (U0 - U2) / TWO
    else:  # If ABS ( T )  > =  0.6 use the Reinsch modification
        D1 = ZERO

        # T > =  0.6 code
        if T > ZERO:
            TT = (T - HALF) - HALF
            TT = TT + TT
            for i in range(N - 1, 0 - 1, -1):  # the 0 -1 is there to make the end point >=0
                D2 = D1
                U2 = U1
                D1 = TT * U2 + A[i] + D2
                U1 = D1 + U2
            l_cheval = (D1 + D2) / TWO
        else:  # T < =  -0.6 code
            TT = (T + HALF) + HALF
            TT = TT + TT
            for i in range(N - 1, 0 - 1, -1):  # the 0 -1 is there to make the end point >=0
                D2 = D1
                U2 = U1
                D1 = TT * U2 + A[i] - D2
                U1 = D1 - U2
            l_cheval = (D1 - D2) / TWO

    return l_cheval


class PVCT:
    # http://ftp.esrf.fr/pub/scisoft/xop2.3/DabaxFiles/ --> all the neutral atoms
    sfacb = (
        (0.413048, 0.294953, 0.187491, 0.080701, 0.023736, 0.000049, 15.569946, 32.398468, 5.711404, 61.889874, 1.334118),
        (0.493002, 0.322912, 0.140191, 0.040810, 0, 0.003038, 10.5109, 26.1257, 3.14236, 57.7997, 0),
        (0.732354, 0.753896, 0.283819, 0.190003, 0.039139, 0.000487, 11.553918, 4.595831, 1.546299, 26.463964, 0.377523),
        (0.974637, 0.158472, 0.811855, 0.262416, 0.790108, 0.002542, 4.334946, 0.342451, 97.102966, 201.363831, 1.409234),
        (1.533712, 0.638283, 0.601052, 0.106139, 1.118414, 0.002511, 42.662079, 0.595420, 99.106499, 0.151340, 1.843093),
        (2.085185, 1.064580, 1.062788, 0.140515, 0.641784, 0.003823, 23.494068, 1.137894, 61.238976, 0.114886, 0.399036),
        (2.657506, 1.078079, 1.490909, -4.241070, 0.713791, 4.297983, 14.780758, 0.776775, 42.086842, -0.000294, 0.239535),
        (11.893780, 3.277479, 1.858092, 0.858927, 0.912985, -11.804902, 0.000158, 10.232723, 30.344690, 0.656065, 0.217287),
        (2.960427, 2.508818, 0.637853, 0.722838, 1.142756, 0.027014, 14.182259, 5.936858, 0.112726, 34.958481, 0.390240),
        (3.511943, 2.772244, 0.678385, 0.915159, 1.089261, 0.032557, 10.687859, 4.380466, 0.093982, 27.255203, 0.313066),
        (4.183749, 2.905726, 0.520513, 1.135641, 1.228065, 0.025576, 8.175457, 3.252536, 0.063295, 21.813910, 0.224952),
        (4.910127, 3.081783, 1.262067, 1.098938, 0.560991, 0.079712, 3.281434, 9.119178, 0.102763, 132.013947, 0.405878),
        (4.708971, 1.194814, 1.558157, 1.170413, 3.239403, 0.126842, 4.875207, 108.506081, 0.111516, 48.292408, 1.928171),
        (4.730796, 2.313951, 1.541980, 1.117564, 3.154754, 0.139509, 3.628931, 43.051167, 0.095960, 108.932388, 1.555918),
        (5.275329, 3.191038, 1.511514, 1.356849, 2.519114, 0.145073, 2.631338, 33.730728, 0.081119, 86.288643, 1.170087),
        (1.950541, 4.146930, 1.494560, 1.522042, 5.729711, 0.155233, 0.908139, 27.044952, 0.071280, 67.520187, 1.981173),
        (6.372157, 5.154568, 1.473732, 1.635073, 1.209372, 0.154722, 1.514347, 22.092527, 0.061373, 55.445175, 0.646925),
        (1.446071, 6.870609, 6.151801, 1.750347, 0.634168, 0.146773, 0.052357, 1.193165, 18.343416, 46.398396, 0.401005),
        (7.188004, 6.638454, 0.454180, 1.929593, 1.523654, 0.265954, 0.956221, 15.339877, 15.339862, 39.043823, 0.062409),
        (8.163991, 7.146945, 1.070140, 0.877316, 1.486434, 0.253614, 12.816323, 0.808945, 210.327011, 39.597652, 0.052821),
        (8.593655, 1.477324, 1.436254, 1.182839, 7.113258, 0.196255, 10.460644, 0.041891, 81.390381, 169.847839, 0.688098),
        (1.476566, 1.487278, 1.600187, 9.177463, 7.099750, 0.157765, 53.131023, 0.035325, 137.319489, 9.098031, 0.602102),
        (9.818524, 1.522646, 1.703101, 1.768774, 7.082555, 0.102473, 8.001879, 0.029763, 39.885422, 120.157997, 0.532405),
        (10.473575, 1.547881, 1.986381, 1.865616, 7.056250, 0.067744, 7.081940, 0.026040, 31.909672, 108.022842, 0.474882),
        (11.007069, 1.555477, 2.985293, 1.347855, 7.034779, 0.065510, 6.366281, 0.023987, 23.244839, 105.774498, 0.429369),
        (11.709542, 1.733414, 2.673141, 2.023368, 7.003180, -0.147293, 5.597120, 0.017800, 21.788420, 89.517914, 0.383054),
        (12.311098, 1.876623, 3.066177, 2.070451, 6.975185, -0.304931, 5.009415, 0.014461, 18.743040, 82.767876, 0.346506),
        (12.914510, 2.481908, 3.466894, 2.106351, 6.960892, -0.936572, 4.507138, 0.009126, 16.438129, 76.987320, 0.314418),
        (13.521865, 6.947285, 3.866028, 2.135900, 4.284731, -2.762697, 4.077277, 0.286763, 14.622634, 71.966080, 0.004437),
        (14.014192, 4.784577, 5.056806, 1.457971, 6.932996, -3.254477, 3.738280, 0.003744, 13.034982, 72.554794, 0.265666),
        (14.741002, 6.907748, 4.642337, 2.191766, 38.424042, -36.915829, 3.388232, 0.243315, 11.903689, 63.312130, 0.000397),
        (15.758946, 6.841123, 4.121016, 2.714681, 2.395246, -0.847395, 3.121754, 0.226057, 12.482196, 66.203621, 0.007238),
        (16.540613, 1.567900, 3.727829, 3.345098, 6.785079, 0.018726, 2.866618, 0.012198, 13.432163, 58.866047, 0.210974),
        (17.025642, 4.503441, 3.715904, 3.937200, 6.790175, -2.984117, 2.597739, 0.003012, 14.272119, 50.437996, 0.193015),
        (17.354071, 4.653248, 4.259489, 4.136455, 6.749163, -3.160982, 2.349787, 0.002550, 15.579460, 45.181202, 0.177432),
        (17.550570, 5.411882, 3.937180, 3.880645, 6.707793, -2.492088, 2.119226, 16.557184, 0.002481, 42.164009, 0.162121),
        (17.655279, 6.848105, 4.171004, 3.446760, 6.685200, -2.810592, 1.908231, 16.606236, 0.001598, 39.917473, 0.146896),
        (8.123134, 2.138042, 6.761702, 1.156051, 17.679546, 1.139548, 15.142385, 33.542667, 0.129372, 224.132507, 1.713368),
        (17.730219, 9.795867, 6.099763, 2.620025, 0.600053, 1.140251, 1.563060, 14.310868, 0.120574, 135.771317, 0.120574),
        (17.792040, 10.253252, 5.714949, 3.170516, 0.918251, 1.131787, 1.429691, 13.132816, 0.112173, 108.197029, 0.112173),
        (17.859772, 10.911038, 5.821115, 3.512513, 0.746965, 1.124859, 1.310692, 12.319285, 0.104353, 91.777542, 0.104353),
        (17.958399, 12.063054, 5.007015, 3.287667, 1.531019, 1.123452, 1.211590, 12.246687, 0.098615, 75.011948, 0.098615),
        (6.236218, 17.987711, 12.973127, 3.451426, 0.210899, 1.108770, 0.090780, 1.108310, 11.468720, 66.684151, 0.090780),
        (17.840963, 3.428236, 1.373012, 12.947364, 6.335469, 1.074784, 1.005729, 41.901382, 119.320541, 9.781542, 0.083391),
        (6.271624, 17.906738, 14.123269, 3.746008, 0.908235, 1.043992, 0.077040, 0.928222, 9.555345, 35.860680, 123.552246),
        (6.216648, 17.919739, 3.854252, 0.840326, 15.173498, 0.995452, 0.070789, 0.856121, 33.889484, 121.686691, 9.029517),
        (6.121511, 4.784063, 16.631683, 4.318258, 13.246773, 0.883099, 0.062549, 0.784031, 8.751391, 34.489983, 0.784031),
        (6.073874, 17.155437, 4.173344, 0.852238, 17.988686, 0.756603, 0.055333, 7.896512, 28.443739, 110.376106, 0.716809),
        (6.080986, 18.019468, 4.018197, 1.303510, 17.974669, 0.603504, 0.048990, 7.273646, 29.119284, 95.831207, 0.661231),
        (6.196477, 18.816183, 4.050479, 1.638929, 17.962912, 0.333097, 0.042072, 6.695665, 31.009790, 103.284348, 0.610714),
        (19.325171, 6.281571, 4.498866, 1.856934, 17.917318, 0.119024, 6.118104, 0.036915, 32.529045, 95.037186, 0.565651),
        (5.394956, 6.549570, 19.650681, 1.827820, 17.867832, -0.290506, 33.326523, 0.030974, 5.564929, 87.130966, 0.523992),
        (6.660302, 6.940756, 19.847015, 1.557175, 17.802427, -0.806668, 33.031654, 0.025750, 5.065547, 84.101616, 0.487660),
        (19.884502, 6.736593, 8.110516, 1.170953, 17.548716, -0.448811, 4.628591, 0.027754, 31.849096, 84.406387, 0.463550),
        (19.978920, 11.774945, 9.332182, 1.244749, 17.737501, -6.065902, 4.143356, 0.010142, 28.796200, 75.280685, 0.413616),
        (17.418674, 8.314444, 10.323193, 1.383834, 19.876251, -2.322802, 0.399828, 0.016872, 25.605827, 233.339676, 3.826915),
        (19.747343, 17.368477, 10.465718, 2.592602, 11.003653, -5.183497, 3.481823, 0.371224, 21.226641, 173.834274, 0.010719),
        (19.966019, 27.329655, 11.018425, 3.086696, 17.335455, -21.745489, 3.197408, 0.003446, 19.955492, 141.381973, 0.341817),
        (17.355122, 43.988499, 20.546650, 3.130670, 11.353665, -38.386017, 0.328369, 0.002047, 3.088196, 134.907654, 18.832960),
        (21.551311, 17.161730, 11.903859, 2.679103, 9.564197, -3.871068, 2.995675, 0.312491, 17.716705, 152.192825, 0.010468),
        (17.331244, 62.783924, 12.160097, 2.663483, 22.239950, -57.189842, 0.300269, 0.001320, 17.026001, 148.748993, 2.910268),
        (17.286388, 51.560162, 12.478557, 2.675515, 22.960947, -45.973682, 0.286620, 0.001550, 16.223755, 143.984512, 2.796480),
        (23.700363, 23.072214, 12.777782, 2.684217, 17.204367, -17.452166, 2.689539, 0.003491, 15.495437, 139.862473, 0.274536),
        (17.186195, 37.156837, 13.103387, 2.707246, 24.419271, -31.586687, 0.261678, 0.001995, 14.787360, 134.816299, 2.581883),
        (24.898117, 17.104952, 13.222581, 3.266152, 48.995213, -43.505684, 2.435028, 0.246961, 13.996325, 110.863091, 0.001383),
        (25.910013, 32.344139, 13.765117, 2.751404, 17.064405, -26.851971, 2.373912, 0.002034, 13.481969, 125.836510, 0.236916),
        (26.671785, 88.687576, 14.065445, 2.768497, 17.067781, -83.279831, 2.282593, 0.000665, 12.920230, 121.937187, 0.225531),
        (27.150190, 16.999819, 14.059334, 3.386979, 46.546471, -41.165253, 2.169660, 0.215414, 12.213148, 100.506783, 0.001211),
        (28.174887, 82.493271, 14.624002, 2.802756, 17.018515, -77.135223, 2.120995, 0.000640, 11.915256, 114.529938, 0.207519),
        (28.925894, 76.173798, 14.904704, 2.814812, 16.998117, -70.839813, 2.046203, 0.000656, 11.465375, 111.411980, 0.199376),
        (29.676760, 65.624069, 15.160854, 2.830288, 16.997850, -60.313812, 1.977630, 0.000720, 11.044622, 108.139153, 0.192110),
        (30.122866, 15.099346, 56.314899, 3.540980, 16.943729, -51.049416, 1.883090, 10.342764, 0.000780, 89.559250, 0.183849),
        (30.617033, 15.145351, 54.933548, 4.096253, 16.896156, -49.719837, 1.795613, 9.934469, 0.000739, 76.189705, 0.175914),
        (31.066359, 15.341823, 49.278297, 4.577665, 16.828321, -44.119026, 1.708732, 9.618455, 0.000760, 66.346199, 0.168002),
        (31.507900, 15.682498, 37.960129, 4.885509, 16.792112, -32.864574, 1.629485, 9.446448, 0.000898, 59.980675, 0.160798),
        (31.888456, 16.117104, 42.390297, 5.211669, 16.767591, -37.412682, 1.549238, 9.233474, 0.000689, 54.516373, 0.152815),
        (32.210297, 16.678440, 48.559906, 5.455839, 16.735533, -43.677956, 1.473531, 9.049695, 0.000519, 50.210201, 0.145771),
        (32.004436, 1.975454, 17.070105, 15.939454, 5.990003, 4.018893, 1.353767, 81.014175, 0.128093, 7.661196, 26.659403),
        (31.273891, 18.445440, 17.063745, 5.555933, 1.575270, 4.050394, 1.316992, 8.797154, 0.124741, 40.177994, 1.316997),
        (16.777390, 19.317156, 32.979683, 5.595453, 10.576854, -6.279078, 0.122737, 8.621570, 1.256902, 38.008820, 0.000601),
        (16.839890, 20.023823, 28.428564, 5.881564, 4.714706, 4.076478, 0.115905, 8.256927, 1.195250, 39.247227, 1.195250),
        (16.630795, 19.386616, 32.808571, 1.747191, 6.356862, 4.066939, 0.110704, 7.181401, 1.119730, 90.660263, 26.014978),
        (16.419567, 32.738590, 6.530247, 2.342742, 19.916475, 4.049824, 0.105499, 1.055049, 25.025890, 80.906593, 6.664449),
        (16.282274, 32.725136, 6.678302, 2.694750, 20.576559, 4.040914, 0.101180, 1.002287, 25.714146, 77.057549, 6.291882),
        (16.289164, 32.807171, 21.095163, 2.505901, 7.254589, 4.046556, 0.098121, 0.966265, 6.046622, 76.598068, 28.096128),
        (16.011461, 32.615547, 8.113899, 2.884082, 21.377867, 3.995684, 0.092639, 0.904416, 26.543257, 68.372963, 5.499512),
        (16.070229, 32.641106, 21.489658, 2.299218, 9.480184, 4.020977, 0.090437, 0.876409, 5.239687, 69.188477, 27.632641),
        (16.007385, 32.663830, 21.594351, 1.598497, 11.121192, 4.003472, 0.087031, 0.840187, 4.954467, 199.805801, 26.905106),
        (32.563690, 21.396671, 11.298093, 2.834688, 15.914965, 3.981773, 0.801980, 4.590666, 22.758972, 160.404388, 0.083544),
        (15.914053, 32.535042, 21.553976, 11.433394, 3.612409, 3.939212, 0.080511, 0.770669, 4.352206, 21.381622, 130.500748),
        (15.784024, 32.454899, 21.849222, 4.239077, 11.736191, 3.922533, 0.077067, 0.735137, 4.097976, 109.464111, 20.512138),
        (32.740208, 21.973675, 12.957398, 3.683832, 15.744058, 3.886066, 0.709545, 4.050881, 19.231543, 117.255005, 0.074040),
        (15.679275, 32.824306, 13.660459, 3.687261, 22.279434, 3.854444, 0.071206, 0.681177, 18.236156, 112.500038, 3.930325),
        (32.999901, 22.638077, 14.219973, 3.672950, 15.683245, 3.769391, 0.657086, 3.854918, 17.435474, 109.464485, 0.068033),
        (33.281178, 23.148544, 15.153755, 3.031492, 15.704215, 3.664200, 0.634999, 3.856168, 16.849735, 121.292038, 0.064857),
        (33.435162, 23.657259, 15.576339, 3.027023, 15.746100, 3.541160, 0.612785, 3.792942, 16.195778, 117.757004, 0.061755),
        (15.804837, 33.480801, 24.150198, 3.655563, 15.499866, 3.390840, 0.058619, 0.590160, 3.674720, 100.736191, 15.408296),
        (15.889072, 33.625286, 24.710381, 3.707139, 15.839268, 3.213169, 0.055503, 0.569571, 3.615472, 97.694786, 14.754303),
        (33.794075, 25.467693, 16.048487, 3.657525, 16.008982, 3.005326, 0.550447, 3.581973, 14.357388, 96.064972, 0.052450)
    )

    # corresponds to the row number in the sf array
    atomicNumber = {
        "D": 0, "H": 1, "He": 2, "Li": 3, "Be": 4,
        "B": 5, "C": 6, "N": 7, "O": 8, "F": 9,
        "Ne": 10, "Na": 11, "Mg": 12, "Al": 13, "Si": 14,
        "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19,
        "Ca": 20, "Sc": 21, "Ti": 22, "V": 23, "Cr": 24,
        "Mn": 25, "Fe": 26, "Co": 27, "Ni": 28, "Cu": 29,
        "Zn": 30, "Ga": 31, "Ge": 32, "As": 33, "Se": 34,
        "Br": 35, "Kr": 36, "Rb": 37, "Sr": 38, "Y": 39,
        "Zr": 40, "Nb": 41, "Mo": 42, "Tc": 43, "Ru": 44,
        "Rh": 45, "Pd": 46, "Ag": 47, "Cd": 48, "In": 49,
        "Sn": 50, "Sb": 51, "Te": 52, "I": 53, "Xe": 54,
        "Cs": 55, "Ba": 56, "La": 57, "Ce": 58, "Pr": 59,
        "Nd": 60, "Pm": 61, "Sm": 62, "Eu": 63, "Gd": 64,
        "Tb": 65, "Dy": 66, "Ho": 67, "Er": 68, "Tm": 69,
        "Yb": 70, "Lu": 71, "Hf": 72, "Ta": 73, "W": 74,
        "Re": 75, "Os": 76, "Ir": 77, "Pt": 78, "Au": 79,
        "Hg": 80, "Tl": 81, "Pb": 82, "Bi": 83, "Po": 84,
        "At": 85, "Rn": 86, "Fr": 87, "Ra": 88, "Ac": 89,
        "Th": 90, "Pa": 91, "U": 92, "Np": 93, "Pu": 94,
        "Am": 95, "Cm": 96, "Bk": 97, "Cf": 98}

    def __init__(self, lam=1.5406,
                 mono=0,
                 B=1,
                 muR=0,
                 formula="Fe 1",
                 min_angle=10,
                 max_angle=145):
        """
        x

        Parameters
        ----------
        lam : float, optional
            X-ray wavelength in angstrom or keV. if >4, assume its keV, otherwise angstrom. The default is 1.5406.
        formula : String, optional
            representing the chemical formula of the material belonging to the diffraction patterns
            eg "Ca 1 C 1 O 3". The default is "Fe".
        muR : float, optional
            if muR is >5, assume it is a flat plate and muR == omega, otherwise, absorption. The default is 1.
        B : float, optional
            Overal isotropic thermal factor. The default is 1.
        mono : float, optional
            monochromator angle in deg2Th. The default is 0.
        min_angle : float, optional
            angle of the first peak angle in deg2Th. The default is 10.
        max_angle : float, optional
            highest angle to use in the calculation in deg2Th. The default is 145.

        Returns
        -------
        None.

        """
        if lam > 4:
            self.lam = lam / 12.39837457
        else:
            self.lam = lam

        self.formula = formula
        self.muR = muR
        self.B = B
        self.mono = mono
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.isFlatPlate = self.muR >= 5.0  # more than 5 == flat plate

        # these are here so they're here from the start
        self.D = None
        self.filenames = None
        self.pvct = None  # This will be the final pVCT DiffractionPattern
        self.pvct_sum = None  # Ths will be the sum DiffractionPattern before averaging
        self.s_array = None
        self.angle_array = None
        self.summary = None
        self.patterns = []

    def simulate(self, D=10):
        """
        Do a simulation of a pVCT experiment with a certain number of datasets
        The min and max angles are taken from the object initialisation

        Parameters
        ----------
        D : int, optional
            Number of diffraction patterns to simulate. The default is 10.

        Returns
        -------
        None.

        """
        self.D = D
        stop = self.max_angle
        start = self.min_angle
        step = 0.05
        nstps = int(((stop - start) / step) + 1)

        self.s_array = [0] * nstps
        self.angle_array = [0.0] * nstps
        self.summary = [[None] * 8] * nstps

        for i in range(nstps):
            self.angle_array[i] = start + i * step

    def read_filenames(self, filenames):
        """
        set the filenames from which I'm going to read the diffraction patterns

        Parameters
        ----------
        filenames : list
            strings containing the filenames.

        Returns
        -------
        None.

        """
        self.filenames = filenames[:]
        self.D = len(filenames)

        for name in filenames:
            # print(f"Now reading {name}.")
            pattern = du.DiffractionPattern(name)
            self.patterns.append(pattern)

        if self.min_angle < self.patterns[0].getMinAngle() or self.min_angle == -1:
            self.min_angle = self.patterns[0].getMinAngle()

        if self.max_angle < self.patterns[0].getMaxAngle() or self.max_angle == -1:
            self.max_angle = self.patterns[0].getMaxAngle()

        nstps = self.patterns[0].getNumOfDataPoints()

        self.s_array = [0] * nstps
        self.angle_array = self.patterns[0].getAngles()
        self.summary = [[None] * 8] * nstps


    def calc_sum_array(self, writeSummary=True):
        """
        Calculates the number of diffpats to add together at each angle

        Parameters
        ----------
        writeSummary : boolean, optional
            Do you want to write the summary information to file?. The default is True.

        Returns
        -------
        None.

        """
        print("Calculating sum array...")
        f = 1.0 / self.D  # fraction of datasets to use as a constant too all angles - Ian uses f = 0.1 for his stuff
        Dmin = int(round(max(1, f * self.D)))
        Dmax = self.D - Dmin

        # Pmax is value of P at the minAngle
        Pmax = self.temperatureFactor(self.min_angle) * \
               self.LPFactor(self.min_angle) * \
               self.averageScatteringFactorSquared(self.min_angle) * \
               self.absorption(self.min_angle)

        # Pmin is the minimum value of P, that is less than maxAngle
        Pmin = sys.float_info.max

        for i in range(len(self.s_array)):
            angle = self.angle_array[i]

            if angle < self.min_angle:
                continue

            tmp = self.temperatureFactor(angle) * \
                  self.LPFactor(angle) * \
                  self.averageScatteringFactorSquared(angle) * \
                  self.absorption(angle)

            if tmp < Pmin and angle < self.max_angle:
                Pmin = tmp

        if writeSummary:
            print("Writing summary.txt.")
            f = open("summary.txt", "w")
            f.write("Pmax\tPmin\tDmax\tDmin\n")
            f.write("{:.{dps}f}\t".format(Pmax, dps=5))
            f.write("{:.{dps}f}\t".format(Pmin, dps=5))
            f.write("{:.{dps}f}\t".format(Dmax, dps=5))
            f.write("{:.{dps}f}\n\n".format(Dmin, dps=5))

            f.write("angle\tSFsq\tLP\tTF\tA\tP\tPstar\tS\n")

        for i in range(len(self.s_array)):
            if i % 20 == 0:
                print(f"{i} of {len(self.s_array)}", end="\r", flush=True)

            angle = self.angle_array[i]

            TF = self.temperatureFactor(angle)
            LP = self.LPFactor(angle)
            SFsq = self.averageScatteringFactorSquared(angle)
            A = self.absorption(angle)

            P = SFsq * LP * TF * A
            try:
                Pstar = ((Pmax / P) - 1) / ((Pmax / Pmin) - 1)
            except ZeroDivisionError:
                Pstar = float('inf')

            S = max(0, Pstar * Dmax) + Dmin

            if math.isinf(S) or (self.isFlatPlate and angle < self.muR + 0.5):  # for angles below the fib angle + 0.5 deg
                S = 1.0

            if angle < self.max_angle:  # then update the S_maxangle value
                S_maxAngle = S
            else:  # you're past the max angle, and you want to keep the last calculated value of S.
                S = S_maxAngle

            self.s_array[i] = round(S)

            #  for somereason, this only gives me multiple copies of the last entry....
            if writeSummary:
                f.write("{:.{dps}f}\t".format(angle, dps=5))
                f.write("{:.{dps}f}\t".format(SFsq, dps=5))
                f.write("{:.{dps}f}\t".format(LP, dps=5))
                f.write("{:.{dps}f}\t".format(TF, dps=5))
                f.write("{:.{dps}f}\t".format(A, dps=5))
                f.write("{:.{dps}f}\t".format(P, dps=5))
                f.write("{:.{dps}f}\t".format(Pstar, dps=7))
                f.write("{:.{dps}f}\n".format(self.s_array[i], dps=0))

        if writeSummary:
            f.close()


    def combine_files(self):
        print("Trimming files...")
        for i in range(len(self.patterns)):
            print(f"{i} of {len(self.patterns)}", end="\r", flush=True)
            j = i + 1
            min_cutoff_index, max_cutoff_index = first_last_index(self.s_array, j)
            min_cutoff_angle = self.angle_array[min_cutoff_index]
            max_cutoff_angle = self.angle_array[max_cutoff_index]
            self.patterns[i].trim(min_cutoff_angle, max_cutoff_angle)

        print("Adding up patterns...")
        self.pvct_sum = copy.deepcopy(self.patterns[0])
        for i in range(1, len(self.patterns)):
            print(f"{i} of {len(self.patterns)}", end="\r", flush=True)
            self.pvct_sum += self.patterns[i]  # += --> in-place sum much quicker than +

        # dividing sum by number that were summed
        print("Averaging pVCT pattern.")
        self.pvct = copy.deepcopy(self.pvct_sum)
        for i in range(len(self.s_array)):
            self.pvct.diffpat[i] /= self.s_array[i]  # /= in-place divide is faster than /

    def writeToFile(self, dp_angle=5, dp_intensity=3, dp_error=3):
        file = removeExtension(self.filenames[0]) + "_pvct.xye"
        # print(f"Writing to {file}")
        self.pvct.writeToFile(file, dp_angle, dp_intensity, dp_error)

    def writeSumToFile(self, dp_angle=5, dp_intensity=3, dp_error=3):
        file = removeExtension(self.filenames[0]) + "_pvct_sum.xye"
        # print(f"Writing sum to {file}")
        self.pvct_sum.writeToFile(file, dp_angle, dp_intensity, dp_error)

    # angle is in 2Th deg
    def temperatureFactor(self, angle):
        """
        find the value of the effect of the temperature factor on the scattering power
        math.exp(-2.0 * self.B * sin * sin)
        sin = math.sin(math.radians(angle/2))/self.lam

        Parameters
        ----------
        angle : Diffraction angle in deg 2Th.

        Returns
        -------
        float
            The valu.

        """
        sin = math.sin(math.radians(angle / 2)) / self.lam
        return math.exp(-2.0 * self.B * sin * sin)

    # angle and mono are in 2Th deg
    def LPFactor(self, angle):
        """
        Find the magnitude of the LP factor at an angle

        Parameters
        ----------
        angle : diffraction angle in deg 2Th

        Returns
        -------
        float
            DESCRIPTION.

        """
        ang = math.radians(angle)
        mon = math.radians(self.mono)

        return (1 + math.pow(math.cos(mon) * math.cos(ang), 2)) / (2 * math.cos(ang / 2) * math.pow(math.sin(ang / 2), 2))

    # angle is in 2Th deg
    def scatteringFactor(self, element, angle):
        """
        find the magnitude of the scattering factor at a given angle

        Parameters
        ----------
        element : String. Element symbol
        angle : float. Diffraction angle in deg 2Th

        Returns
        -------
        float
            DESCRIPTION.

        """
        sin2 = math.pow(math.sin(math.radians(angle / 2)) / self.lam, 2)
        ele = PVCT.atomicNumber[element]
        f = 0.0

        for i in range(5):
            a = PVCT.sfacb[ele][i]
            b = PVCT.sfacb[ele][i + 6]
            f += a * math.exp(-1.0 * b * sin2)

        f += PVCT.sfacb[ele][5]

        return f

    def scatteringFactorSquared(self, element, angle):
        """ Returns the square of the scattering factor"""
        return self.scatteringFactor(element, angle) ** 2

    # calculate an average scattering factor from a chemical formula:
    #  must be of the sort "Fe 2 O 3", or "Ca 1 C 1 O 3"
    def averageScatteringFactor(self, angle):
        """
        Given the chemical formula, what is the average scattering factor of
        all the elements, at a given angle

        Parameters
        ----------
        angle : float. diffraction angle in deg 2Th

        Returns
        -------
        float
            DESCRIPTION.

        """
        atoms = group(self.formula.split(" "), 2)
        f = 0.0  # scattering factor
        n = 0.0  # number of atoms in formula

        for atom in atoms:
            element = atom[0]
            mols = float(atom[1])
            f += self.scatteringFactor(element, angle) * mols
            n += mols

        f /= n
        return f

    def averageScatteringFactorSquared(self, angle):
        """Square of the average scattering factor"""
        return self.averageScatteringFactor(angle) ** 2

    def capillaryAbsorption(self, angle):
        """
        What is the effect of capillary absorption ate a given angle

        Parameters
        ----------\
        angle : float diffraction angle in deg 2 Th

        Returns
        -------
        float.

        """
        if self.muR < 0.001:
            return 1.0

        ang = math.radians(angle / 2)
        z = 2 * self.muR
        return AL(z) * math.cos(ang) * math.cos(ang) + AB(z) * math.sin(ang) * math.sin(ang)

    def flatPlateAbsorption(self, angle):
        """
        What is the effect of fixed-incident beame, flat plate absorption with angle?

        Parameters
        ----------
        angle : float
            deg 2 Th.

        Returns
        -------
        float.

        """
        omega = self.muR

        if angle <= omega:
            return 0.0

        ang = math.radians(angle)
        ome = math.radians(omega)
        return 2 / (1 + (math.sin(ome) / math.sin(ang - ome)))

    def absorption(self, angle):
        """
        Decide if a value is a flat plate or capillary absorption, and return the correct interpretation


        Parameters
        ----------
        angle : float. A diffration angle in deg 2Th\

        Returns
        -------
        float

        """
        if self.isFlatPlate:
            return self.flatPlateAbsorption(angle)
        else:
            return self.capillaryAbsorption(angle)
