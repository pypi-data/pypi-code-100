""" this module contains useful functions for converting between colorspaces """

import math

def rgb_to_hsv(r, g, b, maximum=255):
    """ convert from rgb to hsv """
    r = float(r)
    g = float(g)
    b = float(b)
    if r > 1 or g > 1 or b > 1:
    	r /= maximum
    	g /= maximum
    	b /= maximum
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d/high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return round(h*360, 2), round(s*100, 2), round(v*100, 2)

def hsv_to_rgb(h, s, v, maximum = 255):
    """ convert from hsv to rgb """
    h = h/360
    s = s/100
    v = v/100
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]

    return round(r*maximum), round(g*maximum), round(b*maximum)

def rgb_to_hsl(r, g, b):
    """ convert from rgb to hsl """
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, l = ((high + low) / 2,)*3

    if high == low:
        h = 0.0
        s = 0.0
    else:
        d = high - low
        s = d / (2 - high - low) if l > 0.5 else d / (high + low)
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h, s, l

def hsl_to_rgb(h, s, l, maximum = 255):
    """ convert from hsl to rgb """
    h, s, v = hsl_to_hsv(h,s,l)
    return hsv_to_rgb(h,s,v)

def hsv_to_hsl(h, s, v):
    """ convert from hsv to hsl """
    h = h/360
    s = s/100
    v = v/100
    if h >= 1:
    	h = 0.9999
    elif h <= 0:
    	h = 0.0001
    if s >= 1:
    	s = 0.9999
    elif s <= 0:
    	s = 0.0001
    if v >= 1:
    	v = 0.9999
    elif v <= 0:
    	v = 0.0001
    l = 0.5 * v  * (2 - s)
    s = v * s / (1 - math.fabs(2*l-1))
    return h*360, s*100, l*100

def hsl_to_hsv(h, s, l):
    """ convert from hsv to hsl """
    h = h/360
    s = s/100
    l = l/100
    if h >= 1:
    	h = 0.9999
    elif h <= 0:
    	h = 0.0001
    if s >= 1:
    	s = 0.9999
    elif s <= 0:
    	s = 0.0001
    if l >= 1:
    	l = 0.9999
    elif l <= 0:
    	l = 0.0001
    
    
    v = (2*l + s*(1-math.fabs(2*l-1)))/2
    s = 2*(v-l)/v
    return h*360, s*100, v*100
    
def hex_to_rgb(string):
	""" convert hex to rgb """
	if len(string) >= 2:
		if string[0] == "#" or string[0:2] == "0x":
			if string[0] == "#":
				string = string[1:]
			else:
				string = string[2:]
			for char in string:
				if char not in ("0","1","2","3","4","5","6","7","8","9", "a", "b", "c", "d", "e", "f"):
					raise ValueError(f"Not hex value: {char}")
		if len(string) == 4:
			string = string[:-1]
		elif len(string) == 8:
			string = string[:-2]
			
		if len(string) == 3:
			r, g, b = string[0], string[1], string[2]
		elif len(string) == 6:
			r, g, b = string[0:2], string[2:4], string[4:6]
		else:
			raise ValueError(f"Invalid hex 0x{string}")
		
		
	else:
		raise ValueError(f"Invalid hex: {string}")
	
	r = int(f"0x{r}", 16)
	g = int(f"0x{g}", 16)
	b = int(f"0x{b}", 16)
	return r,g,b
	
			
	
def rgb_to_hex(r, g, b):
	""" convert rgb to hex """
	h = ("0","1","2","3","4","5","6","7","8","9", "a", "b", "c", "d", "e", "f")
	
	r1, r2 = int(r/16), int(float("0." + str(r/16).split(".")[-1])*16)
	r = h[r1] + h[r2]
	g1, g2 = int(g/16), int(float("0." + str(g/16).split(".")[-1])*16)
	g = h[g1] + h[g2]
	b1, b2 = int(b/16), int(float("0." + str(b/16).split(".")[-1])*16)
	b = h[b1] + h[b2]
	return f"0x{r}{g}{b}"
	
