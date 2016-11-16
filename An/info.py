import sublime_plugin

class InfoCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		from An import an
		win = self.view.window()
		print("viewid:   ", self.view.id())
		print("windowid: ", win.id())
		print("panel:    ", win.active_panel())