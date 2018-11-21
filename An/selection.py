from An import an
import re
import sublime
import sublime_plugin


class BaseSelect(sublime_plugin.TextCommand):
    def set_regions(self, regions):
        self.view.selection.clear()
        self.view.selection.add_all(regions)


class SelectReg(BaseSelect):
    """选中所选部分中符合指定正则表达式的内容"""
    flags = re.M

    def run(self, edit):
        view = self.view
        regions = []
        sel_len = len(view.selection)
        if sel_len == 0 or (sel_len == 1 and view.selection[0].empty()):
            selection = [an.region(view)]
        else:
            selection = view.selection
        for region in selection:
            pt = region.begin()
            text = view.substr(region)
            for m in re.finditer(self.reg, text, self.flags):
                span = m.span()
                regions.append(sublime.Region(span[0] + pt, span[1] + pt))
        self.set_regions(regions)


class SelectLineStartCommand(SelectReg):
    """快速选中所有行首"""
    reg = '^'


class SelectLineEndCommand(SelectReg):
    """快速选中所有行尾"""
    reg = '$'


class SelectLineAllCommand(SelectReg):
    """快速选中所有行"""
    reg = '.+'


class SelectEmptyLinesCommand(SelectReg):
    """选中空行"""
    reg = '\n[ \t]*(?=\n|$)'


class SelectLineEndSpaceCommand(SelectReg):
    """选中行结尾的空白字符"""
    reg = '[ \t]+(?=\n|$)'


class SplitSelectByLenCommand(BaseSelect):
    """按长度分隔选区"""
    def run(self, edit):
        # 显示输入框
        input_panel = self.view.window().show_input_panel('分隔长度', '', self.on_input_text, None, None)

    def on_input_text(self, text):
        regions = []
        step = int(text)
        if step > 0:
            for region in self.view.selection:
                if not region.empty():
                    start = region.begin()
                    end = region.end()
                    i = start
                    while i < end:
                        regions.append(sublime.Region(i, min(i + step, end)))
                        i += step
            if len(regions) > 0:
                self.view.selection.clear()
                self.view.selection.add_all(regions)


class SplitSelectByRegCommand(BaseSelect):
    """用正则表达式分隔选区"""
    def run(self, edit):
        # 显示输入框
        input_panel = self.view.window().show_input_panel('分隔文本', '', self.on_input_text, None, None)

    def on_input_text(self, text):
        if text is not '':
            import re
            reg = re.compile(text)
            regions = []
            for region in self.view.selection:
                if not region.empty():
                    pos = 0
                    start = region.begin()
                    end = region.end()
                    itemtext = self.view.substr(region)
                    while True:
                        matcher = reg.search(itemtext, pos)
                        if not matcher:
                            break
                        span = matcher.span()
                        regions.append(sublime.Region(start + pos, start + span[0]))
                        pos = span[1]

                    if pos < end:
                        regions.append(sublime.Region(start + pos, end))
            if len(regions) > 0:
                self.view.selection.clear()
                self.view.selection.add_all(regions)


class SelectStartToEndCommand(BaseSelect):
    """选区行尾互换"""
    def run(self, edit):
        regions = [sublime.Region(region.b, region.a) for region in self.view.selection]
        self.set_regions(regions)


class ExchangeSelectCommand(BaseSelect):
    """交换两个选区的内容"""
    def run(self, edit):
        if len(self.view.selection) == 2:
            view = self.view
            tmp = view.substr(view.selection[0])
            view.replace(edit, view.selection[0], view.substr(view.selection[1]))
            view.replace(edit, view.selection[1], tmp)


class SelectionQuoteCommand(BaseSelect):
    """选中引号外侧/内侧"""
    def run(self, edit):
        view = self.view
        regions = []
        for region in view.selection:
            desc = region.a > region.b
            if desc:
                region.a, region.b = region.b, region.a

            quote = view.substr(region.begin())
            if quote in '\'"':
                # deflate 缩小
                inflate = False
            else:
                quote = view.substr(region.begin() - 1)
                if quote in '\'"':
                    # inflate 扩充
                    inflate = True
                else:
                    quote = None
            if quote:
                da, db = (-1, 1) if inflate else (1, -1)
                if inflate:
                    while view.substr(region.a + da) == quote:
                        region.a += da
                    while view.substr(region.b) == quote:
                        region.b += db
                else:
                    while view.substr(region.a) == quote:
                        region.a += da
                    while view.substr(region.b + db) == quote:
                        region.b += db
                if desc:
                    region.a, region.b = region.b, region.a
                regions.append(region)
        if regions:
            self.set_regions(regions)


class SelectMiddleCommand(BaseSelect):
    """选中每两个光标中间的区域（列模式）"""
    def run(self, edit, sort_by_col=False):
        view = self.view
        regions = []
        selection = list(self.view.selection)
        if sort_by_col:
            # 横向扫描
            selection = sorted(selection, key=lambda s: view.rowcol(s.a)[1])
        if len(selection) & 1:
            selection.pop()
        itr = iter(selection)
        for region in itr:
            aa, ab = view.rowcol(region.a)
            ba, bb = view.rowcol(next(itr).a)
            while aa <= ba:
                a = view.text_point(aa, ab)
                b = view.text_point(aa, bb)
                if view.rowcol(a) == (aa, ab):
                    if view.rowcol(b) != (aa, bb):
                        # 这行不够长
                        b = view.text_point(aa + 1, 0) - 1
                    regions.append(sublime.Region(a, b))
                aa += 1
        self.set_regions(regions)


class SelectToArrayCommand(sublime_plugin.TextCommand):
    """选中区域暂存"""
    def run(self, edit):
        data = []
        for region in self.view.selection:
            data.append(self.view.substr(region))
        an.tmp = data
