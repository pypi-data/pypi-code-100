##############################################################################
# python equivalent of matlabs' tic & toc functions
# taken from: https://stackoverflow.com/questions/5849800/what-is-the-python-equivalent-of-matlabs-tic-and-toc-functions
import time
def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(dsp=1, tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        if dsp: print( "Elapsed time: %f seconds.\n" %tempTimeInterval )
        return tempTimeInterval

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)
TicToc2 = TicTocGenerator() # create another instance of the TicTocGen generator

def toc2(dsp=1, tempBool=True):
    # Prints the time difference yielded by generator instance TicToc2
    tempTimeInterval = next(TicToc2)
    if tempBool:
        if dsp: print("Elapsed time 2: %f seconds.\n" %tempTimeInterval)
        return tempTimeInterval   
def tic2():
    # Records a time in TicToc2, mar
    toc2(False)
##############################################################################
