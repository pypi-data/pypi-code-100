from scipy import stats
import shutil
import importlib
import xspec
import astropy.io.fits as fits
import os
import numpy as np
from IPython.display import Image


def view_group_spectra(r, reference_instrument, subcases_pattern, systematic_fraction=0.):
    # I add response and arf keywords for easier reading
    import astropy.io.fits as pf

    if reference_instrument.lower() == 'spi':
        ff=pf.open(r["reference_spec"],  mode='update')
        try:
            reference_exposure=ff[2].header['EXPOSURE']
            ff[2].header['RESPFILE']=r["reference_rmf"]
        except:
            try:
                reference_exposure=ff[1].header['EXPOSURE']
                ff[1].header['RESPFILE']=r["reference_rmf"]
            except:
                raise ValueError("Exposure should be in SPI spectrum!")
        reference_times='N/A'
        ff.flush()
        ff.close()
    elif reference_instrument.lower() == 'nustar':
        for x in ['A', 'B']:
            
            ff=pf.open(r["reference_spec_"+x],  mode='update')
            ff[1].header['RESPFILE']=r["reference_rmf_"+x]
            ff[1].header['ANCRFILE']=r["reference_arf_"+x]
            ff[1].header['BACKFILE']=r["reference_bkg_"+x]
            reference_exposure=ff[1].header['EXPOSURE']
            mjdref=float(ff[1].header['MJDREFI'])+float(ff[1].header['MJDREFF'])
            tstart=float(ff[1].header['TSTART'])/86400. + mjdref
            tstop=float(ff[1].header['TSTOP'])/86400. + mjdref
            reference_times='%.4f--%.4f'%(tstart,tstop)
            
            #reference_date=ff[1].header['DATE-OBS'] + '--'+ ff[1].header['DATE-END']
            ff.flush()
            ff.close()
    elif reference_instrument.lower().replace("'","") == 'none':
        reference_exposure='N/A'
        reference_times='N/A'
    else:
        print("Undefined reference instrument")
        raise ValueError


    ff=pf.open(r["isgri_spec"],  mode='update')
    ff[1].header['RESPFILE']=r["isgri_rmf"]
    ff[1].header['ANCRFILE']=r["isgri_arf"]
    ff[1].data['SYS_ERR']=systematic_fraction
    mjdref=51544.
    tstart=float(ff[1].header['TSTART']) + mjdref
    tstop=float(ff[1].header['TSTOP']) + mjdref
    isgri_times='%.4f--%.4f'%(tstart,tstop)
    isgri_exposure=ff[1].header['EXPOSURE']
    ff.flush()
    ff.writeto('isgri_spec'+subcases_pattern+'_'+isgri_times+'.fits', overwrite=True)
    ff.close()

    shutil.copy(r["isgri_rmf"],'isgri_rmf'+subcases_pattern+'_'+isgri_times+'.fits' )
    shutil.copy(r["isgri_arf"],'isgri_arf'+subcases_pattern+'_'+isgri_times+'.fits' )

    print("reference exposure",reference_exposure,"isgri exposure",isgri_exposure, "isgri time range", isgri_times, reference_times)

    return dict(
                reference_exposure=reference_exposure,
                isgri_exposure=isgri_exposure,
                isgri_times=isgri_times,
                reference_times=reference_times,
            )

def basic_consistency(fit_by_lt, nh_sig_limit):
    # marginally more adcanced choice of low thresholds
    print("lt\tchi2_r\tprob\tsigmas")
    for lt,d in fit_by_lt.items():
        d['nh_prob']=stats.chi2(d['ndof']).sf(d['chi2'])
        d['nh_sig']=stats.norm().isf(d['nh_prob'])
        print("%.1f\t%.2f\t%.2f\t%.2f"%(float(lt), d['chi2_red'], d['nh_prob'], d['nh_sig']) )
    try:
        good_lt = min([p for p in fit_by_lt.items() if p[1]['nh_sig'] < nh_sig_limit])
    except:
        good_lt = None
    best_lt = min([p for p in fit_by_lt.items()], key=lambda x:x[1]['chi2_red'])

    if good_lt != best_lt:
        print("\033[31mNote that in this case, best LT does not coincde with the good LT. We want broader energy range\033[0m")

    if good_lt is not None:
        return good_lt
    else:
        return best_lt


def fit(data, reference_instrument, model_setter, emin_values, fn_prefix="", systematic_fraction=0):
    importlib.reload(xspec)

    if isinstance(emin_values, str):
        emin_values = map(float, emin_values.split(","))

    fit_by_lt = {}
    fn_by_lt={}

    xspec.AllModels.systematic=systematic_fraction

    for c_emin in emin_values:

        xspec.AllData.clear()
        xspec.AllModels.clear()

        isgri, ref_ind = model_setter(data, reference_instrument, c_emin)

        

        max_chi=np.ceil(xspec.Fit.statistic / xspec.Fit.dof)
        m1=xspec.AllModels(1)

        if ref_ind is not None:
            n_spec = 2
            if isinstance(ref_ind, list):
                n_spec = len(ref_ind) + 1
            xspec.Fit.error("1.0 max %.1f 1-%d"%(max_chi, n_spec*m1.nParameters))
            ref = ref_ind[0]
        else:
            xspec.Fit.error("1.0 max %.1f 1-%d" % (max_chi,m1.nParameters))

        models={}

        lt_key='%.10lg'%c_emin
    
        fit_by_lt[lt_key]=dict(
                emin=c_emin,
                chi2_red=xspec.Fit.statistic/xspec.Fit.dof,                                
                chi2=xspec.Fit.statistic,
                ndof=xspec.Fit.dof,                                    
                models=models,
            )
            
        for m, ss in (isgri, 'isgri'), (ref, 'ref'):
            if m is None: continue

            #initialize dictionaries
            models[ss]={}
            #models[ss]['flux']={}
            
            #fills dictionaries
            for i in range(1,m.nParameters+1): 
                if (not m(i).frozen) and (not bool(m(i).link)):
                    #use the name plus position because there could be parameters with same name from multiple 
                    #model components (e.g., several gaussians)
                    print(m(i).name, "%.2f"%(m(i).values[0]), m(i).frozen,bool(m(i).link) )
                    models[ss][m(i).name+"_%02d"%(i)]=[ m(i).values[0], m(i).error[0], m(i).error[1] ]              
            
            


    #     for flux_e1, flux_e2 in [(30,80), (80,200)]:
    #         xspec.AllModels.calcFlux("{} {} err".format(flux_e1, flux_e2))
    #         #print ( xspec.AllData(1).flux)
    #         models['isgri']['flux'][(flux_e1, flux_e2)] = xspec.AllData(1).flux
    #         models['ref']['flux'][(flux_e1, flux_e2)] = xspec.AllData(2).flux

            
        xcmfile="saved"+fn_prefix+"_"+reference_instrument+".xcm"
        if os.path.exists(xcmfile):
            os.remove(xcmfile)

        xspec.XspecSettings.save(xspec.XspecSettings, xcmfile, info='a')

        xspec.Plot.device="/png"
        #xspec.Plot.addCommand("setplot en")
        xspec.Plot.xAxis="keV"
        xspec.Plot("ldata del")
        xspec.Plot.device="/png"
        
        fn="fit_lt%.5lg.png"%c_emin
        
        fn_by_lt[lt_key] = fn
        
        shutil.move("pgplot.png_2", fn)

        _=display(Image(filename=fn,format="png"))

    return fit_by_lt, fn_by_lt


def parameter_comparison(good_lt, ng_sig_limit, reference_instrument, flux_tolerance=0.1):
    #compare parameters of best fit
    parameter_comparison={}
    best_result=good_lt[1]
    for par_name, par_values_ref in best_result['models']['ref'].items():
        try:
            par_values_isgri=best_result['models']['isgri'][par_name]
        except:
            print("parameter %s is not in isgri parameter list"%(par_name))
            continue
        isgri_value = par_values_isgri[0]
        ref_value = par_values_ref[0]
        
        if ref_value > isgri_value:
            err_ref = ref_value - par_values_ref[1]
            err_isgri = par_values_isgri[2] - isgri_value
        else:
            err_ref = - (ref_value - par_values_ref[2])
            err_isgri = - (par_values_isgri[1] - isgri_value)

        par_diff_sigmas = (isgri_value - ref_value) / np.sqrt(err_ref**2 + err_isgri**2)

        print(par_name + " %.2f +/- %.2f ; %.2f +/- %.2f ; %.1f" % (
        isgri_value, err_isgri, ref_value, err_ref, par_diff_sigmas))
        
        #We do not compare the normalization with NuSTAR strictly, because of non-simultaneity issues
        if (('g10Flux' in par_name) or ('norm' in par_name)) and (reference_instrument.lower() == 'nustar') :
            print("Not comparing %s for %s"%(par_name, reference_instrument))
            success = True
        elif 'g10Flux' in par_name and np.abs(par_diff_sigmas) > ng_sig_limit:
            frac_difference = np.abs( 1 - 10**(isgri_value - ref_value))
            print("Using a fractional difference of %f to compare %s for %s" % (frac_difference,
                                                                                par_name, reference_instrument))
            success = bool(frac_difference < flux_tolerance)
        elif 'norm' in par_name and np.abs(par_diff_sigmas) > ng_sig_limit:
            frac_difference = np.abs( 1 - isgri_value / ref_value)
            print("Using a fractional difference of %f to compare %s for %s" % (frac_difference,
                                                                                par_name, reference_instrument))
            success = bool(frac_difference < flux_tolerance)
        else:
            #print("standard comparison for %s"%par_name)
            success = bool(np.abs(par_diff_sigmas) < ng_sig_limit)

        parameter_comparison[par_name] = dict(
            ref = [ref_value, err_ref],
            isgri = [isgri_value, err_isgri ],
            significance = np.abs(par_diff_sigmas),
            success=success
        )

    return parameter_comparison


def write_down_oda_spectrum(spectrum, write_to_dir):
    all_ext = []

    files_by_source_name = {}

    for name in set([s.meta_data['src_name'] for s in spectrum._p_list]):
        print(f"writting down spectra for {name}")
        
        d = {}
        files_by_source_name[name] = d
        
        src_name_stub = name.replace(' ', '_').replace('+','p')    
        
        d['spec_fn'] = write_to_dir + "/isgri_spectrum_{}.fits".format(src_name_stub)
        d['arf_fn'] = write_to_dir + "/isgri_arf_{}.fits".format(src_name_stub)
        d['rmf_fn'] = write_to_dir + "/isgri_rmf_{}.fits".format(src_name_stub)

        specprod_for_source = [l for l in spectrum._p_list if l.meta_data['src_name'] == name ]

        for p in specprod_for_source:
            print(p.meta_data)

        specprod_for_source[0].write_fits_file(d['spec_fn'])
        specprod_for_source[1].write_fits_file(d['arf_fn'])
        specprod_for_source[2].write_fits_file(d['rmf_fn'])
        
        all_ext.extend(fits.open(d['spec_fn'])[1:])
        all_ext.extend(fits.open(d['arf_fn'])[1:])
        all_ext.extend(fits.open(d['rmf_fn'])[1:])
        
    all_spectra_file = "isgri_all.fits"
    fits.HDUList([fits.PrimaryHDU()] + all_ext).writeto(all_spectra_file, overwrite=True)

    return files_by_source_name, all_spectra_file