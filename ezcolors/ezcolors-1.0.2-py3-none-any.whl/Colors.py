""" this module contains the definition of the color class a simple and easy to use class for anything colorful in all color spaces """

import json
import textdistance
from copy import copy, deepcopy

from .utilities import *
from .palettes import *

#checks for numpy
try:
	import numpy as np
	numpy_enabled = True
except:
	numpy_enabled = False

#"C:/Users/Y0L0S.DESKTOP-LE6HALS/Documents/ezcolors/src/ezcolors/web.json"
with open("/".join(__file__.split("/")[0:-1]) + "/web.json") as f:
	string = ""
	for line in f:
		string += line
	web = json.loads(string)
	del string

class Color():
	""" Color class that can be constructed with either a string (hex value or color name), singular r, g and b values or a list/tuple of rgb/hsv/hsv values """
	def __init__(self, r:int =0, g:int =0, b:int =0, a:int =255, s:str ="", space:str = "wiki", range: int = 255, name:str = None, **kwargs):
		""" r, g, b, a are the red green blue and alpha  values of the color if a string is given then it will ignore these values and try to match that string to a color and become that color
		s is the string representation of the color. this can be a hex or a name
		space is whether you want to use the full gammut of colors from Names.json ('wiki') or to limit to the web safe colors
		name is for if you wish to define a name for the color 
		
		additional kwargs:
			rgb=(list/tuple) creates a color from rgb
			rgba=(list/tuple) creates a color from rgba
			hsv=(list/tuple) creates a color from hsv
			hsl=(list/tuple) creates a color from hsl
		"""
		if "rgb" in kwargs.keys():
			r = kwargs["rgb"][0]
			g = kwargs["rgb"][1]
			b = kwargs["rgb"][2]
			a = 255
		elif "rgba" in kwargs.keys():
			r = kwargs["rgba"][0]
			g = kwargs["rgba"][1]
			b = kwargs["rgba"][2]
			a = kwargs["rgba"][3]
		elif "hsl" in kwargs.keys():
			hsl = kwargs["hsl"]
			r,g,b = hsl_to_rgb(*hsl)
			a = 255
			print(r,g,b, "bitch")
		elif "hsv" in kwargs.keys():
			hsv = kwargs["hsv"]
			r,g,b = hsv_to_rgb(*hsv)
			a = 255
		
		
		if space in (web, "web", "Web", 0):
			space = web
		elif space in (wiki, "wiki", "Wiki", 1):
			space = wiki
		elif space in ("x11", "X11", 2):
			#not implemented
			pass
		elif space in ("terminal", "Terminal", 3):
			#not implemented
			pass
		elif space in ("all", "All", -1):
			#not implemented
			pass
		self.space = space
		if type(r) == str:
			s = r
			r = 0
		self._name = name
		self.refresh_name = False
		self._r = r
		self._g = g
		self._b = b
		self._a = a
		self._range = range
		if s != "":
			self._r, self._g, self._b, self.a = string_to_color(s, space=space).rgba
		
		self.clamp()
		
	def random(**kwargs):
		""" Used to define a random color 
		with no arguments it'll return a random colour with random r,g,b values
		alternatively you can give it a list of values of length 0-3 any value that is None not given will be randomly generated
		rgb= red, green, blue
		hsv= hue, saturation, value
		hsl= hue, saturation, luminosity
		eg Color.random(hsl = [345, 100] will return a random color with hue 345° saturation 100% and random luminosity"""
		rgbrandoms = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
		hsxrandoms = random.randint(0, 360), random.randint(0, 100), random.randint(0, 100)
					
		if len(kwargs.keys()) == 0:
			kwargs["rgb"] = None, None, None
		if "rgb" in kwargs.keys():
			rgb = []
			args = list(kwargs["rgb"])
			if len(args) >= 3:
				args = args[0:3]
			else:
				while len(args) < 3:
					args.append(None)
					
			for i in range(0,3):
				if type(args[i]) != int:
					rgb.append(rgbrandoms[i])
				else:
					rgb.append(args[i])
			return Color(rgb=rgb)
			
		if "hsl" in kwargs.keys():
			hsl = []
			args = list(kwargs["hsl"])
			if len(args) >= 3:
				args = args[0:3]
			else:
				while len(args) < 3:
					args.append(None)
					
			for i in range(0,3):
				if type(args[i]) != int:
					hsl.append(hsxrandoms[i])
				else:
					hsl.append(args[i])
			return Color(hsl=hsl)
			
		if "hsv" in kwargs.keys():
			hsv = []
			args = list(kwargs["hsv"])
			if len(args) >= 3:
				args = args[0:3]
			else:
				while len(args) < 3:
					args.append(None)
					
			for i in range(0,3):
				if type(args[i]) != int:
					hsv.append(hsxrandoms[i])
				else:
					hsv.append(args[i])
			return Color(hsv=hsv)
			
			
	def hsvgradient(self, target, steps):
		""" Returns a list of colors from self to target of length steps that gradually blends through the hsv colorspace"""
		out = [deepcopy(self)]
		h, s, v = out[0].hsv
		hstep = max(h, target.h) - min(h, target.h)
		hstep /= steps
		sstep = max(s, target.s) - min(s, target.s)
		sstep /= steps
		vstep = max(v, target.v) - min(v, target.v)
		vstep /= steps
		
		for x in range(0, steps):
			
			if h < target.h:
				h += hstep
			elif h > target.h:
				h -= hstep
			
			if s < target.s:
				s += sstep
			elif s < target.s:
				s -= sstep
				
			if v < target.v:
				v += vstep
			elif v < target.v:
				v -= vstep
			
			out.append(Color(hsv=[h, s, v]))
		out[-1] = Color(hsv=target.hsv)
		return out
				
	def gradient(self, target, steps):
		out = [deepcopy(self)]
		r,g,b = out[0].rgb
		rstep = max(r, target.r) - min(r, target.r)
		rstep /= steps
		gstep = max(g, target.g) - min(g, target.g)
		gstep /= steps
		bstep = max(b, target.b) - min(b, target.b)
		bstep /= steps
		
		for x in range(0, steps):
			
			if r < target.r:
				r += rstep
			elif r > target.r:
				r -= rstep
			
			if g < target.g:
				g += gstep
			elif g > target.g:
				g -= gstep
				
			if b < target.b:
				b += bstep
			elif b > target.b:
				b -= bstep
			
			out.append(Color(rgb=[r,g,b]))
		out[-1] = Color(rgb=target.rgb)
		print("from", self, "to", target, "last", out[-1])
		return out
		
			
	@property
	def compl(self):
		""" Returns the complementaru color
		"""
		c = Color(self._r, self._g, self._b, a=self._a)
		c.h += 180
		return c
		
	@property
	def split_compl(self):
		""" Returns list containing 3 colors
		[complement with hue rotated -90°, original color, comlement with hue rotated 30°] """
		l = self.l
		out = [deepcopy(self.compl), deepcopy(self), deepcopy(self.compl)]
		out[0].h -= 30
		out[2].h += 30
		return out
	
	@property
	def analagous(self):
		""" Returns a list of the color and its analagous colors """
		out = [deepcopy(self), deepcopy(self), deepcopy(self)]
		out[0].h -= 30
		out[2].h += 30
		return out
	
	@property
	def triadic(self):
		""" Returns a list of the color and its triadic harmonies """
		out = [deepcopy(self), deepcopy(self), deepcopy(self)]
		out[0].h -= 120
		out[2].h += 120
		return out
		
	@property
	def tetradic(self):
		""" Returns a list of the color and its tetriadic harmonies """
		out = [deepcopy(self), deepcopy(self), deepcopy(self), deepcopy(self)]
		out[0].h -= 60
		out[2].h += 120
		out[3].h += 180
		return out
		
	@property
	def hsv(self):
		""" Calculates and returns Hue, Saturation, Value from the colors RGB values """
		r, g, b = self._r/255.0, self._g/255.0, self._b/255.0
		mx = max(r, g, b)
		mn = min(r, g, b)
		df = mx-mn
		if mx == mn:
		   h = 0
		elif mx == r:
		   h = (60 * ((g-b)/df) + 360) % 360
		elif mx == g:
		   h = (60 * ((b-r)/df) + 120) % 360
		elif mx == b:
		   h = (60 * ((r-g)/df) + 240) % 360
		if mx == 0:
		   s = 0
		else:
		   s = (df/mx)*100
		   
		v = mx*100
		return round(h, 2), round(s,2), round(v,2)
	
	@hsv.setter
	def hsv(self, value: list):
		""" converts a list of h,s,v to rgb and sets the colors rgb to it """
		self.h, self.s, self.v = value[0], value[1], value[2]
		
	@property
	def hsl(self):
	   """ Calculates and returns Hue, Saturation, Luminosity from the colors RGB values """
	   return hsv_to_hsl(*self.hsv)
	
	@hsl.setter
	def hsl(self, value):
	   """ converts a list of h,s,l to rgb and sets the colors rgb to it """
	   print("Setting", value)
	   self.h, self.s, self.l = value[0], value[1], value[2]
	   
	   
	@property
	def r(self):
		""" The colors Red channel """
		return self._r
	
	@r.setter
	def r(self, value):
		""" Sets the colors Red channel """
		if type(value) == int:
			if value > self.range:
				value = self.range
			if value < 0:
				value = 0
			self._r = value
		elif type(value) == float:
			if value > self.range:
				value = float(self.range)
			if value < 0:
				value = 0.0
			self._r = round(self.range*value)
		
	@property
	def g(self):
		""" The colors Green channel """
		return self._g
	
	@g.setter
	def g(self, value):
		""" Sets colors Green channel """
		if type(value) == int:
			if value > self.range:
				value = self.range
			if value < 0:
				value = 0
			self._g = value
		elif type(value) == float:
			if value > self.range:
				value = float(self.range)
			if value < 0:
				value = 0.0
			self._g = round(self.range*value)
		
	@property
	def b(self):
		""" The colors Blue channel """
		return self._b
	
	@b.setter
	def b(self, value):
		""" Sets the colors Blue channel """
		if type(value) == int:
			if value > self.range:
				value = self.range
			if value < 0:
				value = 0
			self._b = value
		elif type(value) == float:
			if value > range:
				value = float(self.range)
			if value < 0:
				value = 0.0
			self._b = round(self.range*value)
	
	@property
	def h(self):
		""" The colors Hue in degrees 0-360 """
		return self.hsl[0]
	
	@h.setter
	def h(self, value):
		""" Sets the colors hue """
		value = value % 360
		self._r, self._g, self._b= hsl_to_rgb(value, self.s, self.l)
	
	@property
	def s(self):
		""" The colors saturation in %, 0-100 """
		return  self.hsl[1]
		
	@s.setter
	def s(self, value):
		""" Sets the colors saturation """
		value = value%100
		self._r, self._g, self._b= hsl_to_rgb(self.h, value, self.l)
	
	@property
	def l(self):
		""" The colors luminosity in %, 0-100"""
		return self.hsl[2]
		
	@l.setter
	def l(self, value):
		""" Sets the colors luminosity """
		self.clamp()
		value = value
		if value <= 0:
			value = 0.01
		elif value >= 100:
			value = 99.99
		self._r, self._g, self._b= hsl_to_rgb(self.h, self.s, value)
	
	@property
	def v(self):
		""" The colors value or brightness in % 0-100 """
		return self.hsv[2]
		
	@v.setter
	def v(self, value):
		""" Sets the colors value/brightness """
		value = value%100
		self._r, self._g, self._b= hsv_to_rgb(self.h, self.s, value)
		
	@property
	def a(self):
		""" The colors alpha channel """
		return self._a
	
	@a.setter
	def a(self, value):
		""" Sets the colors alpha value """
		if type(value) == int:
			if value > self.range:
				value = self.range
			if value < 0:
				value = 0
			self._a = value
		elif type(value) == float:
			if value > self.range:
				value = float(self.range)
			if value < 0:
				value = 0.0
			self._a = round(255*value)
		
		
	def clamp(self):
		""" ensures that r, g, b, a are within range """
		self.r = int(self._r)
		self.g = int(self._g)
		self.b = int(self._b)
		self.a = int(self._a)
		return 
		if preserve:
			m = max(self._r, self._g, self._b)
			self._r /= m
			self._g /= m
			self._b /= m
			prev = self._range
			self._range = 1
			self.range = prev
			return 
				
		
			
		if self._r > self.range:
			self._r = self.range
		elif self._r < 0:
			self._r = 0
			
		if self._g > self.range:
			self._g = self.range
		elif self._g < 0:
			self._g = 0
			
		if self._b > self.range:
			self._b = self.range
		elif self._b < 0:
			self._b = 0
			
		if self._a > self.range:
			self._a = self.range
		elif self._a < 0:
			self._a = 0
			
	@property
	def range(self):
		""" not fully implemented, range of rgba values default 0-255 """
		return self._range
		
	@range.setter
	def range(self, value):
		""" not fully implemented set rgba range"""
		self._r = round((self._r/self._range)*value)
		self._g = round((self._g/self._range)*value)
		self._b = round((self._b/self._range)*value)
		self._a = round((self._a/self._range)*value)
		self._range = value
			
		
	
	@property
	def hex4(self):
		""" Returns a hexidecimal string of the color including the alpha channel """
		self.clamp()
		red = hex(self.r).replace("x", "")
		if len(red) > 2:
			red = red[1:]
		green = hex(self.g).replace("x", "")
		if len(green) > 2:
			green = green[1:]
		blue = hex(self.b).replace("x", "")
		if len(blue) > 2:
			blue = blue[1:]
		alpha = hex(self.a).replace("x", "")
		if len(alpha) > 2:
			alpha = alpha[1:]
		return f"#{red}{green}{blue}{alpha}"
	
	def __add__(self, value):
		""" add a color, list or int to the color 
		colors add the rgb to the rgb of self
		lists add their values to the channel  corresponding to their index
		ints add the integer to all channels"""
		self.clamp()
		if type(value) == list:
			if len(value) > 4 or len(value) < 1:
				raise ValueError("Not enough values to add")
			while len(value) < 4:
				if len(value) == 3:
					value.append(255)
				else:
					value.append(0)
			return Color(self._r+value[0], self._g+value[1], self._b+value[2], self._a+value[3])
			
		return Color(self._r+value, self._g+value, self._b+value, self._a)
	
	def __str__(self):
		""" returns the hex representation of the color """
		return f"{self.hex}"
		
	def __repr__(self):
		""" returns a stringified constructor of the color """
		return f"Color({self.r}, {self.g}, {self.b}, {self.a})"
	
	@property
	def name(self):
		""" gets the name of the color from the desired space """
		for k, i in self.space.items():
			try:
				if i["hex"].replace("0x", "#") == self.hex:
					self._name = k
					return self._name
			except Exception as e:
				print(e)
		
			self._name = self.closest(Colors16)._name
		return self._name
		
	@property
	def hex(self):
		""" returns the hexidecimal string of the color ignoring alpha """
		return self.hex4[:-2]
		
	@property
	def rgb(self):
		""" returns a tuple of the colors r, g and b values """
		return self.r, self.g, self.b
	
	@rgb.setter
	def rgb(self, value:list):
		""" set the colors r, g and b values in accordance to a list, or integer similar to the rgb keyword in __init__ """
		if type(value) == float:
			value = self._range*abs(value%1)
			r,g,b = value, value, value
		elif type(value) == int:
			value = value * self.range
			r, g, b = value, value, value
		elif type(value) in (list, tuple):
			value = list(value)
			l = len(value)
			if l == 0:
				r, g, b = self._r, self._g, self._b
			elif l == 1:
				r, g, b = value[0], self._g, self._b
			elif l == 2:
				r, g, b = value[0], value[1], self._b
			elif l == 3:
				r, g, b = value[0], value[1], value[2]
			else:
				raise ValueError(f"Too many values. max 3, got {l}")
		else:
			raise ValueError(f"rgb must be int, float, list or tuple not {type(value)}")
		self._r, self._g, self._b = r, g, b
	
	@property
	def rgba(self):
		""" Returns a list of the colors r, g, b and a channels """
		return self.r, self.g, self.b, self.a
		
	def palette(self, length=3, function=uniform_random, **kwargs):
		""" Returns a list of colors following a pattern created by the function """
		
		out = [deepcopy(self)]
		last = deepcopy(self)
		for i in range(0, length):
			col = function(last, length = length, i = i, **kwargs)
			out.append(Color(*col, a=last.a))
			last = out[-1]
		return out
			
	
	@rgba.setter
	def rgba(self, value):
		""" set the colors r, g, b and a values in accordance to a list, or integer similar to the rgba keyword in __init__ """
		if type(value) == int:
			self._a = value
			self.rgb = value
		elif type(value) == float:
			self.rgb = value
			self._a = value*abs(value*self._range)%self._range
		elif type(value) in (list, tuple):
			value = list(value)
			if len(value) >= 0 and len(value) <=4:
				newvalue = [self._r, self._g, self._b, self._a]
				for i, val in enumerate(value):
					value[i] = val
				self.rgb = value[0:3]
				self._a = value[3]
			else:
				raise ValueError(f"Too many values. max 4, got {len(value)}")
		else:
			raise ValueError(f"rgb must be int, float, list or tuple not {type(value)}")
				
		
	def __sub__(self, value):
		""" subtracts a color/list of rgb values/integer from the color inversely to __add__ """
		self.clamp()
		if type(value) == list:
			if len(value) > 4 or len(value) < 1:
				raise ValueError("Not enough values to add")
			while len(value) < 4:
				if len(value) == 3:
					value.append(255)
				else:
					value.append(0)
			return Color(self._r-value[0], self._g-value[1], self._b-value[2], self._a-value[3])
			
		return Color(self._r-value, self._g-value, self._b-value, self._a)
		
	def __mul__(self, value):
		""" Multiplies the r, g, and b values by a list of rgb values, a color or an integer """
		self.clamp()
		if type(value) == list:
			if len(value) > 4 or len(value) < 1:
				raise ValueError("Not enough values to add")
			while len(value) < 4:
				if len(value) == 3:
					value.append(255)
				else:
					value.append(1)
			return Color(self._r*value[0], self._g*value[1], self._b*value[2], self._a*value[3])
			
		return Color(self._r*value, self._g*value, self._b*value, self._a)
		
	def __div__(self, value):
		""" Divides the r, g, and b values by a list of rgb values, a color or an integer """
		self.clamp()
		if type(value) == list:
			if len(value) > 4 or len(value) < 1:
				raise ValueError("Not enough values to add")
			while len(value) < 4:
				value.append(1)
			return Color(self._r/value[0], self._g/value[1], self._b/value[2], self._a/value[3])
			
		return Color(self._r/value, self._g/value, self._b/value, self._a)
		
	def text(self, text, rgb=None):
		""" Returns a colored string using ansi escape sequences """
		
		if rgb == None:
			rgb = self.rgb
		r,g,b = rgb[0], rgb[1], rgb[2]
		
		if self.is_shade_of_white():
			prime = self.closest(Colors16[0:3])
			if prime == Black:
				base = 30
			elif prime == Grey:
				base = 37
			elif prime == White:
				base = 97
				
		elif (r+g+b)/3 >= 128:
			base = 90
			prime = self.closest(LColors).rgb
			if prime == LRed:
				base += 1
			elif prime == LGreen:
				base += 2
			elif prime == LYellow:
				base += 3
			elif prime == LBlue:
				base += 4
			elif prime == LPurple:
				base += 5
			elif prime == LCyan:
				base += 6
			else:
				raise ValueError("Something fucked up")
				
		else:
			base = 30
			prime = self.closest(Colors).rgb
			if prime == Red:
				base += 1
			elif prime == Green:
				base += 2
			elif prime == Yellow:
				base += 3
			elif prime == Blue:
				base += 4
			elif prime == Purple:
				base += 5
			elif prime == Cyan:
				base += 6
			else:
				raise ValueError("Something fucked up")
				
		col = base
		return f"\033[{col}m{text}\033[0m"
		
	def is_shade_of_white(self):
		""" returns True if r == g == b """
		if self.r == self.g and self.g == self.b:
			return True
		return False
	
	def distance(self, other):
		""" returns the distance between two colors rgb values """
		if type(other) in (list, tuple):
			otherr = other[0]
			otherg = other[1]
			otherb = other[2]
		else:
			otherr, otherg, otherb = other.rgb
			
		rdistance = abs(otherr - self.r)
		gdistance = abs(otherg - self.g)
		bdistance = abs(otherb - self.b)
		
		
		return (rdistance + gdistance + bdistance)/3
		
	def __eq__(self, other):
		""" Returns True if self and other are equivelent """
		if self is other:
			return True
			
		if type(other) in (list, tuple):
			other = Color(rgb=other)
			
		if self.r == other.r and self.g == other.g and self.b == other.b:
			return True
		return False
		
	def closest(self, colors = 16):
		""" returns the closest color to self out of the supplied list. if no list is given it will default to the 16 terminal colors """
		reconstruct = False
		names = []
		if colors == 16:
			colors = Colors16
		if colors == None:
			colors = []
			reconstruct = True
			for k, i in self.space.items():
				colors.append(i["rgb"])
				names.append(k)
		distances = [self.distance(col) for col in colors]
		m = min(*distances)
		
		for i, distance in enumerate(distances):
			if distance == m:
				if reconstruct:
					out = Color(rgb=colors[i])
					out._name = names[i]
					return out
				return colors[i]
	
	def __neg__(self):
		return self.compl
	
	def __len__(self):
		return self.r + self.g + self.b
	
	@property
	def nprgb(self):
		""" returns the colors rgb values as a numpy array """
		if not numpy_enabled:
			return self.rgb
		return np.array(self.rgb)
	
	@property
	def nprgba(self):
		""" returns the colors rgba values as a numpy array """
		if not numpy_enabled:
			return self.rgba
		return np.array(self.rgba)
		
	@property
	def nphsv(self):
		""" returns the colors hsv values as a numpy array """
		if not numpy_enabled:
			return self.hsv
		return np.array(self.hsv)
	
	@property
	def nphsl(self):
		""" returns the colors hsl values as a numpy array """
		if not numpy_enabled:
			return self.hsl
		return np.array(self.hsl)
#"C:/Users/Y0L0S.DESKTOP-LE6HALS/Documents/ezcolors/src/ezcolors/names.json"
with open("/".join(__file__.split("/")[0:-1]) + "/names.json") as f:
	string = ""
	for line in f:
		string += line
	wiki = json.loads(string)
	del string


def string_to_color(string, space="wiki:"):
	""" returns a Color from a given hex value or color name """
	string = string.lower()
	is_hex = False
	if len(string) >= 2:
		if string[0] == "#" or string[0:2] == "0x":
			if string[0] == "#":
				string = string[1:]
			else:
				string = string[2:]
			#print(string)
			for char in string:
				if char not in ("0","1","2","3","4","5","6","7","8","9", "a", "b", "c", "d", "e", "f"):
					is_hex = False
					break
				is_hex = True
	if is_hex:
		if len(string) in (3, 4, 6, 8):
			if len(string) == 3:
				r = string[0] + string[0]
				g = string[1] + string[1]
				b = string[2] + string[2]
				a = "ff"
			elif len(string) == 4:
				r = string[0]
				g = string[1]
				b = string[2]
				a = string[3]
			elif len(string) == 6:
				r = string[0:2]
				g = string[2:4]
				b = string[4:6]
				a = "ff"
			elif len(string) == 8:
				r = string[0:2]
				g = string[2:4]
				b = string[4:6]
				a = string[6:8]
				
			r = int(f"0x{r}", 16)
			g = int(f"0x{g}", 16)
			b = int(f"0x{b}", 16)
			a = int(f"0x{a}", 16)
			return Color(r, g, b, a)
		else:
			raise ValueError("Invalid hex. must be rgb, rgba, rrggbb or rrggbbaa")
	else:
		if space in (web, "web", "Web", 0):
			space = web
		elif space in (wiki, "wiki", "Wiki", 1):
			space = wiki
		elif space in ("x11", "X11", 2):
			pass
		elif space in ("terminal", "Terminal", 3):
			pass
		elif space in ("all", "All", -1):
			pass
		else:
			raise ValueError(f"Invalid Color Space {space}")
			
		closest = ""
		for k, i in space.items():
			k = k.replace("_", " ")
			if textdistance.hamming.normalized_similarity(string, k) > textdistance.hamming.normalized_similarity(string, closest):
				closest = k
				if type(closest) != str:
					closest = closest["hex"]
				#print("closest", closest)
				
		if type(closest) != str:
			closest = closest["hex"]
		#print("Closest:", closest, space[closest])
		if type(space[closest]) == str:
			return string_to_color(space[closest])
		elif type(space[closest]) == dict:
			return string_to_color(space[closest]["hex"])

Black = Color(0, 0, 0, name = "Black")
Grey = Color(128, 128, 128, name="Grey")
White = Color(255, 255, 255, name="White")
Red = Color(128,0,0, name="Red")
Green = Color(0, 128, 0, name="Green")
Yellow = Color(128, 128, 0, name="Yellow")
Blue = Color(0, 0, 128, name="Blue")
Purple = Color(128, 0, 128, name="Purple")
Cyan = Color(0, 128, 128, name="Cyan")
LRed = Color(255,128, 128, name="Light Red")
LGreen = Color(128, 255, 128, name="Light Green")
LYellow = Color(255, 255, 128, name="Light Yellow")
LBlue = Color(128, 128, 255, name="Light Blue")
LPurple = Color(255, 125, 255, name="Light Purple")
LCyan = Color(128, 255, 255, name="Light Cyan")
Colors16 = [Black, Grey, White, Red, Green, Yellow, Blue, Purple, Cyan, LRed, LGreen, LYellow, LBlue, LPurple, LCyan]
Colors = Colors16[3:9]
LColors = Colors16[9:]

def avg_color(colors: list):
	""" returns the average color of the list of colors given """
	r = 0
	g = 0
	b = 0
	for c in colors:
		if type(c) in (list, tuple):
			c = list(c)
			while len(c) < 3:
				c.append(0)
			r += c[0]
			g += c[1]
			b += c[2]
		elif c.__class__ == Color:
			r += c.r
			g += c.g
			b += c.b
		elif type(c) == str:
			c = Color(c)
			r += c.r
			g += c.g
			b += c.b
		elif type(c) in (int, float):
			c = int(c)
			r += c
			g += c
			b += c
	r /= len(colors)
	g /= len(colors)
	b /= len(colors)
	return Color(r, g, b)
	
