# 在指定文件夹运行程序
import sublime, sublime_plugin, os
from An import an
from subl import load_settings
from utils.path import run_at

class RunHearCommand(sublime_plugin.WindowCommand):
	def run(self, path = None):
		self.run_list_data = load_settings(self, sublime.platform())
		if self.run_list_data:
			run_list = [[item['title'], item['path']] for item in self.run_list_data]
			if not path:
				path = os.path.dirname(self.window.active_view().file_name())
			self.window.show_quick_panel(run_list, run_at(self.onselect, path), selected_index=an._run_hear_last or -1)

	def onselect(self, index):
		if index == -1:
			return
		an._run_hear_last = index
		cmd = self.run_list_data[index]['path']
		if sublime.platform() == 'windows':
			cmd = 'start ' + cmd
		p = os.popen(cmd)
		p.close()
