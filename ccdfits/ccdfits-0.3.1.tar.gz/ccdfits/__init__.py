"""
CCDfits
=======

Provides
  1. A simple way to view and analyze .fits images that were obtained with CCDs
  2. Algorithms to process images originated in Skipper CCDs

This package requires that `astropy`, `numpy`, `matplotlib` and `scipy` 
be installed within the Python environment.

Available modules
---------------------
processing
	Skipper CCD image processing tools

Classes
-------
FITS
	To easily manipulate data and headers from the images
maskedFITS
	To work with masked images
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.optimize import curve_fit
import os
from ._auxiliary import *

class _BaseFITS:
	"""
	Base class for FITS objects.

	...

	Attributes
	----------
	filename : str
		the name of the file from which the image was loaded
	nhdu : int
		the number of HDUs in the .fits file
	data : numpy array
		the values of the pixels in the image
	hdr : list of astropy Headers
		list of headers, one for each HDU
	"""

	def __init__(self):
			self.filename = None
			self.nhdu = None
			self.data = None
			self.hdr = None

	# Guarda la imagen a un archivo de nombre <filename>
	def save(self, filename, overwrite=True):
		"""
		Save the image to a file.

		Parameters
		----------
		filename : str
			The name of the file to which the new image will be saved.
		overwrite : bool, optional
			Whether to overwrite the file if it already exists or not
			(default is True)
		"""

		new_hdul = fits.HDUList()
		for hdu in range(self.nhdu):
			new_hdul.append(fits.ImageHDU(self.data[hdu], header=self.hdr[hdu]))
		new_hdul.writeto(filename, overwrite=overwrite)

	# permite visualizar una imagen fits (un solo hdu o todos)
	# imprime los fits dividiéndolos en los hdu y con escala de grises para ADU entre vmin y vmax (satura fuera de eso)
	def view(self, hdu=None, logscale=False, colorbar=True, save=False, pngname='foo.png', cmap='gnuplot', vmin=None, vmax=None, **kwargs):
		"""
		Visualize the image (one or all HDUs).

		Plots the images using `matplotlib` function `imshow`.

		Parameters
		----------
		hdu : int, optional
			The HDU to view. If `None` (default), plots all available HDUs in a nice way.
		logscale : bool, optional
			Whether to use a logarithmic scale in the colormap or not. Default is `False`.
		colorbar : bool, optional
			Whether to plot the colorbar beside the images or not. Default is `True`.
		save : bool, optional
			Whether to save the plotted image or not. If `True`, saves to the file
			defined by the `pngname` parameter. Default is `False`.
		pngname : str, optional
			Name of the file to which save the plotted image. This parameter is
			ignored if `save` parameter is `False`. Default is `'foo.png'`.
		cmap : str, optional
			Name of the colormap to use. Must be one of those listed in `plt.colormaps()`. Default: `'gnuplot'`.
		vmin : int or float, optional
			Minimum value of the colormap. Values lesser than `vmin` will appear with
			the same color as the minimum.  If `None` (default), takes the minimum
			value of the whole image data (or of the selected HDU).
		vmax : int or float, optional
			Maximum value of the colormap. Values greater than `vmax` will appear 
			with the same color as the minimum.  If `None` (default), takes the 
			maximum value of the whole image data (or of the selected HDU).
		**kwargs : 
			Keyword arguments passed to `plt.figure`.

		Returns
		-------
		`AxesImage`
			The created matplotlib image.

		"""
		# 4 imágenes separadas si no se especifica hdu
		if hdu == None:
			# Set subplots
			ncols = int(np.ceil(np.sqrt(self.nhdu)))
			nrows = int(np.ceil(self.nhdu / ncols))
			fig,axs = plt.subplots(nrows,ncols,sharex=True,sharey=True, squeeze=False, **kwargs)
			# Set cmap limits if not given
			if vmin == None:
				vmin = self.data.min()
			if vmax == None:
				vmax = self.data.max()
			# Plot
			for n in range(self.nhdu):
				ax = axs.flat[n]
				if logscale:
					if vmin <= 0:
						vmin = 0.1
					d = np.where(self.data[n]<vmin, vmin, self.data[n])
					im = ax.imshow(d, cmap=cmap, norm=colors.LogNorm(vmin=vmin, vmax=vmax, clip=True))
				else:
					im = ax.imshow(self.data[n], cmap=cmap, vmin=vmin, vmax=vmax)
				ax.set_title('hdu '+str(n))
			if colorbar:
					fig.colorbar(im, ax=axs, orientation='horizontal', shrink=.8)
			for n in range(self.nhdu, nrows * ncols):
				fig.delaxes(axs[n // ncols][n % ncols])
			#plt.tight_layout()
			fig.suptitle(str(os.path.basename(self.filename)))
			if save:
				plt.savefig(pngname)
				plt.close()
		# Imagen del hdu elegido
		else:
			# Set cmap limits if not given
			if vmin == None:
				vmin = self.data[hdu].min()
			if vmax == None:
				vmax = self.data[hdu].max()
			# plot
			fig = plt.figure(**kwargs)
			if logscale:
				if vmin <= 0:
					vmin = 0.1
				d = np.where(self.data[hdu]<vmin, vmin, self.data[hdu])
				im = plt.imshow(d, cmap=cmap, norm=colors.LogNorm(vmin=vmin, clip=True))
			else:
				im = plt.imshow(self.data[hdu], cmap=cmap, vmin=vmin, vmax=vmax)
			if colorbar:
				fig.colorbar(im, orientation='horizontal', shrink=.7)
			plt.title(str(os.path.basename(self.filename))+'; hdu '+str(hdu))
			if save:
				plt.savefig(pngname)
				plt.close()
		return im

	# Plottea histograma del fits (uno o todos los hdu)
	def plotHistogram(self, hdu=None, xmin=None, xmax=None, nbins=100, save=False, pngname='foo.png', **fig_kw):
		self.lastHist = np.zeros((self.nhdu,2,nbins))
		# Hace 4 histogramas separados si no se especifica el hdu
		if hdu == None:
			ncols = int(np.ceil(np.sqrt(self.nhdu)))
			nrows = int(np.ceil(self.nhdu / ncols))
			fig,axs = plt.subplots(nrows,ncols,sharex=True,sharey='row',constrained_layout=True, squeeze=False, **fig_kw)
			ax = axs.ravel()
			if xmin == None:
				xmin = self.data.min()
			if xmax == None:
				xmax = self.data.max()
			for n in range(self.nhdu):
				val, bins, foo = self._plotHistogram(ax[n], n, xmin, xmax, nbins)
				self.lastHist[n,0] = binCenters(bins)
				self.lastHist[n,1] = val
				ax[n].set_title('hdu '+str(n))
				ax[n].set_yscale('log')
				ax[n].set_ylim(ymin=0.9)
				ax[n].set_xlim(xmin,xmax)
				ax[n].grid()
			fig.suptitle(str(os.path.basename(self.filename)))
			for n in range(self.nhdu, nrows * ncols):
				fig.delaxes(axs[n // ncols][n % ncols])
			#plt.tight_layout()
			if save:
				plt.savefig(pngname)
				plt.close()
		# Sino, hace uno solo
		else:
			# configuración de matplotlib
			fig, ax = plt.subplots(**fig_kw)
			plt.xlabel('ADU')
			plt.ylabel('# pixels')
			plt.yscale('log')
			plt.grid(True)
			plt.title(str(os.path.basename(self.filename))+' - hdu '+str(hdu))
			# crea histograma
			if xmin == None:
				xmin = self.data[hdu].min()
			if xmax == None:
				xmax = self.data[hdu].max()
			val, bins, foo = self._plotHistogram(ax, hdu, xmin, xmax, nbins)
			self.lastHist[hdu,0] = binCenters(bins)
			self.lastHist[hdu,1] = val
			plt.ylim(ymin=0.9)
			plt.xlim(xmin,xmax)
			plt.tight_layout()
			# guarda si así se requiere
			if save:
				plt.savefig(pngname)
				plt.close()
		# retorna una copia de los histogramas
		return np.copy(self.lastHist)

	# lo mismo que arriba pero sin plottear
	def getHistogram(self, hdu=None, xmin=None, xmax=None, nbins=100):
		self.lastHist = np.zeros((self.nhdu,2,nbins))
		if hdu==None:
			if xmin == None:
				xmin = self.data.min()
			if xmax == None:
				xmax = self.data.max()
			for n in range(self.nhdu):
				val, bins = self._getHistogram(n, xmin, xmax, nbins)
				self.lastHist[n,0] = binCenters(bins)
				self.lastHist[n,1] = val
		else:
			if xmin == None:
				xmin = self.data[hdu].min()
			if xmax == None:
				xmax = self.data[hdu].max()
			val, bins = self._getHistogram(hdu, xmin, xmax, nbins)
			self.lastHist[hdu,0] = binCenters(bins)
			self.lastHist[hdu,1] = val
		return np.copy(self.lastHist)

	# plottear los valores de cada hdu en función de los demás
	# para ver el ruido correlacionado
	def plotCorrelated(self, xmin=None, xmax=None):
		fig, axs = plt.subplots(self.nhdu-1, self.nhdu-1, sharex=True, sharey=True, gridspec_kw={'hspace': 0, 'wspace': 0})

		if xmin == None: xmin = self.data.min()
		if xmax == None: xmax = self.data.max()

		for j in range(self.nhdu-1):
			for i in range(j, self.nhdu-1):
				axs[i][j].scatter(self.data[j].flatten(), self.data[i+1].flatten(),
									s=1)
				axs[i][j].grid()
				axs[i][j].set_xlim(xmin,xmax)
				axs[i][j].set_ylim(xmin,xmax)
				if j == 0: axs[i][j].set_ylabel('hdu {}'.format(i+1))
				if i == self.nhdu-2: axs[i][j].set_xlabel('hdu {}'.format(j))
		
		for i in range(self.nhdu-1):
			for j in range(i+1, self.nhdu-1):
				fig.delaxes(axs[i][j])


	# Actualiza el header del fits con la variable y valor provistos. La variable debe ser un string.
	def updateHeader(self, variable, value, comment='', hdu=None):
		if hdu == None:
			if type(self.hdr) is list:
				for hdr in self.hdr:
					hdr[variable] = (value,comment)
			else:		
				self.hdr[variable] = (value,comment)
		else:
			self.hdr[hdu][variable] = (value,comment)

	# Genera un único hdu a partir de los 4, rotándolos y alineándolos como corresponde
	def generateOneImg(self):
		ldata = np.concatenate([self.data[0], np.flip(self.data[1], axis=0)], axis=0)
		rdata = np.concatenate([np.flip(self.data[3],axis=1), np.flip(self.data[2])], axis=0)
		return FITS(data=np.concatenate([ldata,rdata],axis=1)[None,:], header=self.hdr)

	# Ajuste gaussiano a partir de un histograma
	def gaussianFit(self, hdu, xmin=None, xmax=None, ax=None):
		# define los valores del histograma a ajustar
		hist_x = self.lastHist[hdu,0]
		hist_y = self.lastHist[hdu,1]
		if xmin:
			mask = hist_x >= xmin
			hist_x = hist_x[mask]
			hist_y = hist_y[mask]
		if xmax:
			mask = hist_x < xmax
			hist_x = hist_x[mask]
			hist_y = hist_y[mask]
		# hace los initial guesses
		amp_guess = hist_y.max()
		mean_guess = hist_x[hist_y == hist_y.max()][0]
		std_guess = hist_x[hist_y > hist_y.max()/2][-1] - mean_guess
		p0 = [amp_guess, mean_guess, std_guess]
		# ajusta!
		popt, pcov = curve_fit(gaussian, hist_x, hist_y, p0=p0)
		# plottea el ajuste
		if ax is not None:
			ax.plot(hist_x,gaussian(hist_x, *popt),'g-', label='ajuste gaussiano')
		# guarda las variables que nos interesan
		amplitude = popt[0]
		mean = popt[1]
		std = popt[2]
		# Para calcular el reduced chi square
		hist_y_err = np.where(hist_y==0,1,np.sqrt(hist_y))
		redchisqr = 1.0/(hist_x.size-3)*np.sum(((gaussian(hist_x, *popt) - hist_y)/hist_y_err)**2)
		return {'amp': amplitude, 
				'mean': mean, 
				'std': std, 
				'red_chi_sqr': redchisqr,
				'cov_matrix': pcov}

	def N_GaussianFit(self, N, hdu, p0, ax=None, xmin=None, xmax=None):
		# define qué función va a ajustar
		f_to_fit = N_gaussians(N)
		# define los valores del histograma a ajustar
		hist_x = self.lastHist[hdu,0]
		hist_y = self.lastHist[hdu,1]
		if xmin:
			mask = np.where(hist_x >= xmin)
			hist_x = hist_x[mask]
			hist_y = hist_y[mask]
		if xmax:
			mask = np.where(hist_x < xmax)
			hist_x = hist_x[mask]
			hist_y = hist_y[mask]
		# Fittea
		popt, pcov = curve_fit(f_to_fit, hist_x, hist_y, p0=p0)
		# Plottea
		if ax is not None:
			ax.plot(hist_x,f_to_fit(hist_x, *popt),'r-', label='ajuste gaussiano')
		# Para calcular el reduced chi square
		hist_y_err = np.where(hist_y==0,1,np.sqrt(hist_y))
		redchisqr = 1.0/(hist_x.size-3)*np.sum(((f_to_fit(hist_x, *popt) - hist_y)/hist_y_err)**2)
		# valores a retornar
		d = {}
		for n in range(N):
			d['params_{}'.format(n)] = {'amp':  popt[n*3],
										'mean': popt[(n*3+1)],
										'std':  popt[(n*3+2)]}
		d['cov_matrix'] = pcov
		d['red_chi_sqr'] = redchisqr
		return d


class FITS(_BaseFITS):
	# carga una imagen FITS.
	def __init__(self, filename=None, data=None, header=None):
		self.lastHist = None
		if filename == None:
			self.data = np.copy(data)
			self.nhdu = data.shape[0]
			if header == None:
				self.hdr = [fits.Header() for i in range(self.nhdu)]
			else: 
				self.hdr = [fits.Header(header[i], copy=True) for i in range(self.nhdu)]
			self.filename = ''
		else:
			self.filename = filename
			hdu_list = fits.open(filename)
			# chequear hdu vacíos
			new_hdu_list = []
			for i in range(len(hdu_list)):
				if hdu_list[i].data is None:
					continue
				new_hdu_list.append(hdu_list[i])
			# número de hdus
			self.nhdu = len(new_hdu_list)
			# valor de los píxeles en forma de numpy array de shape nhdu x NROW x NCOL
			self.data = np.array([new_hdu_list[n].data for n in range(self.nhdu)])
			# header
			self.hdr = [new_hdu_list[n].header for n in range(self.nhdu)]
			hdu_list.close()

	# genera un maskedFITS con la misma metadata
	#def to_maskedFITS(self, mask):


	def _plotHistogram(self, ax, hdu, xmin, xmax, nbins):
		return ax.hist(self.data[hdu].flatten(), bins=np.linspace(xmin,xmax,nbins+1))
	
	def _getHistogram(self, n, xmin, xmax, nbins):
		return np.histogram(self.data[n].flatten(), bins=np.linspace(xmin,xmax,nbins+1))

# Clase para analizar imágenes enmascaradas
class maskedFITS(_BaseFITS):
	def __init__(self, data, mask):
		# Create masked array
		self.data = np.ma.masked_array(data=data, mask=mask)
		self.nhdu = data.shape[0]
		self.filename = ''
		self.lastHist = None
		# Create compressed data array(s)
		# if len(self.shape) == 3:
		# 	self.cdata = [self.data[n].compressed() for n in range(self.shape[0])]
		# elif len(self.shape) == 2:
		# 	self.cdata = self.data.compressed()
		# else:
		# 	print('Warning: wrong data shape (expected 2D or 3D): {}'.format(self.shape))

	def _plotHistogram(self, ax, hdu, xmin, xmax, nbins):
		return ax.hist(self.data[hdu].compressed(), bins=np.linspace(xmin,xmax,nbins+1))

	def _getHistogram(self, n, xmin, xmax, nbins):
		return np.histogram(self.data[n].compressed(), bins=np.linspace(xmin,xmax,nbins+1))

	def changeMask(self, newmask):
		self.data = np.ma.masked_array(data=self.data.data, mask=newmask)
		# self.cdata = self.data.compressed()

