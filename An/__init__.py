import sublime, sys
from os import path as Path

class An:
	def set(self, view, edit = None):
		self.view = view
		self.edit = edit
		if edit:
			edit.an = self
			edit.view = view

	def show_output(self, text=None):
		win = sublime.active_window()
		if not self.output:
			self.output = win.create_output_panel('an')
			self.output.settings().set('color_scheme', self.view.settings().get('color_scheme'))
		
		if text is not None:
			self.output.run_command('set_text', {'text': astr(text)})
		
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
			self.init_exec_env()
			exec(text, self.edit.__dict__)
			return True
		except Exception as e:
			logerr(e)
			return False

	def _eval(self, text):
		try:
			self.init_exec_env()
			self.edit._ret = eval(text, self.edit.__dict__)
			return True
		except Exception as e:
			logerr(e)
			return False

	def init_exec_env(self):
		self.edit.print = self.echo
		self.edit._print = print

	# 获取设置文本
	def text(self, text = None):
		if text is not None:
			self.view.replace(self.edit, __class__.region(self.view), astr(text))
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

	# 复制的数组（用换行分隔）
	@property
	def copied(self):
		return sublime.get_clipboard().split('\n')
	

	# 静态方法
	def region(view):
		return sublime.Region(0, view.size())

	def lines(view):
		return view.lines(__class__.region(view))

an = An()

# 打印错误
def logerr(e):
	print(type(e).__name__ + ': ' + str(e), file=an)

def add_path(*args):
	for x in args:
		if x not in sys.path:
			sys.path.append(x)

def sublime_path():
	return Path.dirname(sublime.__file__)

def default_packages_path():
	return Path.join(sublime_path(), 'packages')

add_path(Path.join(Path.dirname(__file__), 'lib'))
from type import astr