# 快速选中所有行首或者行尾

import sublime_plugin
from An import An, an

# 快速选中所有行首
class SelectLineStartCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = An.lines(self.view)
		for region in regions:
			region.b = region.a
		self.view.selection.clear()
		self.view.selection.add_all(regions)

# 快速选中所有行尾
class SelectLineEndCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = An.lines(self.view)
		for region in regions:
			region.a = region.b
		self.view.selection.clear()
		self.view.selection.add_all(regions)

# 快速选中所有行
class SelectLineAllCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = An.lines(self.view)
		self.view.selection.clear()
		self.view.selection.add_all(regions)