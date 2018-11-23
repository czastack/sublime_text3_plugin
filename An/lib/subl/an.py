import sublime
import sublime_api
import extypes
import subl
import subl.view
import utils.string
import utils.path


class An:
    __slots__ = ('_data', 'window_id', 'exec_scope')

    def __init__(self):
        self._data = {}
        self.attachWindow(0)
        self.exec_scope = {
            'an': self,
            'print': self.echo,
            '_print': print,
            'sublime': sublime,
        }

    def onload(self):
        self.attachWindow(sublime_api.active_window())

    def attachWindow(self, window_id):
        self.window_id = window_id
        self._data.setdefault(window_id, {})
        self._data[self.window_id].setdefault('globals', extypes.Map())

    def set(self, view, edit=None):
        window_id = sublime_api.view_window(view.view_id)
        if self.window_id != window_id:
            self.attachWindow(sublime_api.view_window(view.view_id))

        if view == self.output:
            view = sublime.View(sublime_api.window_active_view(window_id))

        self.view = view
        self.edit = edit

    def tout(self, text=None):
        win = sublime.Window(self.window_id)
        output = self.output
        if not output:
            output = self.output = win.create_output_panel('an')
            view = self.view or win.active_view()
            # self.output.settings().set('color_scheme', view.settings().get('color_scheme'))
            output.assign_syntax('Packages/Text/Plain text.tmLanguage')

        if text is not None:
            output.run_command('set_text', {'text': extypes.astr(text)})

        win.run_command('show_panel', {'panel': 'output.an'})

    def cls(self):
        """清空控制台"""
        if self.output:
            view = self.output
            if view.is_in_edit():
                # 如果在output发起的exec, is_in_edit返回True, undo就不会运行
                sublime.set_timeout(self.cls, 500)
            else:
                while view.size():
                    view.run_command('undo')

    def echo(self, *args, **kwargs):
        """控制台打印"""
        kwargs['file'] = self
        print(*args, **kwargs)

    def flush(self):
        """作为print file参数"""
        if self.stdout:
            self.stdout.flush()

    def write(self, s):
        if self.stdout and not self.haserr:
            self.stdout.write(s)
        elif self.output:
            self.output.run_command('append', {"characters": s})
            self.output.run_command('viewport_scrool', {"di": 4})

    def logerr(self, e):
        """打印错误信息"""
        if not self.output:
            self.tout()
        import traceback
        self.haserr = True
        self.echo(traceback.format_exc())
        self.haserr = False

    def exec_(self, text):
        try:
            self.init_exec_env()
            exec(text, self.edit.__dict__)
            return True
        except Exception as e:
            self.logerr(e)
            return False

    def eval_(self, text):
        try:
            self.init_exec_env()
            self.edit.ret = eval(text, self.edit.__dict__)
            return True
        except Exception as e:
            self.logerr(e)
            return False

    def init_exec_env(self):
        edit = self.edit
        edit.view = self.view
        edit.__dict__.update(self.exec_scope)
        if self.globals:
            for key, val in self.globals.items():
                edit.__dict__.setdefault(key, val)

    def get_window(self):
        return sublime.Window(self.window_id)

    def active_view(self):
        return self.get_window().active_view()

    def open(self, file):
        """打开文件或目录"""
        subl.open(utils.path.get_file(file), self.get_window())

    def popup(self, text, **args):
        style = '<style>body{margin:0; padding:10px; color:#ccc; font-size:18px; background-color:#000;}</style>'
        self.view.show_popup(style + text, **args)

    def __getattr__(self, name):
        return self._data[self.window_id].get(name, None)

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            object.__setattr__(self, name, value)
        else:
            self._data[self.window_id][name] = value

    def __delattr__(self, name):
        if name in __class__.__slots__:
            object.__delattr__(self, name)
        else:
            del self._data[self.window_id][name]

    def sublvars(self):
        """sublime variables"""
        return sublime_api.window_extract_variables(self.window_id)

    def varsval(self, val):
        return sublime_api.expand_variables(val, self.sublvars())

    @property
    def copied(self):
        """ 复制的数组（用换行分隔）
        另见: selected_text
        """
        return sublime.get_clipboard().split('\n')

    @property
    def copied_tuple(self):
        """复制的元组"""
        return tuple(self.copied)

    def text(self, view=None):
        return subl.view.view_text(view or self.view)

    def selected_text(self, view=None):
        return subl.view.selected_text(view or self.view)

    def clone(self):
        self.run_win_command('clone_file')

    def matchAll(self, reg, fn):
        return utils.string.matchAll(self.text(), reg, fn)

    def replace(self, rulers):
        result = utils.string.replace(self.text(), rulers)
        self.view.run_command('set_text', {'text': result})

    def map_selected_text(self, fn, withIndex=False):
        origin = self.selected_text()
        if withIndex:
            origin = enumerate(origin)
        texts = list(map(fn, origin))
        self.view.run_command('set_regions_text', {'texts': texts})

    region = staticmethod(subl.view.view_region)
    run_win_command = sublime.Window.run_command
