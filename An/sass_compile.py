import sublime_plugin
import os, sasshelper
from os import path as Path
from An import an

class SassCompileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		an.set(self.view, edit)

		# 切换工作目录
		curdir = Path.dirname(self.view.file_name())
		oldir = os.getcwd()
		os.chdir(curdir)
		# 取得编译结果
		result = sasshelper.compile_string(an.text())
		# 切回当前目录
		os.chdir(oldir)

		content = result.contents.content.decode()
		if result.contents.success:
			filename = self.view.file_name()
			dirname  = Path.dirname(filename)
			filename = Path.join(dirname, '..', 'css', Path.splitext(Path.basename(filename))[0] + '.css')
			with open(filename, 'w', encoding='utf-8') as f:
				f.write(content)
			an.show_output('编译成功')
		else:
			an.show_output(content)
			pass
