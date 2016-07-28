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
				path1 = 'sasshelper_win32.dll' if platform.architecture()[0].startswith('32') else 'sasshelper.dll'
				path1 = os.path.join(curdir, path1)
			else:
				path1 = os.path.join(curdir, 'sasshelper.so')

			oldir = os.getcwd()
			os.chdir(curdir)
			if os.path.exists(path1):
				self.clib = cdll.LoadLibrary(path1)
			else:
				raise Exception("Could not load library")
			os.chdir(oldir)

			self.clib.sass_compile_string.restype = POINTER(SassResult)
			self.clib.sass_compile_string.argtypes = [c_char_p]

			self.clib.sass_compile_file.restype = POINTER(SassResult)
			self.clib.sass_compile_file.argtypes = [c_char_p]

			self.clib.free_result.restype = None
			self.clib.free_result.argtypes = None

	def __getattribute__(self, name):
		attr = object.__getattribute__(self, name)
		if hasattr(attr, '__call__') and name != "_load":
			def load_wrapper(*args, **kwargs):
				self._load()
				return attr(*args, **kwargs)
			return load_wrapper
		else:
			return attr

	def compile_string(self, text):
		p = create_string_buffer(text.encode())
		return self.clib.sass_compile_string(p)

	def compile_file(self, file):
		p = create_string_buffer(text.encode())
		return self.clib.sass_compile_file(p)

	def free_result(self):
		self.clib.free_result()

_helper = SassHelper();
compile_string = _helper.compile_string
compile_file = _helper.compile_file