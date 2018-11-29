import sublime_plugin


class ViewportScroolCommand(sublime_plugin.TextCommand):
    """ 光标不移动的滚动
        di: 1  下一行, di: -1 上一行
        di: 2  下一屏, di: -2 上一屏
        di: -4  开头, di: 4  结尾
    """
    def run(self, edit, di):
        top = self.view.viewport_position()[1]
        # 行高(layout单位)
        line_height = self.view.line_height()
        max_top = self.view.layout_extent()[1] - line_height
        mul = 1 if di > 0 else -1
        num = 0
        if di & 1:
            # 行滚动
            # 行高(layout单位)
            num = mul * line_height
        elif di & 2:
            # 屏滚动
            # 可视区高(layout单位)
            num = mul * self.view.viewport_extent()[1]
        else:
            # 开头或结尾
            if di < 0:
                top = 0
            else:
                top = max_top
        top += num
        if top < 0:
            top = 0
        elif top > max_top:
            top = max_top
        self.view.set_viewport_position((0, top))
