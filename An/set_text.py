import sublime, sublime_plugin
from An import An

class SetTextCommand(sublime_plugin.TextCommand):
	def run(self, edit, text):
		self.view.replace(edit, An.region(self.view), text);
		self.view.selection.clear()
