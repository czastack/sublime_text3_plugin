import sublime, sublime_plugin, sasshelper
from os import path as Path
from An import an

helper = None

def get_settings():
	return sublime.load_settings('an_sass.sublime-settings')

def compile(view):
	filename = view.file_name()
	if not filename:
		return False

	global helper
	if not helper:
		helper = sasshelper.SassHelper()

	an.set(view)

	settings = get_settings()
	helper.set_include_path(settings.get('include_path'))
	autoload = settings.get('autoload')

	# 要编译的文本
	text = an.text()

	if autoload:
		text = ''.join(['@import "%s";\n' % item for item in autoload]) + text

	result = helper.compile_string(text, Path.dirname(filename))

	content = result.contents.content.decode()
	if result.contents.success:
		dirname  = Path.dirname(filename)
		filename = Path.join(dirname, '..', 'css', Path.splitext(Path.basename(filename))[0] + '.css')
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(content)
		sublime.status_message('编译成功')
		return True
	else:
		an.tout(content)
		return False

class SassCompileCommand(sublime_plugin.WindowCommand):
	def run(self):
		compile(self.window.active_view())

class BuildonSave(sublime_plugin.EventListener):
	def on_post_save(self, view):
		filename = view.file_name()
		if filename and filename.endswith(".scss") and get_settings().get('build_on_save'):
			compile(view)
