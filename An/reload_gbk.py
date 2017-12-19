import sublime_plugin
import subl.view

class ReloadGbkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name = self.view.file_name()
        if file_name:
            with open(file_name, 'r', encoding='GBK') as f:
                self.view.replace(edit, subl.view.view_region(self.view), f.read())
                self.view.set_encoding('UTF-8')
