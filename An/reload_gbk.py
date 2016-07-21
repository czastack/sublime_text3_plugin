import sublime_plugin
from An import An

class ReloadGbkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file_name = self.view.file_name()
		if file_name:
			with open(file_name, 'r', encoding='GBK') as f:
				self.view.replace(edit, An.region(self.view), f.read())
