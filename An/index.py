import sublime, sublime_plugin
from An import An, an, logerr, is_list_or_tuple
from type import astr

# 清空内容
class ClearTextCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.erase(edit, An.region(self.view))

# 执行当前文件内的语句
#self.view.window().run_command('show_panel', {"panel": "console"})
class ExecDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		an.set(self.view, edit)
		an._exec(an.text())

# 执行选中的语句
class ExecSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		an.set(self.view, edit)
		for region in self.view.selection:
			if region.empty():
				region = self.view.line(region.a)
			edit._ret=None
			if an._exec(self.view.substr(region)) and edit._ret:
				self.view.replace(edit, region, str(edit._ret))

# 执行选中的表达式并替换当前文本
class EvalSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		an.set(self.view, edit)
		for region in self.view.selection:
			if not region.empty() and an._eval(self.view.substr(region)):
				self.view.replace(edit, region, str(edit._ret))

# 选择文字替换成表达式
class ToExprCommand(sublime_plugin.TextCommand):
	def run(self, edit, text = None):
		if text:
			self.on_exec(edit, text)
			return

		default = an.to_expr_last if an.to_expr_last else 'src'
		input_panel = self.view.window().show_input_panel('to expr', default, self.on_input_text, None, None)
		#选中默认文字
		input_panel.selection.add(An.region(input_panel));

	def on_input_text(self, text):
		an.to_expr_last = text
		self.view.run_command(self.name(), {"text": text})

	def on_exec(self, edit, text):
		an.set(self.view, edit)
		edit.i = 0
		for region in self.view.selection:
			edit.src=self.view.substr(region)
			edit.i += 1
			if(an._eval(text)):
				self.view.replace(edit, region, str(edit._ret))

# 插入列表
class InsertListCommand(sublime_plugin.TextCommand):
	def run(self, edit, text = None):
		if text:
			self.on_insert(edit, text)
			return

		#默认是插入数字
		default = an.insert_text_last if an.insert_text_last else '["%%01d" %% x for x in range(1, %d)]' % (len(self.view.selection) + 1)
		input_panel = self.view.window().show_input_panel('list expr', default, self.on_input_text, None, None)
		#选中默认文字
		input_panel.selection.add(An.region(input_panel));

	def on_input_text(self, text):
		an.insert_text_last = text
		self.view.run_command(self.name(), {"text": text})

	def on_insert(self, edit, text):
		an.set(self.view, edit)
		edit._ret = None
		edit._newline = True
		an._eval(text) or an._exec(text)
		if hasattr(edit._ret, '__len__'):
			selectionlen = len(self.view.selection)
			if selectionlen > 1:
				# 依次应用到光标
				itr = iter(edit._ret)
				i = 0
				for region in self.view.selection:
					if i == selectionlen:
						break
					else:
						i += 1
					cur = itr.__next__() # 当前要插入的文本
					if not isinstance(cur, str):
						cur = str(cur)
					self.view.replace(edit, region, cur)
			else:
				# 列表插入到当前位置
				regions = []
				i = 0
				itemlen = len(edit._ret)
				usetpl = False # 使用模板
				region = self.view.selection[0]
				if selectionlen == 1 and region.size() > 1 and self.view.substr(region.begin()) == '%':
					usetpl = True
					tpl = self.view.substr(sublime.Region(region.begin() + 1, region.end())) # 模板文字
				self.view.erase(edit, region)
				while i < itemlen:
					item = edit._ret[i]
					if not usetpl:
						item = astr(item)
					else:
						if is_list_or_tuple(item):
							argslen = len(item) # 当前参数的长度
							iscontainer = argslen > 0 and is_list_or_tuple(item[0])
							if iscontainer and argslen == 1:
								item = tpl.format(*item[0])
							elif iscontainer and argslen == 2:
								item = tpl.format(*item[0], **item[1])
							else:
								item = tpl.format(*item)
						elif isinstance(item, dict):
							item = tpl.format(**item) # 替换一个参数
						else:
							item = astr(item)
							item = tpl.format(item)
					cur = self.view.selection[-1].a
					regions.append(sublime.Region(cur, cur + len(item)))
					self.view.insert(edit, cur, item)
					i += 1
					if edit._newline and i < itemlen:
						self.view.run_command('insert', {"characters": "\n"});
				self.view.selection.clear()
				self.view.selection.add_all(regions)