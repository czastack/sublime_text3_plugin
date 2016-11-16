# sublime 工具集
import sublime

def opened_files(change_sep = True):
	"""当前窗口所有打开的文件名"""
	files = []
	for view in sublime.active_window().views():
		file = view.file_name()
		if file and change_sep:
			file = file.replace('\\', '/')
		files.append(file)
	return files

def load_settings(self, key, prefix = 'an_'):
	settings = getattr(self, '_settings', None)
	if not settings:
		settings = sublime.load_settings(prefix + self.name() + '.sublime-settings')
		self._settings = settings
	return settings.get(key)

def open_zip_file(zfpath, filename):
	import os
	from zipfile import ZipFile
	with ZipFile(zfpath) as zf:
		content = zf.read(filename).decode()
	view = sublime.active_window().new_file()
	view.set_name(filename.split(os.path.sep)[-1])
	view.run_command('append', {"characters": content})

def sass_compile_string(text):
	import sasshelper
	helper = sasshelper.SassHelper()
	helper.set_include_path(sublime.packages_path() + "/scss/scss/")
	pre = '@import "mixin.scss";\n'
	return helper.compile_string(pre + text).contents.content.decode()