""" this module contains various color palette functions that are to be used with the Color().palette() function """

import os
import json
import random
from copy import deepcopy

from . import utilities

def uniform_random(last, **kwargs):
	""" Random values for r,g,b this is the least harmonious palette as its completely random """
	return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
	
def random_offset(last, **kwargs):
	""" produces a pelette of colors consisting of values + or - the given offset """
	if "offset" not in kwargs.keys():
		offset = 30
	else:
		offset = kwargs["offset"]
	
	r = last.r
	r = random.randint(r-offset, r+offset)
	g = last.g
	g = random.randint(g-offset, g+offset)
	b = last.b
	b = random.randint(b-offset, b+offset)
	
	
	return (r,g,b)

def golden_ratio(last, **kwargs):
	""" produces a palette rotating each colors hue by the golden ratio. each color is high in contrast to the last """
	gr = 0.618033988749895
	h, s, v = last.hsv
	h += gr*360
	return (utilities.hsv_to_rgb(h,s,v))
	
def random_hsv(last, **kwargs):
	""" random hue saturation and value/brightness values. if h, s or v specified those values won't be randomised """
	rh, rs, rv = False, False, False
	if "h" in kwargs.keys():
		rh = kwargs["h"]
	if "s" in kwargs.keys():
		rs = kwargs["s"]
	if "v" in kwargs.keys():
		rv = kwargs["v"]
	
	h, s, v = last.hsv
	if rh:
		h = random.randint(0,360)
		hrem = 1/random.randint(1, 10000)
		if h + hrem > 360:
			hrem = h + hrem - 360
		else:
			h += hrem
	if rs:
		s = random.randint(0,100)
	if rv:
		v = random.randint(0,100)
		
	return utilities.hsv_to_rgb(h, s, v)

def shades(last, length = 16, **kwargs):
	""" produces a palette varying from the base color to black """
	h, s, l = last.hsl
	l -= l/(length-1)
	return utilities.hsl_to_rgb(h, s, l)

def tints(last, length = 16, **kwargs):
	""" produces a palette varying from the base color to white """
	h, s, l = last.hsl
	l += l/(length+1)
	return utilities.hsl_to_rgb(h, s, l)
	
def tones(last, length = 16, **kwargs):
	""" produces a palette varying from the base color to grey """
	r, g, b = last.rgb
	m = max(r, g, b)
	if r == m:
		r = m
	else:
		r += m/(length+1)
	if g == m:
		g = m
	else:
		g += m/(length+1)
	if b == m:
		b = m
	else:
		b += m/(length+1)
	
	return r, g, b
	
def rainbow(last, length = 16, **kwargs):
	""" produces a palette rotating the hue 360° gradually"""
	h, s, l = last.hsl
	h += 360/(length+1)
	return utilities.hsl_to_rgb(h, s, l)

def color_list(last, length = 16, i = 0, colorlist=None,**kwargs):
	""" not sure if i still need this but havent deleted it in case it breaks everything """
	if colorlist is None:
		raise ValueError("Expected list of colors, got None")
	i %= len(colorlist)
	return colorlist[i].rgb

def random_hsl(last, **kwargs):
	""" random hue saturation and luminosity values. if h, s or l specified those values won't be randomised """
	rh, rs, rl = False, False, False
	if "h" in kwargs.keys():
		rh = kwargs["h"]
	if "s" in kwargs.keys():
		rs = kwargs["s"]
	if "l" in kwargs.keys():
		rl = kwargs["l"]
	
	h, s, l = last.hsl
	if rh:
		h = random.randint(0,360)
		hrem = 1/random.randint(1, 10000)
		if h + hrem > 360:
			hrem = h + hrem - 360
		else:
			h += hrem
	if rs:
		s = random.randint(0,100)
	if rl:
		l = random.randint(0,100)
		
	return utilities.hsl_to_rgb(h, s, l)
	
def all(last, steps = 16, **kwargs):
	""" debug function that returns a list containing all available palettes for the color """
	p = last
	x = p.gradient(p.compl, steps)
	x.extend(p.palette(steps, shades))
	x.extend(p.palette(steps, tints))
	x.extend(p.palette(steps, tones))
	x.extend(p.palette(steps, random_offset))
	x.extend(p.palette(steps, random_hsv, s = True))
	x.extend(p.palette(steps, random_hsv, v = True))
	x.extend(p.palette(steps, color_list, colorlist=p.analagous))
	x.extend(p.palette(steps, random_hsl, s = True, l = True))
	x.extend(p.palette(steps, color_list, colorlist=p.split_compl))
	x.extend(p.palette(steps, color_list, colorlist=p.triadic))
	x.extend(p.palette(steps, color_list, colorlist=p.tetradic))
	x.extend(p.palette(steps, golden_ratio))
	x.extend(p.palette(steps, rainbow))
	return x
	
def save(palette, path = "./", file= "SavedPallet", overwrite = True, **kwargs):
	""" not fully implemented
	saves the color palette to a json file """
	i = 1
	if not overwrite:
		while os.path.isfile(path+file+"-"+str(i) + ".json"):
			i += 1
	out_file = path + file + "-" + str(i) +".json"
	print(out_file)
	out = {}
	for c in palette:
		col = {}
		col["rgb"] = str(list(c.rgb))
		col["hsv"] = str([round(c.h, 2), round(c.s, 2), round(c.v, 2)])
		col["hsl"] = str([round(c.h, 2), round(c.s, 2), round(c.l, 2)])
		out[c.hex] = col
		
	out = {file: out}
		
	with open(out_file, "w") as of:
		of.write(json.dumps(out, indent=4))
	
def saveall(color, path = "./", file= "SavedPallet", overwrite = True, length = 16, **kwargs):
	""" not fully implemented
	saves all color palettes of a color to a json file """
	i = 1
	if not overwrite:
		while os.path.isfile(path+file+"-"+str(i) + ".json"):
			i += 1
	out_file = path + file + "-" + str(i) +".json"
	print(out_file)
	i = 1
	c = color.gradient(color.compl, length)
	for i, col in enumerate(c):
		c[i] = col.hex
	ti = color.palette(length, tints)
	for i, col in enumerate(ti):
		ti[i] = col.hex
	s = color.palette(length, shades)
	for i, col in enumerate(s):
		s[i] = col.hex
	to = color.palette(length, tones)
	for i, col in enumerate(to):
		to[i] = col.hex
	
	rows = {
	"complementary gradient": c,
	"tints": ti,
	"shades": s,
	"tones": to
	
	}
	with open(out_file, "w") as of:
		of.write(json.dumps(rows, indent=4))
