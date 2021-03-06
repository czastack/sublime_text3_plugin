import sublime
import sublime_plugin
from An import an
import extypes
import re


class ExecDocumentCommand(sublime_plugin.TextCommand):
    """执行当前文件内的语句"""
    def run(self, edit):
        an.attach(self.view, edit)
        an.exec_(an.text(self.view))


class ExecSelectionCommand(sublime_plugin.TextCommand):
    """执行选中的语句"""
    def run(self, edit):
        an.attach(self.view, edit)
        for region in self.view.selection:
            if region.empty():
                region = self.view.line(region.a)
            edit.ret = None
            if an.exec_(self.view.substr(region)) and edit.ret:
                self.view.replace(edit, region, extypes.astr(edit.ret))


class EvalSelectionCommand(sublime_plugin.TextCommand):
    """执行选中的表达式并替换当前文本"""
    def run(self, edit):
        an.attach(self.view, edit)
        for region in self.view.selection:
            if not region.empty() and an.eval_(self.view.substr(region)):
                self.view.replace(edit, region, extypes.astr(edit.ret))


class ComputeHexCommand(sublime_plugin.TextCommand):
    """计算选中的16进制表达式并替换当前文本"""
    reg_hex = re.compile('([\\da-fA-F]+)')

    def run(self, edit):
        an.attach(self.view, edit)
        for region in self.view.selection:
            if not region.empty():
                ret = "%X" % eval(self.reg_hex.sub('0x\\1', self.view.substr(region)))
                self.view.replace(edit, region, ret)


class ToExprCommand(sublime_plugin.TextCommand):
    """选择文字替换成表达式"""
    def run(self, edit, text=None):
        if text:
            self.on_exec(edit, text)
            return

        default = an.to_expr_last if an.to_expr_last else 'src'
        input_panel = self.view.window().show_input_panel('to expr', default, self.on_input_text, None, None)
        # 选中默认文字
        input_panel.selection.add(an.region(input_panel))

    def on_input_text(self, text):
        an.to_expr_last = text
        self.view.run_command(self.name(), {"text": text})

    def on_exec(self, edit, text):
        an.attach(self.view, edit)
        edit.i = 0
        for region in self.view.selection:
            edit.src = self.view.substr(region)
            edit.i += 1
            if(an.eval_(text)):
                self.view.replace(edit, region, extypes.astr(edit.ret))


class InsertListCommand(sublime_plugin.TextCommand):
    """插入列表"""
    def run(self, edit, text=None):
        if text:
            self.on_insert(edit, text)
            return

        # 默认是插入数字
        default = an.insert_text_last if an.insert_text_last else (
            '["%%01d" %% x for x in range(1, %d)]' % (len(self.view.selection) + 1))
        input_panel = self.view.window().show_input_panel('list expr', default, self.on_input_text, None, None)
        # 选中默认文字
        input_panel.selection.add(an.region(input_panel))

    def on_input_text(self, text):
        an.insert_text_last = text
        self.view.run_command(self.name(), {"text": text})

    def on_insert(self, edit, text):
        an.attach(self.view, edit)
        edit.ret = None
        edit._n = True  # 是否自动插入换行
        an.eval_(text) or an.exec_(text)
        if hasattr(edit.ret, '__len__'):
            selectionlen = len(self.view.selection)
            if selectionlen > 1:
                # 依次应用到光标
                itr = iter(edit.ret)
                i = 0
                for region in self.view.selection:
                    if i == selectionlen:
                        break
                    else:
                        i += 1
                    cur = itr.__next__()  # 当前要插入的文本
                    if not isinstance(cur, str):
                        cur = str(cur)
                    self.view.replace(edit, region, cur)
            else:
                # 列表插入到当前位置
                regions = []
                i = 0
                itemlen = len(edit.ret)
                usetpl = False  # 使用模板
                region = self.view.selection[0]
                if selectionlen == 1 and region.size() > 1 and self.view.substr(region.begin()) == '%':
                    usetpl = True
                    tpl = self.view.substr(sublime.Region(region.begin() + 1, region.end()))  # 模板文字
                self.view.erase(edit, region)
                while i < itemlen:
                    item = edit.ret[i]
                    if not usetpl:
                        item = extypes.astr(item)
                    else:
                        if isinstance(item, (list, tuple)):
                            argslen = len(item)  # 当前参数的长度
                            iscontainer = argslen > 0 and isinstance(item[0], (list, tuple))
                            if iscontainer and argslen == 1:
                                item = tpl.format(*item[0])
                            elif iscontainer and argslen == 2:
                                item = tpl.format(*item[0], **item[1])
                            else:
                                item = tpl.format(*item)
                        elif isinstance(item, dict):
                            item = tpl.format(**item)  # 替换一个参数
                        else:
                            item = extypes.astr(item)
                            item = tpl.format(item)
                    cur = self.view.selection[-1].a
                    regions.append(sublime.Region(cur, cur + len(item)))
                    self.view.insert(edit, cur, item)
                    i += 1
                    if edit._n and i < itemlen:
                        self.view.run_command('insert', {"characters": "\n"})
                self.view.selection.clear()
                self.view.selection.add_all(regions)


class StartTestCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.new_file(syntax='Python.sublime-syntax')
        view.set_name('Test')
        an.attach(view)
        an.set_output()
