import re
from extypes import Dict
from utils import add_brother_path

class BaseFormatter:
    __slots__ = ('syntax', 'opts')

    def __init__(self, syntax, settings):
        self.syntax = syntax
        # prefix = self.prefix if hasattr(self, 'prefix') else syntax
        self.opts = Dict(settings.get(syntax + '_options'))
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
        return self.opts.format_on_save

class JsFormatter(BaseFormatter):
    __slots__ = ()
    depand = 'jsbeautifier'

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
            p_indent_size = self.opts.indent_size or 4
            
            soup = BeautifulSoup(text, 'html.parser')
            return soup.prettify(formatter=None, indent_size=p_indent_size)
        else:
            options = htmlbeautifier.default_options()
            self.coverOption(options)
            return htmlbeautifier.beautify(text, options)

FORMATTER_MAP = {
    'html': HtmlFormatter,
    'css': CssFormatter,
    'sass': CssFormatter,
    'js': JsFormatter,
    'json': JsFormatter,
}