import sublime, re
from type import DictRef
from utils import add_brother_path

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
        sublime.error_message('未识别语法')
    if formatter_instance:
        text = formatter_instance.format(text).rstrip()
        text = re.sub(r'\r?\n', '\n' + formatter_instance.getIndent(pre_indent_level), text)
        if not ispart and formatter_instance.opts.__get__('add_empty_line_at_end', False):
            text += '\n'
        return text
    return None

class BaseFormatter:
    __slots__ = ('syntax', 'opts')

    def __init__(self, syntax, settings):
        self.syntax = syntax
        prefix = self.prefix if hasattr(self, 'prefix') else syntax
        self.opts = DictRef(settings.get(prefix + '_options'))
        env = globals()
        if self.depand not in env:
            # 加载依赖库
            add_brother_path(__file__, 'lib')
            env[self.depand] = __import__(self.depand)

    # 覆盖默认样式
    def coverOption(self, opt):
        opt.__dict__.update(self.opts.__dict__)

    def getIndent(self, level):
        if level <= 0:
            return ""
        if self.opts.indent_with_tabs:
            return '\t' * level
        else:
            return self.opts.indent_char * (self.opts.indent_size * level)

    # 是否允许保存时自动格式化
    def formatOnSaveEnabled(self):
        return self.opts.__get__("format_on_save", False)

class JsFormatter(BaseFormatter):
    __slots__ = ()
    depand = 'jsbeautifier'
    prefix = 'js'

    def format(self, text):
        options = jsbeautifier.default_options()
        self.coverOption(options)
        return jsbeautifier.beautify(text, options)

class CssFormatter(BaseFormatter):
    __slots__ = ()
    depand = 'cssbeautifier'

    def format(self, text):
        options = cssbeautifier.default_options()
        self.coverOption(options)
        return cssbeautifier.beautify(text, options)

class HtmlFormatter(BaseFormatter):
    __slots__ = ()
    depand = 'htmlbeautifier'

    def format(self, text):
        result = ""
        if self.opts.use_bs4:
            add_brother_path(__file__, 'lib/htmlbeautifier')
            from bs4 import BeautifulSoup
            p_indent_size = self.opts.__get__("indent_size", 4)
            
            soup = BeautifulSoup(text, 'html.parser')
            return soup.prettify(formatter=None, indent_size=p_indent_size)
        else:
            options = htmlbeautifier.default_options()
            self.coverOption(options)
            return htmlbeautifier.beautify(text, options)

FORMATTER_MAP = {
    'html': HtmlFormatter,
    'css': CssFormatter,
    'javascript': JsFormatter,
    'json': JsFormatter,
}

formatter_instance = None