# 调用winrar打开包

import sublime_plugin, os

# contain_default 包括默认的包(sublime根目录/Packages)
class ViewPackageCommand(sublime_plugin.WindowCommand):
	def show(self, packages_path):
		self.packages_path = packages_path
		self.packages = [f for f in os.listdir(self.packages_path) if f.endswith('.sublime-package')]
		self.window.show_quick_panel(self.packages, self.openPackageWithWinrar)

	def openPackageWithWinrar(self, i):
		if i != -1:
			p = os.popen('start winrar "%s\\%s"' % (self.packages_path, self.packages[i]))
			p.close()

class ViewDefaultPackageCommand(ViewPackageCommand):
	def run(self):
		import An
		ViewPackageCommand.show(self, An.default_packages_path())

class ViewInstalledPackageCommand(ViewPackageCommand):
	def run(self):
		import sublime
		ViewPackageCommand.show(self, sublime.installed_packages_path())
