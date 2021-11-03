from astropy.io import ascii

# Static Distortion
static_distort =  ascii.read("Dist_grid2_ZPL_01_rot0.txt")                # Static distortion map reflecting the contribution of the MAVIS optics
plate_scale =  1.29                                                      # arcsec/mm, to convert location in mm to arcseconds
dynamic_amp = 1                                                          # NOT IN USE, amplification factor to increase the distortion
