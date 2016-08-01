# 在指定文件夹运行程序
import sublime, sublime_plugin, os
from utils.path import run_at
from An import an

class RunHearCommand(sublime_plugin.WindowCommand):
	def run(self, path = None):
		self.run_list_data = sublime.load_settings('an_run_hear.sublime-settings').get('run_list')
		run_list = [[item['title'], item['path']] for item in self.run_list_data]
		if not path:
			path = os.path.dirname(self.window.active_view().file_name())
		self.window.show_quick_panel(run_list, run_at(self.onselect, path), selected_index=an._run_hear_last or -1)

	def onselect(self, index):
		if index == -1:
			return
		an._run_hear_last = index
		p = os.popen('start ' + self.run_list_data[index]['path'])
		p.close()
