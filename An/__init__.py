import sublime, sys

class An:
	def set(self, view, edit):
		self.view = view
		self.edit = edit

		edit.an = self
		edit.view = view
		edit.sublime = sublime

	def show_output(self, text=None):
		win = sublime.active_window()
		if not self.output:
			self.output = win.create_output_panel('an')
			self.output.settings().set('color_scheme', self.view.settings().get('color_scheme'))
		
		if text is not None:
			if not isinstance(text, str):
				text = str(text)
			self.output.run_command('set_text', {'text': text})
		
		win.run_command('show_panel', {'panel': 'output.an'})

	# show_output的别名
	def tout(self, text=None):
		self.show_output(text)

	def cls(self):
		if self.output:
			self.output.run_command('clear_text')

	def echo(self, *args, **dictArgs):
		dictArgs['file'] = self
		print(*args, **dictArgs)

	#作为print file参数
	def flush(self):
		pass

	def write(self, s):
		if self.output:
			self.output.run_command('append', {"characters": s});

	def _exec(self, text):
		try:
			exec(text, self.edit.__dict__)
			return True
		except Exception as e:
			logerr(e)
			return False

	def _eval(self, text):
		try:
			self.edit._ret = eval(text, self.edit.__dict__)
			return True
		except Exception as e:
			logerr(e)
			return False

	# 获取设置文本
	def text(self, text = None):
		if text is not None:
			if not isinstance(text, str):
				text = str(text)
			self.view.replace(self.edit, __class__.region(self.view), text)
		else:
			return self.view.substr(__class__.region(self.view))

	def view_selected_text(view):
		texts = []
		for region in view.selection:
			if region.empty():
				region = view.line(region.a)
			texts.append(view.substr(region))
		return texts

	def selected_text(self):
		return view_selected_text(self.view)

	def popup(self, text, **args):
		self.view.show_popup('<style>body{margin:0; padding:10px; color:#ccc; font-size:18px; background-color:#000;}</style>' + text, **args);

	def open_file(self, file):
		sublime.active_window().open_file(file)

	def __getattr__(self, name):
		return None

	# 静态方法
	def region(view):
		return sublime.Region(0, view.size())

	def lines(view):
		return view.lines(__class__.region(view))

an = An()

# 打印错误
def logerr(e):
	print(type(e).__name__ + ': ' + str(e), file=an)

# 是否是列表或元组
def is_list_or_tuple(var):
	return isinstance(var, list) or isinstance(var, tuple)

# 生成字符序列
def strsq(a, b, split = ''):
	def check_param(ch):
		ok = False
		if isinstance(ch, str):
			if len(ch) == 1:
				ch = ord(ch)
				ok = True
		elif isinstance(ch, int):
			ok = True
		if ok:
			return ch
		else:
			raise ValueError('参数必须是字符或者整数')
	a = check_param(a)
	b = check_param(b)
	if a > b:
		a, b = b, a
	sq = (chr(x) for x in range(a, b + 1))
	return split.join(sq) if isinstance(split, str) else sq

def add_path(*args):
	for x in args:
		if x not in sys.path:
			sys.path.append(x)

def sublime_path():
	import os
	return os.path.dirname(sublime.__file__)

def default_packages_path():
	import os
	return os.path.join(sublime_path(), 'packages')

add_path(sublime_path() + '\\pyext')