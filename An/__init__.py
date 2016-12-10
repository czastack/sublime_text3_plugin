if __name__ == 'An':
	import os, sys
	sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
	del os, sys

	from subl import An
	an = An()
else:
	def plugin_loaded():
		from An import an
		an.onload()