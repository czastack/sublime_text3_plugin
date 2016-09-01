import sublime, sublime_plugin, re
from .codeformatter.formatter import FORMATTER_MAP

formatter_instance = None

SCOPE_SYNTAX_MAP = (
    ('source.js', 'js'),
    ('source.css', 'css'),
    ('source.sass', 'css'),
    ('source.scss', 'css'),
    ('text.html', 'html'),
)

def show_error(text):
    import traceback
    traceback.print_exc()
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
                    syntax = None
                    scopea = self.view.scope_name(region.a)
                    scopeb = self.view.scope_name(region.b)
                    for scope in SCOPE_SYNTAX_MAP:
                        if scope[0] in scopea and scope[0] in scopeb:
                            syntax = scope[1]
                            break
                    if syntax is None:
                        raise ValueError('不支持的语法')
                    text = self.view.substr(region)
                    indent_level = self.view.indentation_level(region.begin())
                    result = format(text, syntax, indent_level, ispart)
                    if result:
                        self.view.replace(edit, region, result)
                except Exception as e:
                    show_error(e)

class CodeFormatterReloadSettingCommand(sublime_plugin.WindowCommand):
    def run(self):
        formatter.formatter_instance = None

# return 格式化后的文本
def format(text, syntax, pre_indent_level = 0, ispart = False):
    global formatter_instance
    if formatter_instance and formatter_instance.syntax == syntax:
        pass
    elif syntax in FORMATTER_MAP:
        settings = sublime.load_settings('CodeFormatter.sublime-settings')
        formatter_instance = FORMATTER_MAP[syntax](syntax, settings)
    else:
        formatter_instance = None
        raise ValueError('不支持的语法')
    if formatter_instance:
        text = formatter_instance.format(text).rstrip()
        text = re.sub(r'\r?\n', '\n' + formatter_instance.getIndent(pre_indent_level), text)
        if not ispart and formatter_instance.opts.add_empty_line_at_end:
            text += '\n'
        return text
    return None

# 获取语法名
def getSyntax(syntax_file):
    pattern = re.compile(r"Packages/.*/(.+?).(?=tmLanguage|sublime-syntax)")
    matcher = pattern.search(syntax_file)
    return matcher.group(1).lower() if matcher else None