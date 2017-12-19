import sublime_plugin
from subl.view import view_region

class SetTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.replace(edit, view_region(self.view), text)
        self.view.selection.clear()


class SetRegionsTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, texts):
        texts = iter(texts)
        for region in self.view.selection:
            if region.empty():
                region = self.view.line(region.a)
            try:
                self.view.replace(edit, region, next(texts))
            except StopIteration:
                break
