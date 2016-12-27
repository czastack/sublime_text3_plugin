
class ViewWriter:
	__slots__ = ('view')

	def __init__(self, view):
		self.view = view

	def flush(self):
		pass

	def write(self, s):
		self.view.run_command('append', {"characters": s})

	def cls(self):
		self.view.run_command('clear_text')