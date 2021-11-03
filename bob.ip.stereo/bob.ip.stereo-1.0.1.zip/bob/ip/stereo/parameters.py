import json

class StereoParameters:
    """ This class stores parameters for the OpenCV's 
        stereo semi-global block matching algorithm (SGBM). 
        Please refer to OpenCV's documentation for more information.

        Attributes
        ----------
        min_disparity : int
            Minimum possible disparity value.
        num_disparities : int
            Maximum disparity minus minimum disparity, this parameter must be divisible by 16.
        blockSize : int
            Matched block size, in the 3-11 range.
        normalise : bool
            Normalise left and right images.
        downscale : bool
            Downscale left and right images.
        erode : bool
            Erode disparity holes borders before inpaint.
        inpaint : bool
            Inpaint holes in the disparity map.
    """

    STEREO_CV_SGBM = 0

    def __init__(   self,
                    algorithm           = STEREO_CV_SGBM,
                    min_disparity       = 128,
                    num_disparities     = 96,
                    block_size          = 15,
                    window_size         = 11,
                    disp12_max_diff     = 5,
                    uniqueness_ratio    = 5,
                    speckle_window_size = 400,
                    speckle_range       = 32,
                    sgbm_mode           = 0,
                    normalise           = True,
                    downscale           = True,
                    erode               = False,
                    inpaint             = False):

        self.algorithm              = algorithm

        # OPENCV_SGBM
        self.min_disparity          = min_disparity
        self.num_disparities        = num_disparities
        self.block_size             = block_size
        self.window_size            = window_size
        self.p1                     = 8*3*self.window_size**2
        self.p2                     = 32*3*self.window_size**2
        self.disp12_max_diff        = disp12_max_diff
        self.uniqueness_ratio       = uniqueness_ratio
        self.speckle_window_size    = speckle_window_size
        self.speckle_range          = speckle_range
        self.sgbm_mode              = sgbm_mode

        # post processing
        self.normalize              = normalise
        self.downscale              = downscale
        self.erode                  = erode
        self.inpaint                = inpaint

    def save(self, filepath):
        """ Save parameters to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self, f, default=lambda x: x.__dict__, indent=4)

    def load(self, filepath):
        """ Load parameters from a JSON file."""
        with open(filepath) as f:
            data = json.load(f)
            for key in self.__dict__:
                try:
                    new_val = data[key]
                    self.__dict__[key] = new_val
                except:
                    pass
