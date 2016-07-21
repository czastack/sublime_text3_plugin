# 快速选中所有行首或者行尾

import sublime, sublime_plugin
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

# 按长度分隔选区
class SplitSelectByLenCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# 显示输入框
		input_panel = self.view.window().show_input_panel('分隔长度', '', self.on_input_text, None, None)

	def on_input_text(self, text):
		regions = []
		step = int(text)
		if step > 0:
			for region in self.view.selection:
				if not region.empty():
					start = region.begin()
					end = region.end()
					i = start
					while i < end:
						regions.append(sublime.Region(i, min(i + step, end)))
						i += step
			if len(regions) > 0:
				self.view.selection.clear()
				self.view.selection.add_all(regions)

# 用正则表达式分隔选区
class SplitSelectByRegCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# 显示输入框
		input_panel = self.view.window().show_input_panel('分隔文本', '', self.on_input_text, None, None)

	def on_input_text(self, text):
		if text is not '':
			import re
			reg = re.compile(text)
			regions = []
			for region in self.view.selection:
				if not region.empty():
					pos = 0
					start = region.begin()
					end = region.end()
					itemtext = self.view.substr(region)
					while True:
						matcher = reg.search(itemtext, pos)
						if not matcher:
							break
						span = matcher.span()
						regions.append(sublime.Region(start + pos, start + span[0]))
						pos = span[1]

					if pos < end:
						 regions.append(sublime.Region(start + pos, end))
			if len(regions) > 0:
				self.view.selection.clear()
				self.view.selection.add_all(regions)

# 选区行尾互换
class SelectStartToEndCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = [sublime.Region(region.end(), region.begin()) for region in self.view.selection]
		self.view.selection.clear()
		self.view.selection.add_all(regions)

# 交换两个选区的内容
class ExchangeSelectCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if len(self.view.selection) == 2:
			view = self.view
			tmp = view.substr(view.selection[0])
			view.replace(edit, view.selection[0], view.substr(view.selection[1]))
			view.replace(edit, view.selection[1], tmp)