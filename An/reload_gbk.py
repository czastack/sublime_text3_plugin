import sublime, sublime_plugin

class ReloadGbkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file_name = self.view.file_name()
		if file_name:
			with open(file_name, 'r', encoding='GBK') as f:
				self.view.replace(edit, sublime.Region(0, self.view.size()), f.read())
