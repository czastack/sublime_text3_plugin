import sublime_plugin
from An import an

class SelectToArrayCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		data = []
		for region in self.view.selection:
			data.append(self.view.substr(region))
		an.tmp = data
