from astropy.io import fits
import subprocess
import time
import os
import warnings


def solveField(hdul,RA,DEC,radius=2,cmdstring="--no-plots --downsample 4  --scale-units degwidth --scale-low 0.4 --scale-high 0.6 --crpix-center"):
    dn = os.path.dirname(os.path.realpath(__file__))
    tempfits = os.path.join(dn,'tmp/temp.fits')
    wcsfits  = os.path.join(dn,'tmp/wcsfits.fits')
    solvedfile = os.path.join(dn,'tmp/temp.solved')
    hdul.writeto(str(tempfits),overwrite=True)
    cmds = f'solve-field {tempfits} --overwrite --new-fits {wcsfits} --ra {RA} --dec {DEC} --radius {radius}'
    cmds = cmds.split()
    cmds += cmdstring.split()

    start = time.time()
    process = subprocess.Popen(cmds)
    stdout, stderr = process.communicate()
    end = time.time()

    if os.path.exists(solvedfile):
        #print(f'solved field in {round(end-start,2)} seconds!')
        newheader = fits.getheader(wcsfits)
        return newheader
    else:
        warnings.warn("Warning: Field did not solve.")
        return None




    