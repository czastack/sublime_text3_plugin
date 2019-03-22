# 打开文件

import sublime_plugin
import subl


class OpenAnFileCommand(sublime_plugin.WindowCommand):
    """打开指定路径文件"""

    def run(self):
        input_panel = self.window.show_input_panel('path', '', self.on_input_path, None, None)
        # 选中默认文字
        input_panel.selection.add(an.region(input_panel))

    def on_input_path(self, path):
        subl.open(path, self.window)
