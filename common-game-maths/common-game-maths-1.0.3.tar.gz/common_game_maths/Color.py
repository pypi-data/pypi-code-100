class Color:
    def __init__(self, r, g, b, alpha=255):
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

        if self.r < 0 or self.g < 0 or self.b < 0 or self.alpha < 0:
            raise ValueError("color values can't be below 0")
        if self.r > 255 or self.g > 255 or self.b > 255 or self.alpha > 255:
            raise ValueError("color values can't be above 255")
    
    # Get the floating point representation between 0 and 1
    def scale_down(self):
        return Color(self.r / 255, self.g / 255, self.b / 255, self.alpha / 255)