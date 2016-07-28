class Color:
	def __init__(self, r=0, g=0, b=0, a=1):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def __str__(self):
		return self.toRgb()

	def toRgb(self, alpha = False):
		return ("rgba({r}, {g}, {b}, {a})" if alpha else rgb({r}, {g}, {b})).format(**self.__dict__)

	def toTuple(self, alpha = False):
		return (self.r, self.g, self.b, self.a) if alpha else (self.r, self.g, self.b)

	def toHex(self, alpha = False):
		tpl = "#{r:02X}{g:02X}{b:02X}"
		if alpha:
			tpl += "{a:02X}"
		return tpl.format(**self.__dict__)

	def toHalfHex(self):
		h = lambda c: (c & 0xF0) >> 4
		return "#{r:X}{g:X}{b:X}".format(r=h(self.r), g=h(self.g), b=h(self.b))