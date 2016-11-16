import re, sublime, sublime_plugin
from An import An, an

class BaseSelect(sublime_plugin.TextCommand):
	def set_regions(self, regions):
		self.view.selection.clear()
		self.view.selection.add_all(regions)

# 选中所选部分中符合指定正则表达式的内容
class SelectReg(BaseSelect):
	flags = re.M
	def run(self, edit):
		view = self.view
		regions = []
		sel_len = len(view.selection)
		if sel_len == 0 or (sel_len == 1 and view.selection[0].empty()):
			selection = [An.region(view)]
		else:
			selection = view.selection
		for region in selection:
			pt = region.begin()
			text = view.substr(region)
			for m in re.finditer(self.reg, text, self.flags):
				span = m.span()
				regions.append(sublime.Region(span[0] + pt, span[1] + pt))
		self.set_regions(regions)

# # 快速选中所有行首
# class SelectLineStartCommand(BaseSelect):
# 	def run(self, edit):
# 		regions = An.lines(self.view)
# 		for region in regions:
# 			region.b = region.a
# 		self.set_regions(regions)

# # 快速选中所有行尾
# class SelectLineEndCommand(BaseSelect):
# 	def run(self, edit):
# 		regions = An.lines(self.view)
# 		for region in regions:
# 			region.a = region.b
# 		self.set_regions(regions)

# # 快速选中所有行
# class SelectLineAllCommand(BaseSelect):
# 	def run(self, edit):
# 		regions = An.lines(self.view)
# 		self.set_regions(regions)

# 快速选中所有行首
class SelectLineStartCommand(SelectReg):
	reg = '^'

# 快速选中所有行尾
class SelectLineEndCommand(SelectReg):
	reg = '$'

# 快速选中所有行
class SelectLineAllCommand(SelectReg):
	reg = '.+'

# 选中空行
class SelectEmptyLinesCommand(SelectReg):
	reg = '\n[ \t]*(?=\n|$)'

# 选中行结尾的空白字符
class SelectLineEndSpaceCommand(SelectReg):
	reg = '[ \t]+(?=\n|$)'
	

# 按长度分隔选区
class SplitSelectByLenCommand(BaseSelect):
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
class SplitSelectByRegCommand(BaseSelect):
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
class SelectStartToEndCommand(BaseSelect):
	def run(self, edit):
		regions = [sublime.Region(region.b, region.a) for region in self.view.selection]
		self.set_regions(regions)

# 交换两个选区的内容
class ExchangeSelectCommand(BaseSelect):
	def run(self, edit):
		if len(self.view.selection) == 2:
			view = self.view
			tmp = view.substr(view.selection[0])
			view.replace(edit, view.selection[0], view.substr(view.selection[1]))
			view.replace(edit, view.selection[1], tmp)

# 选中引号外侧/内侧
class SelectionQuoteCommand(BaseSelect):
	def run(self, edit):
		view = self.view
		regions = []
		for region in view.selection:
			desc = region.a > region.b
			if desc:
				region.a, region.b = region.b, region.a

			quote = view.substr(region.begin())
			if quote in '\'"':
				# deflate 缩小
				inflate = False
			else:
				quote = view.substr(region.begin() - 1)
				if quote in '\'"':
					# inflate 扩充
					inflate = True
				else:
					quote = None
			if quote:
				da, db = (-1, 1) if inflate else (1, -1)
				if inflate:
					while view.substr(region.a + da) == quote:
						region.a += da
					while view.substr(region.b) == quote:
						region.b += db
				else:
					while view.substr(region.a) == quote:
						region.a += da
					while view.substr(region.b + db) == quote:
						region.b += db
				if desc:
					region.a, region.b = region.b, region.a
				regions.append(region)
		if regions:
			self.set_regions(regions)

# 选中每两个光标中间的区域（列模式）
class SelectMiddleCommand(BaseSelect):
	def run(self, edit, sort_by_col = False):
		view = self.view
		regions = []
		selection = list(self.view.selection)
		if sort_by_col:
			# 横向扫描
			selection = sorted(selection, key=lambda s: view.rowcol(s.a)[1])
		if len(selection) & 1:
			selection.pop()
		itr = iter(selection)
		for region in itr:
			aa, ab = view.rowcol(region.a)
			ba, bb = view.rowcol(next(itr).a)
			while aa <= ba:
				a = view.text_point(aa, ab)
				b = view.text_point(aa, bb)
				if view.rowcol(a) == (aa, ab):
					if view.rowcol(b) != (aa, bb):
						# 这行不够长
						b = view.text_point(aa + 1, 0) - 1
					regions.append(sublime.Region(a, b))
				aa += 1
		self.set_regions(regions)