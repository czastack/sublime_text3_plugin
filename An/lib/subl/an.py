import sublime, sublime_api, extypes

class An:
	__slots__ = ('_data', 'window_id')

	def __init__(self):
		self._data = {}
		self.attachWindow(0)

	def onload(self):
		self.attachWindow(sublime_api.active_window())

	def attachWindow(self, window_id):
		self.window_id = window_id
		self._data.setdefault(window_id, {})
		self._data[self.window_id].setdefault('globals', extypes.Map())

	def set(self, view, edit = None):
		self.attachWindow(sublime_api.view_window(view.view_id))
		self.view = view
		self.edit = edit
		if edit:
			edit.an = self
			edit.view = view

	def tout(self, text=None):
		win = sublime.Window(self.window_id)
		if not self.output:
			self.output = win.create_output_panel('an')
			view = self.view or win.active_view()
			self.output.settings().set('color_scheme', view.settings().get('color_scheme'))
		
		if text is not None:
			self.output.run_command('set_text', {'text': extypes.astr(text)})
		
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
			self.output.run_command('append', {"characters": s})
			self.output.run_command('viewport_scrool', {"di": 4})

	# 打印错误
	def logerr(self, e):
		if not self.output:
			self.tout()
		import traceback
		self.echo(traceback.format_exc())

	def _exec(self, text):
		try:
			self.init_exec_env()
			exec(text, self.edit.__dict__)
			return True
		except Exception as e:
			self.logerr(e)
			return False

	def _eval(self, text):
		try:
			self.init_exec_env()
			self.edit._ret = eval(text, self.edit.__dict__)
			return True
		except Exception as e:
			self.logerr(e)
			return False

	def init_exec_env(self):
		edit = self.edit
		edit.print = self.echo
		edit._print = print
		if self.globals:
			for key, val in self.globals.items():
				edit.__dict__.setdefault(key, val)

	# 获取设置文本
	def text(self, text = None):
		if text is not None:
			self.view.replace(self.edit, __class__.region(self.view), extypes.astr(text))
		else:
			return self.view.substr(__class__.region(self.view))

	def open(self, file, win = None):
		"""打开文件或目录"""
		(win or sublime.Window(self.window_id)).run_command('open_file', {"file": file})

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

	def __getattr__(self, name):
		return self._data[self.window_id].get(name, None)

	def __setattr__(self, name, value):
		if name in __class__.__slots__:
			object.__setattr__(self, name, value)
		else:
			self._data[self.window_id][name] = value

	def __delattr__(self, name):
		if name in __class__.__slots__:
			object.__delattr__(self, name)
		else:
			del self._data[self.window_id][name]

	def sublvars(self):
		"""sublime variables"""
		return sublime_api.window_extract_variables(self.window_id)

	def varsval(self, val):
		return sublime_api.expand_variables(val, self.sublvars())

	# 复制的数组（用换行分隔）
	@property
	def copied(self):
		return sublime.get_clipboard().split('\n')

	# 静态方法
	def region(view):
		return sublime.Region(0, view.size())

	def lines(view):
		return view.lines(__class__.region(view))