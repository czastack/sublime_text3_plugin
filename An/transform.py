from utils.string import toggle_bc_case
from An import an
import sublime_plugin
import re


class BaseTransverter(sublime_plugin.TextCommand):
    def run(self, edit):
        if hasattr(self, 'init'):
            self.init()
        for region in self.view.selection:
            if not region.empty():
                self.view.replace(edit, region, self.transform(self.view.substr(region)))


class TransverterSelect(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_quick_panel([choice[0] for choice in __CHOICES__], self.onselect,
            selected_index=an._transform_last or -1)

    def onselect(self, index):
        if index == -1:
            return
        an._transform_last = index
        self.window.run_command('text_transform', {"index": index})


class TextTransform(sublime_plugin.TextCommand):
    def run(self, edit, index):
        for region in self.view.selection:
            if not region.empty():
                self.view.replace(edit, region, __CHOICES__[index][1](self.view.substr(region)))


def camel_or_lower(text):
    """驼峰下划线转换"""
    if '_' in text:
        # 转为驼峰
        text = re.sub(r'_[a-z]', lambda t: t.group(0)[1].upper(), text)
        # 开头大写
        text = text[0].upper() + text[1:]
    elif text.islower():
        # 开头大写
        text = text[0].upper() + text[1:]
    else:
        # 转为下划线
        text = re.sub(r'[A-Z]', lambda t: '_' + t.group(0).lower(), text)
        # 去掉开头的下划线
        if text[0] == '_':
            text = text[1:]
    return text


def to_sbc_case(text):
    """转成全角字符"""
    return toggle_bc_case(text, dbc=False)


def to_dbc_case(text):
    """转成半角字符"""
    return toggle_bc_case(text, sbc=False)


__CHOICES__ = (
    ('驼峰下划线转换', camel_or_lower),
    ('切换全角半角', toggle_bc_case),
    ('转成全角字符', to_sbc_case),
    ('转成半角字符', to_dbc_case),
)
