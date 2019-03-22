"""调用winrar/file-roller打开包"""

import os
import sublime_plugin
import subl
import sublime
from utils import runtime


class ViewPackageCommand(sublime_plugin.WindowCommand):
    """contain_default 包括默认的包(sublime根目录/Packages)"""
    def show(self, packages_path):
        self.packages_path = packages_path
        self.packages = [f for f in os.listdir(self.packages_path) if f.endswith('.sublime-package')]
        self.window.show_quick_panel(self.packages, self.openPackageWithWinrar)

    def openPackageWithWinrar(self, i):
        if i != -1:
            cmd = ('start winrar "%s\\%s"' if runtime.is_windows else '(file-roller  "%s/%s" &)')
            p = os.popen(cmd % (self.packages_path, self.packages[i]))
            p.close()


class ViewDefaultPackageCommand(ViewPackageCommand):
    def run(self):
        ViewPackageCommand.show(self, subl.default_packages_path())


class ViewInstalledPackageCommand(ViewPackageCommand):
    def run(self):
        ViewPackageCommand.show(self, sublime.installed_packages_path())
