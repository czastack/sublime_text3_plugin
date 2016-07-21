import sublime_plugin
from An import an

class SetTextCommand(sublime_plugin.TextCommand):
	def run(self, edit, text):
		an.set(self.view, edit)
		an.text(text);
		self.view.selection.clear()
