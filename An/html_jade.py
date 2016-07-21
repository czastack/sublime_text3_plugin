import sublime_plugin

class HtmlJadeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		import pyjade
		for region in self.view.selection:
			if not region.empty():
				self.view.replace(edit, region, pyjade.simple_convert(self.view.substr(region)))