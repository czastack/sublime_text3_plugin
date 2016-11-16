from ctypes import cdll, Structure, c_int, c_char_p, POINTER, create_string_buffer
import os

class SassResult(Structure):
	_fields_ = [
		("success", c_int),
		("content", c_char_p),
	]

class SassHelper:

	def __init__(self):
		self.clib = None

	def _load(self):
		"""Loads the libsass library if it isn't already loaded."""
		if self.clib is None:
			curdir = os.path.dirname(__file__)
			
			import platform
			if platform.system() == 'Windows':
				libname = 'sasshelper_win32.dll' if platform.architecture()[0].startswith('32') else 'sasshelper.dll'
				libname = os.path.join(curdir, libname)
			else:
				libname = os.path.join(curdir, 'sasshelper.so')

			libpath = os.path.join(curdir, libname)

			if os.path.exists(libpath):
				self.clib = cdll.LoadLibrary(libpath)
			else:
				raise Exception("Could not load library")

			self.clib.set_include_path.argtypes = [c_char_p]
			self.clib.set_include_path.restype = None

			self.clib.sass_compile_string.argtypes = [c_char_p, c_char_p]
			self.clib.sass_compile_string.restype = POINTER(SassResult)

			self.clib.sass_compile_file.argtypes = [c_char_p]
			self.clib.sass_compile_file.restype = POINTER(SassResult)

			self.clib.free_result.argtypes = None
			self.clib.free_result.restype = None



	def __getattribute__(self, name):
		attr = object.__getattribute__(self, name)
		if hasattr(attr, '__call__') and name != "_load":
			def load_wrapper(*args, **kwargs):
				self._load()
				return attr(*args, **kwargs)
			return load_wrapper
		else:
			return attr

	def set_include_path(self, path):
		p = create_string_buffer(path.encode())
		self.clib.set_include_path(p)

	def compile_string(self, text, path = ''):
		text = create_string_buffer(text.encode())
		path = create_string_buffer(path.encode())
		return self.clib.sass_compile_string(text, path)

	def compile_file(self, file):
		p = create_string_buffer(file.encode())
		return self.clib.sass_compile_file(p)

	def free_result(self):
		self.clib.free_result()

if __name__ == '__main__':
	helper = SassHelper()
	print(helper.compile_string('$fontSize: 12px;\nbody{\nfont-size:$fontSize;\n}').contents.content.decode())