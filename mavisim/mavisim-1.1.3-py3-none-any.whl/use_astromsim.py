from mavisim import AstromCalibSim
from astropy.io import ascii
import matplotlib.pyplot as plt; plt.ion()
import numpy as np

# input true distortion field:
static_distort =  ascii.read("/Users/jcranney/mavis-astrosim/StaticDistortTransmissive")

# create the astrometry simulator object:
astrom_sim = AstromCalibSim(
    static_distort,           # astropy parsed input file with appropriate headers
    centroid_noise_std=10e-6, # centroiding noise in arcsec.
    hole_position_std=1e-2,   # manufacturing tolerance in mm.
    dx=0.2, dy=0.2,           # Shift applied to mask for differential method.
    n_poly=6)                 # max order of polynomial to fit with.

# Values to evaluate distortion functions with. Can be any arangement of 
# coordinates within the science field.
nsamp = 51
xx,yy = np.meshgrid(np.linspace(-15,15,nsamp),np.linspace(-15,15,nsamp))
xx = xx.flatten()
yy = yy.flatten()
rr = (xx**2+yy**2)**0.5
# use slightly smaller field because distortions arent defined beyond 30"x30" box
xx = xx[rr<=14.5]
yy = yy[rr<=14.5]

# interpolate input distortions at xx/yy coordinates
input_dist_xx,input_dist_yy = astrom_sim.input_dist(xx,yy)

# interpolate recovered distortions at xx/yy coordinates
recovered_dist_xx,recovered_dist_yy = astrom_sim.recovered_dist(xx,yy)

# interpolate residual distortions at xx/yy coordinates
residual_dist_xx,residual_dist_yy = astrom_sim.residual_dist(xx,yy)
# remove tt from residual since it doesn't affect the science
residual_dist_xx -= residual_dist_xx.mean()
residual_dist_yy -= residual_dist_yy.mean()

plt.figure(figsize=[8,8])
arrow_sf = 40
for i in range(xx.shape[0]):
    plt.arrow(xx[i],yy[i],arrow_sf*input_dist_xx[i],arrow_sf*input_dist_yy[i],
            color="r",head_width=0.05,width=0.01,length_includes_head=True)
    plt.arrow(xx[i],yy[i],arrow_sf*recovered_dist_xx[i],arrow_sf*recovered_dist_yy[i],
            color="b",head_width=0.05,width=0.01,length_includes_head=True)
    plt.axis("square")
plt.legend(["true distortion","fitted distortion"])

plt.figure(figsize=[8,8])
arrow_sf = 10000
for i in range(xx.shape[0]):
    plt.arrow(xx[i],yy[i],arrow_sf*residual_dist_xx[i],arrow_sf*residual_dist_yy[i],
            color="g",head_width=0.05,width=0.01,length_includes_head=True)
    plt.axis("square")
plt.legend(["residual distortion"])
plt.title(f"RMS Residual Distortion: {(residual_dist_xx.std()**2+residual_dist_yy.std()**2)**0.5*1e6:0.3f} uas")