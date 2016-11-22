import sublime_plugin
from An import an

class FocusOutputCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		if self.view.view_id == an.output.view_id:
			if an.last_group is not None:
				self.view.window().focus_group(an.last_group)
		else:
			an.last_group = self.view.window().active_group()
			an.tout()
			self.view.window().focus_view(an.output)
