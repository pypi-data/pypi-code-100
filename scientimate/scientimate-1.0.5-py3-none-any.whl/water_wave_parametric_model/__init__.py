"""
.. ++++++++++++++++++++++++++++++++YA LATIF++++++++++++++++++++++++++++++++++
.. +                                                                        +
.. + ScientiMate                                                            +
.. + Earth-Science Data Analysis Library                                    +
.. +                                                                        +
.. + Developed by: Arash Karimpour                                          +
.. + Contact     : www.arashkarimpour.com                                   +
.. + Developed/Updated (yyyy-mm-dd): 2020-08-01                             +
.. +                                                                        +
.. ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

#----------------------------------------------------------
#Import subdirectory modules
#It uses for module base import such as:
#import scientimate as sm
#from scientimate import plotting
#sm.plotting.plot2d(x,y,'line_confid','blue_red','large')
#----------------------------------------------------------

#Water Wave Parametric Model
#---------------------------
# from .asymptlimit import asymptlimit
# from .equivfetchdeep import equivfetchdeep
# from .equivfetchshallow import equivfetchshallow
# from .fullydevwave import fullydevwave
# from .mindurationdeep import mindurationdeep
# from .mindurationshallow import mindurationshallow
from .parametricwavedeep import parametricwavedeep
from .parametricwaveshallow import parametricwaveshallow
# from .wavedim2dimless import wavedim2dimless
# from .wavedimless2dim import wavedimless2dim
