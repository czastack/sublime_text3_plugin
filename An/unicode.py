import sublime_plugin
from An import an
import re


class UnicodeDecodeCommand(sublime_plugin.TextCommand):
    reg = None

    def run(self, edit):
        if self.reg is None:
            self.reg = re.compile(r'(\\u[0-9a-fA-F]{4})+')
        if len(self.view.selection) == 1 and self.view.selection[0].empty():
            region = an.region(self.view)
            self.unicode_escape_region_tostr(edit, region)
        else:
            # 所选部分
            for region in self.view.selection:
                if not region.empty():
                    self.unicode_escape_region_tostr(edit, region)

    def unicode_escape_region_tostr(self, edit, region):
        origin = self.view.substr(region)
        result = self.reg.sub(lambda matcher: matcher.group(0).encode().decode('unicode_escape'), origin)
        self.view.replace(edit, region, result)
