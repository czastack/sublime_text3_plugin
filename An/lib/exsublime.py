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