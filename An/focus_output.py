import sublime_plugin
from An import an

class FocusOutputCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		an.view = self.view
		an.tout()
		if self.view == an.output:
			if an.last_group is not None:
				self.view.window().focus_group(an.last_group)
		else:
			an.last_group = self.view.window().active_group()
			self.view.window().focus_view(an.output)
