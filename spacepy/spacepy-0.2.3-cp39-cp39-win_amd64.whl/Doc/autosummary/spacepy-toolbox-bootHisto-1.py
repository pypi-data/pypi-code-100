import numpy.random
import spacepy.toolbox
numpy.random.seed(0)
data = numpy.random.randn(1000)
bin_edges, low, high, sample, bars = spacepy.toolbox.bootHisto(
    data, plot=True)
