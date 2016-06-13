import sublime, sys

class An:
	def set(self, view, edit):
		self.view = view
		self.edit = edit

		edit.an = self
		edit.edit = edit
		edit.view = view
		edit.sublime = sublime

	def show_output(self):
		win = sublime.active_window()
		if not self.output:
			self.output = win.create_output_panel('an')
			self.output.settings().set('color_scheme', self.view.settings().get('color_scheme'))
		win.run_command('show_panel', {'panel': 'output.an'})

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

	def text(self):
		return self.view.substr(An.region(self.view))

	def view_selected_text(view):
		texts = []
		for region in view.selection:
			if region.empty():
				region = view.line(region.a)
			texts.append(view.substr(region))
		return texts

	def selected_text(self):
		return view_selected_text(self.view)

	def __getattr__(self, name):
		return None

	# 静态方法
	def region(view):
		return sublime.Region(0, view.size())

	def lines(view):
		return view.lines(An.region(view))

an = An()

# 打印错误
def logerr(e):
	print(type(e).__name__ + ': ' + str(e), file=an)

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