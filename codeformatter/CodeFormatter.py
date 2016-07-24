import sublime, sublime_plugin, re
from .codeformatter import formatter

def show_error(text):
    sublime.error_message('CodeFormatter\n' + str(text))

class CodeFormatterCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax=False, saving=False):

        if self.view.is_scratch():
            return show_error("File is scratch")

        regionlen = len(self.view.selection)
        ispart = False # 是否是局部格式化
        if regionlen == 0 or (regionlen == 1 and self.view.selection[0].empty()):
            regions = [sublime.Region(0, self.view.size())]
        else:
            regions = self.view.selection
            ispart = True
        for region in regions:
            if not region.empty():
                try:
                    syntax = getSyntax(self.view.settings().get('syntax'))
                    text = self.view.substr(region)
                    indent_level = self.view.indentation_level(region.begin())
                    result = formatter.format(text, syntax, indent_level, ispart)
                    if result:
                        self.view.replace(edit, region, result)
                except Exception as e:
                    show_error(e)

class CodeFormatterReloadSettingCommand(sublime_plugin.WindowCommand):
    def run(self):
        formatter.formatter_instance = None

# 获取语法名
def getSyntax(syntax_file):
    pattern = re.compile(r"Packages/.*/(.+?).(?=tmLanguage|sublime-syntax)")
    matcher = pattern.search(syntax_file)
    return matcher.group(1).lower() if matcher else None