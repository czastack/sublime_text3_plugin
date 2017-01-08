import sublime_plugin
from subl.view import view_region

class SetTextCommand(sublime_plugin.TextCommand):
	def run(self, edit, text):
		self.view.replace(edit, view_region(self.view), text)
		self.view.selection.clear()
