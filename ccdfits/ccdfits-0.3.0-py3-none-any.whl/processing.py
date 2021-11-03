from ccdfits import FITS, maskedFITS
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import warnings

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class UnknownCCDError(Error):
    """Exception raised when the attributes of a .fits image
    do not match any of the listed CCDs.
    """

    def __init__(self, ccdprops_dict):
        print('No CCD found with the following properties:')
        print(ccdprops_dict)

r2pi = np.sqrt(2*np.pi)

class CCD:
    """Class with the properties of a CCD."""

    def __init__(self, ccdprops_dict):
        """ 
        Parameters
        ----------
        ccdprops_dict : dict
            a dictionary containing the following keys:
            'CCDNCOL': int
                number of columns in whole CCD
            'CCDNROW': int
                number of rows in whole CCD
            'NAMP': int
                number of amplifiers in CCD
            'prescan_size': int
                number of pixels of prescan
            'usual_gain_by_amp': list of length `namp`
                list of gain by amplifier, used to make the initial 
                guesses for the gaussian fits.
            'crosstalk_matrix': numpy array of shape [`namp`,`namp`]
                matrix to apply to remove cross-talk between amplifiers

        
        """

        self.NCOL = ccdprops_dict['CCDNCOL']
        self.NROW = ccdprops_dict['CCDNROW']
        self.NAMP = ccdprops_dict['NAMP']
        self.columns_by_amp = self.NCOL // 2
        self.prescan_size = ccdprops_dict['prescan_size']
        self.usual_gain_by_amp = ccdprops_dict['usual_gain_by_amp']
        self.crosstalk_matrix = ccdprops_dict['crosstalk_matrix']


def get_ccd_properties(img: FITS, verbose=False):
    """ Read the header of `img` and get the properties of the CCD, if it is known.

    Parameters
    -----------
    img : FITS
        the FITS object that contains the .fits data and header
    verbose : bool, optional
        whether to print what is being done or not

    Returns
    -------
    CCD
        an object with the CCD properties

    Raises
    ------
    UnknownCCDError
        If no known CCD matches the information in the header.
    """

    # get ccd params. 
    if verbose:
        print('> Getting CCD parameters...')

    ccdprops_dict = {}
    # these are fixed for each Skipper:
    CCDNCOL = int(img.hdr[0]['CCDNCOL'])
    CCDNROW = int(img.hdr[0]['CCDNROW'])

    ccdprops_dict['CCDNCOL'] = CCDNCOL
    ccdprops_dict['CCDNROW'] = CCDNROW
    
    if (CCDNCOL==724) and (CCDNROW==1248):
        ## toti params ##
        if verbose:
            print('Known CCD: \"Toti\".')
        ccdprops_dict['NAMP'] = 4
        ccdprops_dict['prescan_size'] = 8
        ccdprops_dict['usual_gain_by_amp'] = [605, 555, 519, 620]
        ccdprops_dict['crosstalk_matrix'] = 1/np.array([[1.0, 3362.0, 4069.0, 3991.0], 
                                    [3631.0, 1.0, 4337.0, 4393.0], 
                                    [4482.0, 4592.0, 1.0, 3793.0], 
                                    [4570.0, 4629.0, 3668.0, 1.0]])

    elif ((CCDNCOL==6144) or (CCDNCOL==684)) and (CCDNROW==1024): # first images, should be corrected later
        ## acds13 params ##
        if verbose:
            print('Known CCD: \"ACDS13\".')
        ccdprops_dict['NAMP'] = 4
        ccdprops_dict['prescan_size'] = 8
        ccdprops_dict['usual_gain_by_amp'] = [209, 200, 200, 200] # TBC
        ccdprops_dict['crosstalk_matrix'] = np.array(
            [[ 1.        , 1.7656e-04, 0., 0.],
             [ 1.6619e-04, 1.        , 0., 0.],
             [ 5.9560e-04, 6.0970e-04, 1., 0.],
             [ 0.        ,-4.8208e-04, 0., 1.]])
        ccdprops_dict['CCDNCOL'] = 684

    else:
        raise UnknownCCDError(ccdprops_dict)
    
    return CCD(ccdprops_dict)


def get_img_properties(img: FITS):
    # these depend on how the image was taken:
    NCOL = int(img.hdr[0]['NCOL'])
    NROW = int(img.hdr[0]['NROW'])
    # these keys do not always exist. Treat them as one if that is the case
    try:
        NVBIN = int(img.hdr[0]['NVBIN']) # in connie: NBINROW
    except KeyError:
        NVBIN = 1
    try:
        NHBIN = int(img.hdr[0]['NHBIN']) # in connie: NBINCOL
    except KeyError:
        NHBIN = 1
    try:
        LEVEL = img.hdr[0]['imglevel']
    except KeyError:
        LEVEL = 'unknown'

    return {'ncol': NCOL,
            'nrow': NROW,
            'nvbin': NVBIN, 
            'nhbin': NHBIN,
            'level': LEVEL,
            }


def _xtalk_iteration(x, y, slope_guess, gain, x_min):
    from ._auxiliary import recta
    from scipy.optimize import curve_fit

    y_max = x*slope_guess + .5*gain

    mask = (x>x_min) & (y<y_max)
    xdata = x[mask].flatten()
    ydata = y[mask].flatten()

    popt, pcov = curve_fit(recta, xdata, ydata)
    
    return popt


def get_xtalk(img: FITS, h0: int, h1: int, slope_guess: float,
              gain: int or list, x_min: float, iterations=None, tol=1e-7,
              plot=False, verbose=False):
    """ Find cross-talk matrix element between hdus `h0` and `h1` for given image.

    Performs a linear fit between the values of pixels in `h0` and the same pixels in `h1` and returns the slope. Takes into account the gain and the initial guess to fit only those pixels that should have a value of zero in `h1`.

    Parameters
    -----------
    img : FITS
        the FITS object that contains the .fits data
    h0, h1 : int
        number of the FITS hdus to which compute the cross-talk matrix
    slope_guess : float
        initial guess for the cross-talk value
    gain : int or list
        gain of the given hdus. If `int`, apply the same for each hdu; if `list`, use each element of the list as gain for each hdu
    x_min : float
        the minimum value of pixels `h0` to perform the linear fit
    iterations : int or None, optional
        number of iterations of the algorithm. If `None` (default), iterate until convergence to a tolerance of `tol`
    tol : float, optional
        tolerance to reach if `iterations==None`, ignored otherwise. Default: `1e-7`.
    plot : bool, optional
        whether to plot the process or not. Default: False

    Returns
    -------
    float
        the slope of the fit after all iterations.
    """
    
    if verbose: print(f'> Analyzing cross-talk between hdus {h0} & {h1}...')

    x = img.data[h0]
    y = img.data[h1]

    new_slope = slope_guess

    if iterations == None:
        if verbose: print(f'>> Will iterate until reaching convergence value of {tol}.')
        converged = False
        i = 0
        while not converged:
            if i > 20:
                print('Too many iterations!')
                raise ValueError
            i += 1
            if verbose: print(f'>>> Iteration {i}')
            new_slope, origin = _xtalk_iteration(x, y, new_slope, gain, x_min)
            if np.abs(slope_guess-new_slope) < tol:
                converged = True
            slope_guess = new_slope
            
    
    else:
        if verbose: print(f'>> Will iterate {iterations} times.')
        for i in range(iterations):
            if verbose: print(f'>>> Iteration {i+1}')
            new_slope, origin = _xtalk_iteration(x, y, new_slope, gain, x_min, tol)
        i += 1

    if verbose: print('> Done!\n')

    if plot:
        fig, axs = plt.subplots(1,2,sharex=True,sharey=True,figsize=(12,6))

        axs[0].plot(x.flatten(), y.flatten(), 'o', markersize=2)
        axs[0].set_xlabel(f'hdu {h0}')
        axs[0].set_ylabel(f'hdu {h1}')

        xx = np.linspace(0, x.max(), 5)
        yy = xx*new_slope + origin

        newy = y - x*new_slope

        axs[0].plot(xx, xx*new_slope+.5*gain, 'gray', ls='--')
        axs[0].plot(xx, yy, 'g--')
        axs[0].text(x_min, x_min*new_slope + .5*gain, f'slope={new_slope:.3e}')

        axs[1].plot(x.flatten(), newy.flatten(), 'o', markersize=2)
        axs[1].set_xlabel(f'hdu {h0}')
        axs[1].set_ylabel(f'Corrected hdu {h1}')

        if new_slope < 0:
            plt.ylim(x.max()*new_slope - gain, gain)
        else:
            plt.ylim(-gain, x.max()*new_slope - gain)
        plt.suptitle(f'Iteration {i}')
        plt.show()

    return new_slope


def skp2raw_lowmem(file_name: str):
    from astropy.io import fits
    hdu_list = fits.open(file_name)
    # chequear hdu vacíos
    new_hdu_list = []
    for i in range(len(hdu_list)):
        if hdu_list[i].data is None:
            continue
        new_hdu_list.append(hdu_list[i])
    hdu_list = new_hdu_list
    # número de hdus
    nhdu = len(hdu_list)
    # image dimensions
    Ny = int(hdu_list[0].header['NROW'])
    Nx = int(hdu_list[0].header['NCOL'])
    # get number of skipper samples
    Ns = int(hdu_list[0].header['NSAMP'])
    # Nx //= Ns
    # initialize new image
    new_data = np.zeros((nhdu, Ny, Nx))
    data_median = np.zeros(nhdu)
    for hdu in range(nhdu):
        # first reshape, then average
        rdata = hdu_list[hdu].data.reshape([Ny, Ns, Nx], order='F')
        skp = rdata.mean(axis=1)
        # subtract the hdu median
        data_median[hdu] = np.median(skp)
        data = skp - data_median[hdu]
        # save to new array
        new_data[hdu] = data
    # save as float32
    new_data = new_data.astype('float32')
    # return the FITS object
    hdr = [ hdu_list[i].header for i in range(nhdu) ]
    skp_img = FITS(data=new_data, header=hdr)
    skp_img.updateHeader('level', 'skp', 'averaged skipper samples')
    for hdu in range(nhdu):
        skp_img.updateHeader('median', data_median[hdu], 'subtracted median for this hdu')
    return skp_img


def skp2raw(img: FITS):
    """Average skipper samples """

    # get image dimenions & header
    nhdus, Ny, Nx = img.data.shape
    # get number of skipper samples
    Ns = int(img.hdr[0]['NSAMP'])
    Nx //= Ns
    # first reshape, then average
    rdata = img.data.reshape([nhdus, Ny, Ns, Nx], order='F')
    skp = rdata.mean(axis=2)
    # subtract the hdu median
    data_median = np.median(skp, axis=(1,2))
    data = skp - data_median[:,None,None]
    # return the FITS object
    skp_img = FITS(data=data, header=img.hdr)
    skp_img.updateHeader('level', 'skp', 'averaged skipper samples')
    for hdu in range(nhdus):
        skp_img.updateHeader('median', data_median[hdu], 'subtracted median for this hdu')
    return skp_img


def raw2proc(img: FITS, verbose=False, overscan=False, ccd=None,
             remove_xtalk=True, subtract_baseline=True):
    """Create a proc_ FITS from a raw_ FITS """
    if ccd == None:
        ccd = get_ccd_properties(img, verbose)
    # get the image properties
    img_prop = get_img_properties(img)
    NCOL = img_prop['ncol']
    NROW = img_prop['nrow']
    NHBIN = img_prop['nhbin']

    # split the data into parts
    if verbose:
        print('> Loading and splitting data...')
    
    prescan_size = int(np.ceil(ccd.prescan_size/NHBIN))
    data_size = int(np.floor(ccd.columns_by_amp/NHBIN))
    overscan_size = NCOL - prescan_size - int(np.ceil(ccd.columns_by_amp//NHBIN))

    exposed_data = img.data[:ccd.NAMP,:,prescan_size:prescan_size+data_size].copy()
    overscan_data = img.data[:ccd.NAMP,:,-overscan_size:].copy()

    # These may be used in the future
    # exposed_rms = img.data[ccd.NAMP:,:,prescan_size:-overscan_size]
    # overscan_rms = img.data[ccd.NAMP:,:,-overscan_size:]

    # subtract overscan mean line by line
    if subtract_baseline=='mean' or subtract_baseline==True:
        if verbose: 
            print('> Subtracting overscan mean by line...')

        # mask values outside usual zero range
        mask = [(hdu_overscan_data < -ccd.usual_gain_by_amp[i]*3) | 
                (hdu_overscan_data > ccd.usual_gain_by_amp[i]*3) 
                for i,hdu_overscan_data in enumerate(overscan_data)]
        masked_overscan_data = np.ma.array(overscan_data, mask=mask)

        # subtract mean from exposed and overscan data
        overscan_mean_by_line = masked_overscan_data.mean(axis=2)
        exposed_data -= overscan_mean_by_line[:,:,None]
        overscan_data -= overscan_mean_by_line[:,:,None]

    elif subtract_baseline=='fit':
        if verbose: 
            print('> Fitting overscan mean by line...')

        # define limits for histogram
        ovsc_min = [np.sort(overscan_data[hdu].flatten())[10] for hdu in range(ccd.NAMP)]
        ovsc_max = ovsc_min + 5*ccd.usual_gain_by_amp

        # create a FITS object for the overscan
        ovsc_raw = FITS(data=overscan_data)

        # get the zero for each hdu
        for hdu in range(ccd.NAMP):
            gain = ccd.usual_gain_by_amp[hdu]
            
            # first, locate the global zero
            hist = ovsc_raw.getHistogram(hdu, nbins=100, xmin=ovsc_min[hdu], xmax=ovsc_max[hdu])
            try:
                d0 = ovsc_raw.gaussianFit(hdu, xmax=ovsc_min[hdu]+gain*1.1)
            except:
                print(f'Could not find zero in hdu {hdu}. Skipping.')
                continue
            exposed_data[hdu] -= d0['mean']
            overscan_data[hdu] -= d0['mean']
            
            # now line by line
            for n in range(overscan_data.shape[1]):
                ovsc_line = FITS(data=overscan_data[hdu,n][None,None,:])
                hist = ovsc_line.getHistogram(0, xmax=ovsc_line.data.min()+gain*1.1, nbins=10)
                try:
                    d0 = ovsc_line.gaussianFit(0)
                except:
                    print(f'Could not find zero in line {n}, hdu {hdu}. Skipping.')
                    continue
                exposed_data[hdu, n] -= d0['mean']
                overscan_data[hdu, n] -= d0['mean']

    # correct cross-talk (apply linear matrix)
    if remove_xtalk:
        if verbose:
            print('> Correcting cross-talk...')
        exposed_data = np.dot(ccd.crosstalk_matrix, 
                    exposed_data.reshape((ccd.NAMP,-1))
                    ).reshape(exposed_data.shape)
        overscan_data = np.dot(ccd.crosstalk_matrix, 
                        overscan_data.reshape((ccd.NAMP,-1))
                        ).reshape(overscan_data.shape)

    # create the proc_ img
    if verbose:
        print('> Creating processed image(s)...')
    exposed_img = FITS(data=exposed_data.astype('float32'), header=img.hdr)
    if overscan:
        overscan_img = FITS(data=overscan_data.astype('float32'), header=img.hdr)
    # update header variables
    exposed_img.updateHeader('daqncol', NCOL, 'original number of columns')
    exposed_img.updateHeader('daqnrow', NROW, 'original number of rows')
    if overscan:
        overscan_img.updateHeader('daqncol', NCOL, 'original number of columns')
        overscan_img.updateHeader('daqnrow', NROW, 'original number of rows')
        NHDU, NROW, NCOL = overscan_data.shape
        overscan_img.updateHeader('ncol', NCOL, 'number of columns after processing')
        overscan_img.updateHeader('nrow', NROW, 'number of rows after processing')
        overscan_img.updateHeader('ovscan', True, 'this image corresponds to overscan')
        overscan_img.updateHeader('imglevel', 'proc', 'level of processing')
    NHDU, NROW, NCOL = exposed_data.shape
    exposed_img.updateHeader('ncol', NCOL, 'number of columns after processing')
    exposed_img.updateHeader('nrow', NROW, 'number of rows after processing')
    exposed_img.updateHeader('imglevel', 'proc', 'level of processing')

    if verbose: print('> All done! Returning ', end='')
    if overscan:
        if verbose: print('proc_ and ovsc_.')
        return exposed_img, overscan_img
    else:
        if verbose: print('proc_.')
        return exposed_img


def proc2cal(img: FITS, verbose=False, ccd=None, gain_list=None,
                cal_errors='break', return_gain=False, N_gaussians=3):
    """Create a cal_ FITS from a proc_ FITS.
    
    """
    # get ccd properties if not given
    if ccd == None:
        ccd = get_ccd_properties(img)
    
    # check if image is a proc
    img_prop = get_img_properties(img)
    LEVEL = img_prop['level']
    if LEVEL != 'proc':
        print('Warning: \'proc\' was not found in the image header. ')

    if verbose:
        print('> Calibrating image...')

    zero_list = np.zeros(img.nhdu)

    # get gain: fit two or three gaussians
    gain_fit_flag = False
    if gain_list == None:
        gain_fit_flag = True
        if verbose:
            print('> gain list not given, will try to fit gaussians.')
        zero_list = []
        gain_list = []
        N_0e_list = []
        N_1e_list = []
        if N_gaussians == 3:
            N_2e_list = []
        errors_by_hdu = []
        for hdu in range(ccd.NAMP):	
            hist = img.getHistogram(hdu, xmin=-ccd.usual_gain_by_amp[hdu], 
                            xmax=ccd.usual_gain_by_amp[hdu]*2.5, nbins=300)
            bin_width = hist[hdu,0,1] - hist[hdu,0,0]
            # first gaussian fit will get important parameters
            if verbose:
                print('> Performing initial Gaussian fit in hdu {}...'.format(hdu)
                      , end=' ')
            try:
                initial_fit = img.gaussianFit(hdu, 
                                xmax=ccd.usual_gain_by_amp[hdu]*.5)
            except Exception as e:
                print('Error: Could not perform initial Gaussian fit in hdu {}. Skipping.'.format(hdu))
                if cal_errors != 'break':
                    errors_by_hdu.append(hdu)
                    gain_list.append(1)
                    continue
                else: return None

            if verbose: print('success!')
            zeroth_amplitude = initial_fit['amp']
            hdu_noise = initial_fit['std']

            first_amplitude = hist[hdu,1][hist[hdu,0]>ccd.usual_gain_by_amp[hdu]][0]

            if N_gaussians == 2:
                p0 = [zeroth_amplitude, 0, hdu_noise, 
                    first_amplitude, ccd.usual_gain_by_amp[hdu], hdu_noise]
                # fit!
                if verbose:
                    print('> Performing two Gaussian fits in hdu {}...'.format(hdu)
                        , end=' ')
                try:
                    this_fit_results = img.N_GaussianFit(2, hdu, p0=p0)
                except Exception as e:
                    print('Error: Could not perform two Gaussian fit in hdu {}. Skipping.'.format(hdu))
                    if cal_errors != 'break':
                        errors_by_hdu.append(hdu)
                        gain_list.append(1)
                        continue
                    else: return None

            elif N_gaussians == 3:
                # initialize three gaussian fit parameters
                second_amplitude = hist[hdu,1][hist[hdu,0]>2*ccd.usual_gain_by_amp[hdu]][0]
                p0 = [zeroth_amplitude, 0, hdu_noise, 
                    first_amplitude, ccd.usual_gain_by_amp[hdu], hdu_noise, 
                    second_amplitude, ccd.usual_gain_by_amp[hdu]*2, hdu_noise]
                # fit!
                if verbose:
                    print('> Performing three Gaussian fits in hdu {}...'.format(hdu)
                        , end=' ')
                try:
                    this_fit_results = img.N_GaussianFit(3, hdu, p0=p0)
                except Exception as e:
                    print('Error: Could not perform three Gaussian fit in hdu {}. Skipping.'.format(hdu))
                    if cal_errors != 'break':
                        errors_by_hdu.append(hdu)
                        gain_list.append(1)
                        continue
                    else: return None

            if verbose: print('success!')
            # get the interesting data
            zero = this_fit_results['params_0']['mean']
            gain = this_fit_results['params_1']['mean'] - zero
            N_0e = this_fit_results['params_0']['amp'] * this_fit_results['params_0']['std'] * r2pi / bin_width
            N_1e = this_fit_results['params_1']['amp'] * this_fit_results['params_1']['std'] * r2pi / bin_width
            if N_gaussians == 3:
                N_2e = this_fit_results['params_2']['amp'] * this_fit_results['params_2']['std'] * r2pi / bin_width
            # save it
            zero_list.append(zero)
            gain_list.append(gain)
            N_0e_list.append(N_0e)
            N_1e_list.append(N_1e)
            if N_gaussians == 3:
                N_2e_list.append(N_2e)
        if errors_by_hdu != []:
            print('> Could not calibrate hdu(s) ', end='')
            for e in errors_by_hdu:
                print('{}, '.format(e), end='')
            print('')

    # create calibrated data
    calibrated_data = img.data - np.array(zero_list)[:,None,None]
    calibrated_data = calibrated_data / np.array(gain_list)[:,None,None]
    
    # create a calibrated image
    calibrated_img = FITS(data=calibrated_data.astype('float32'), 
                            header=img.hdr)
    for hdu in range(ccd.NAMP):
        
        calibrated_img.updateHeader('gain', gain_list[hdu], 'fitted gain', hdu=hdu)
        if gain_fit_flag:
            calibrated_img.updateHeader('zero', zero_list[hdu], 'fitted zero electron mean', hdu=hdu)
            calibrated_img.updateHeader('N_0e', N_0e_list[hdu], 'number of pixels with 0 electrons', hdu=hdu)
            calibrated_img.updateHeader('N_1e', N_1e_list[hdu], 'number of pixels with 1 electron', hdu=hdu)
            if N_gaussians == 3:
                calibrated_img.updateHeader('N_2e', N_2e_list[hdu], 'number of pixels with 2 electrons', hdu=hdu)
    calibrated_img.updateHeader('imglevel', 'cal', 'image calibrated in electrons')

    if verbose: print('> All done! Returning ', end='')
    if return_gain:
        if verbose: print('calibrated FITS and gain list.')
        return calibrated_img, gain_list

    else:
        if verbose: print('calibrated FITS.')
        return calibrated_img


def cal2phys(cal_img: FITS, verbose=False, max_e=2, max_sum=4, plot=False,
             mask_val=None, apply2D=True):
    """Create a phys_ img from a cal_ img. Apply the clustering algorithm.  """

    # check if image is a cal
    img_prop = get_img_properties(cal_img)
    LEVEL = img_prop['level']
    if LEVEL != 'cal':
        print('Warning: \'cal\' was not found in the image header. ')

    # default mask value to nan
    if mask_val is None:
        mask_val = -1

    # apply first clustering
    if verbose:
        print('> Applying first clustering ({}-D)...'.format(cal_img.nhdu))
    phys_image, mask = correlated_noise_clustering(cal_img.data, max_e, max_sum, mask_val, plot)

    if apply2D and cal_img.data.shape[0] > 2:
        if verbose: print('> Applying 2D clustering...', flush=True)
        # first create a list of temporary images (will average them later)
        n_temp_images = ((cal_img.nhdu)*(cal_img.nhdu-1))//2
        temp_image_list = np.nan*np.ones((n_temp_images,cal_img.nhdu,(~mask).sum()))

        # apply 2D clustering
        n = 0
        for i in range(cal_img.nhdu-1):
            for j in range(i, cal_img.nhdu-1):
                if verbose: print('> > hdus {} & {}'.format(i,j+1), flush=True)
                image = np.array([cal_img.data[i,~mask], cal_img.data[j+1,~mask]])
                this_max_sum = max_sum
                errors_2d = True
                while errors_2d:
                    if this_max_sum < 1:
                        print('2-D clustering between hdus {} and {} failed.'.format(i,j+1))
                        temp_image = np.nan*np.ones((2,(~mask).sum()))
                        break
                    try:
                        temp_image, temp_mask = correlated_noise_clustering(
                            image, max_e=max_e, max_sum=this_max_sum, mask_val=np.nan, plot=plot)
                        errors_2d = False
                    except ValueError:
                        this_max_sum -= 1
                temp_image_list[n,i] = temp_image[0]
                temp_image_list[n,j+1] = temp_image[1]
                n += 1

        # now average 
        if verbose: print('> > Averaging and masking values...')
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message='Mean of empty slice')
            avg_vals = np.nanmean(temp_image_list, axis=0)
        avg_vals[np.isnan(avg_vals)] = mask_val

        # check which values are integers, mask them if they are not
        integer_mask = (avg_vals == np.floor(avg_vals))
        avg_vals[~integer_mask] = mask_val

        # assign final values to the phys image
        phys_image[:,~mask] = avg_vals

    # round value of pixels above max_e+0.7
    if mask_val == -1:
        phys_image[cal_img.data>max_e+.7] = np.round(cal_img.data[cal_img.data>max_e+.7])

    # create the phys FITS
    phys_img = FITS(data=phys_image, header=cal_img.hdr)
    phys_img.updateHeader('imglevel', 'phys')

    return phys_img


def correlated_noise_clustering(image: np.ndarray, max_e=2, max_sum=4, 
                                mask_val=-1, plot=False):
    
    # number of clustering dimensions is same as hdus in the image
    N_dim = image.shape[0]
    # don't ask. This is magic. Initialize the means of the clusters
    means_by_dim = [np.arange(max_e+1) for i in range(N_dim)]
    mean_list = np.array(np.meshgrid(*means_by_dim)).T.reshape((-1,N_dim))
    # crop the clusters with sum > max_sum
    mean_list = mean_list[mean_list.sum(axis=1)<=max_sum]
   
    # generate the gaussian mixture model
    gmm = GaussianMixture(n_components=mean_list.shape[0], 
                          covariance_type='tied',
                          means_init=mean_list)
    
    # generate the data. First mask the image
    mask = image < max_e + 0.5
    mask = mask.all(axis=0)

    # mask if sum of values is greater than max_sum
    sum_mask = image.sum(axis=0) < max_sum+.7
    mask = np.all([sum_mask, mask], axis=0)

    train_data = image[:,mask].T

    # now begin the training!
    gmm.fit(train_data)

    # get the clusters
    predicted_clusters = gmm.predict(train_data)
    round_means = np.round(gmm.means_)

    # if we want to plot the clusters in a nice way
    if plot:
        color_index_list = _get_color_index(round_means, max_e)
        cluster_list = []
        for i in range(len(color_index_list)):
            cluster_list.append(color_index_list[i, predicted_clusters])
        _plot_clusters(train_data, cluster_list, N_dim, max_e)

    # now generate the phys_ image (note that masked pixels get a value of mask_val)
    phys_image = mask_val*np.ones(image.shape,dtype='int')
    for i in range(N_dim):
        phys_image[i,mask] = round_means[:,i][predicted_clusters]

    return phys_image, mask


def _plot_clusters(train_data, cluster_list, nhdus, max_e):
    # Initialize the plots
    fig, axs = plt.subplots(nhdus-1, nhdus-1, sharex=True, sharey=True, gridspec_kw={'hspace': 0, 'wspace': 0}, squeeze=False)
    # plot
    hidx = 0
    for j in range(nhdus-1):
        for i in range(j, nhdus-1):
            for n in range((max_e+1)**2+1):
                # plots a different set of data for each cluster
                axs[i][j].scatter(train_data[:,j][cluster_list[hidx]==n]
                                , train_data[:,i+1][cluster_list[hidx]==n]
                                , s=1)
            axs[i][j].grid()
            axs[i][j].set_xlim(-1,max_e+.5)
            axs[i][j].set_ylim(-1,max_e+.5)
            if j == 0: axs[i][j].set_ylabel('hdu {}'.format(i+1))
            if i == nhdus-2: axs[i][j].set_xlabel('hdu {}'.format(j))
            hidx += 1
    # delete the redundant axes
    for i in range(nhdus-1):
        for j in range(i+1, nhdus-1):
            fig.delaxes(axs[i][j])
    plt.show()


def _get_color_index(round_means: np.ndarray, max_e: int):
    nclusters = round_means.shape[0]
    nhdus = round_means.shape[1]
    
    color_index = np.zeros(((nhdus*(nhdus-1))//2, nclusters), dtype='uint8')

    hidx = 0
    for m in range(nhdus):
        for n in range(m+1, nhdus):
            cidx = 0
            for i in range(max_e+1):
                for j in range(max_e+1):
                    mask = (round_means[:,n]==i) & (round_means[:,m]==j)
                    color_index[hidx,mask] = cidx
                    cidx += 1
            hidx += 1
    
    return color_index


def generateMask(phys_img: FITS, structure=None, iterations=2,
                 serial_mask=False, bright_columns=False, event_charge=4,
                 mask_touching=False):

    """ Generate a mask for a FITS object.

    Parameters
    -----------
    phys_img : FITS
        the FITS object that contains the .fits data and header. Should be a 'phys'
        image, prints warning if not.
    structure : `numpy.ndarray` of shape (3,3), optional
        the structuring element to use in the binary dilation algorithm. If `None`
        (default), use a full structuring element (`np.ones((3,3))`) 
    iterations : int, optional
        the number of iterations for the binary dilation algorithm. Default is 2.
    serial_mask : bool, optional
        whether to apply or not a mask to try and filter serial register events.
        Default is `False`.
    bright_columns : bool, optional
        whether to apply or not a mask to try and filter bright columns.
        Default is `False`.
    event_charge : int, optional
        the charge in electrons of a pixel for it to be considered part of an event.
        Default is 4.
    mask_touching : bool, optional
        whether to mask pixels that touch with each other even if their charge is 
        lower than `event charge`. Default is False.

    Returns
    -------
    maskedFITS
        the FITS object plus the mask

    """

    from skimage.morphology import remove_small_objects
    from scipy.ndimage import binary_dilation, label

    # check if image is a phys
    try:
        img_prop = get_img_properties(phys_img)
        LEVEL = img_prop['level']
        if LEVEL != 'phys':
            print('Warning: \'phys\' was not found in the image header. ')
    except KeyError:
        print('Warning: data not found in the image header.')

    # event mask structure matrix
    if structure is None:
        structure = np.ones((3,3)) # full

    # generate binary masks
    
    event_mask = phys_img.data>=event_charge    # pixels with events
    undef_mask = phys_img.data==-1              # cal2phys masked pixels
    total_mask = np.zeros_like(event_mask)

    for hdu in range(phys_img.nhdu):
        # sum all masks
        total_mask[hdu] = event_mask[hdu]
        if mask_touching:
            # this masks all events except those which are isolated
            nonempty_mask = phys_img.data!=0    # all but empty pixels
            remove_small_objects(nonempty_mask[hdu], min_size=2, connectivity=1, in_place=True)
            total_mask[hdu] += nonempty_mask[hdu]

        # apply binary dilation
        total_mask[hdu] = binary_dilation(total_mask[hdu], structure=structure, iterations=iterations)

        # include pixels with undefined value
        total_mask[hdu] += undef_mask[hdu]

    # generate the masked fits
    mimg = maskedFITS(data=phys_img.data, mask=total_mask)

    # now mask serial register hits and bright columns
    for hdu in range(phys_img.nhdu):
        N_masked = -1
        while N_masked != 0:
            N_masked = 0

            if serial_mask:
                # serial register hits mask
                hcharge = mimg.data[hdu].mean(axis=1)
                serial_hit = hcharge>(hcharge.mean()+3*hcharge.std())
                serial_hit[1:]+=serial_hit[:-1] # extend to following line
                serial_hit_mask = np.repeat(serial_hit,mimg.data.shape[2]).reshape(mimg.data[hdu].shape)
                mimg.data[hdu].mask += serial_hit_mask
                N_masked += serial_hit.sum()

            if bright_columns:
                # bright columns mask
                vcharge = mimg.data[hdu].mean(axis=0)
                bright_col = vcharge>(vcharge.mean()+3*vcharge.std())
                bright_col_mask = np.repeat(bright_col,mimg.data.shape[1]).reshape(mimg.data[hdu].shape, order='F')
                mimg.data[hdu].mask += bright_col_mask
                N_masked += bright_col.sum()
    
    return mimg
