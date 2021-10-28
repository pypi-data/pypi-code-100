import numpy as np
from calculation.pixel import Pixel


class Reflection:

    @staticmethod
    def mask_convert_big_image(y0, x0, rgb_mask, horizon):
        mask_covnert_x = []
        mask_covnert_y = []
        rgb_mask = (np.nonzero(rgb_mask))
        if len(rgb_mask[0]) == len(rgb_mask[1]) and rgb_mask is not None:
            for i in range(len(rgb_mask[0])):
                [x, y] = rgb_mask[0][i], rgb_mask[1][i]
                temp = Pixel.calc_origin(y0, x0, [y, x], 1, 1, horizon)
                mask_covnert_x.append(temp[0])
                mask_covnert_y.append(temp[1])
        else:
            raise Exception("Mask points X must be equal Y")

        return [mask_covnert_x, mask_covnert_y, rgb_mask[2]]