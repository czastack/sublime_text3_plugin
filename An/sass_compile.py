import sublime, sublime_plugin, sasshelper
from os import path as Path
from An import an

helper = None

class SassCompileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global helper
		if not helper:
			helper = sasshelper.SassHelper()

		an.set(self.view, edit)

		settings = sublime.load_settings('an_sass.sublime-settings')
		helper.set_include_path(settings.get('include_path'))
		autoload = settings.get('autoload')

		# 要编译的文本
		text = an.text()

		if autoload:
			text = ''.join(['@import "%s";\n' % item for item in autoload]) + text

		# 切换工作目录
		# curdir = Path.dirname(self.view.file_name())
		# oldir = os.getcwd()
		# os.chdir(curdir)
		# 取得编译结果
		result = helper.compile_string(text, Path.dirname(self.view.file_name()))
		# 切回当前目录
		# os.chdir(oldir)

		content = result.contents.content.decode()
		if result.contents.success:
			filename = self.view.file_name()
			dirname  = Path.dirname(filename)
			filename = Path.join(dirname, '..', 'css', Path.splitext(Path.basename(filename))[0] + '.css')
			with open(filename, 'w', encoding='utf-8') as f:
				f.write(content)
			sublime.status_message('编译成功')
		else:
			an.tout(content)
