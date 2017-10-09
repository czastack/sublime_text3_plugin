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


def mixColor(c1, c2):
    """ 混合两种RRGB颜色
    print(hex(mixColor(0xee8b83, 0x83aadc)))
    """
    r = int(((c1 >> 16) + (c2 >> 16)) / 2 + 0.5)
    g = int((((c1 >> 8) & 0xFF) + ((c2 >> 8) & 0xFF)) / 2 + 0.5)
    b = int(((c1 & 0xFF) + (c2 & 0xFF)) / 2 + 0.5)
    return (r << 16) | (g << 8) | b
