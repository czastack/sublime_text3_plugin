import sublime
from os import path as Path


def sublime_path():
    return Path.dirname(sublime.__file__)


def default_packages_path():
    return Path.join(sublime_path(), 'Packages')


def opened_files(change_sep=True):
    """当前窗口所有打开的文件名"""
    files = []
    for view in sublime.active_window().views():
        file = view.file_name()
        if file and change_sep:
            file = file.replace('\\', '/')
        files.append(file)
    return files


def load_settings(self, key, prefix='an_'):
    settings = getattr(self, '_settings', None)
    if not settings:
        settings = sublime.load_settings(prefix + self.name() + '.sublime-settings')
        self._settings = settings
    return settings.get(key)


def load_platform_settings(arg1):
    """
    加载通用设置和平台专用设置
    :param arg1: Command实例或配置文件名称(不包括拓展名)
    """
    if isinstance(arg1, str):
        settings = sublime.load_settings(arg1 + '.sublime-settings')
        allsetting = settings.get("all")
        specific = settings.get(sublime.platform())
    else:
        allsetting = load_settings(arg1, "all")
        specific = load_settings(arg1, sublime.platform())

    if allsetting and specific:
        if isinstance(allsetting, list):
            allsetting.extend(specific)
        elif isinstance(allsetting, dict):
            allsetting.update(specific)
    elif specific:
        allsetting = specific
    return allsetting


def open(file, win):
    win.run_command('open_file', {"file": file})


def open_zip_file(zfpath, filename):
    import os
    from zipfile import ZipFile
    with ZipFile(zfpath) as zf:
        content = zf.read(filename).decode()
    view = sublime.active_window().new_file()
    view.set_name(filename.split(os.path.sep)[-1])
    view.run_command('append', {"characters": content})


def sass_compile_string(text):
    import sasshelper
    helper = sasshelper.SassHelper()
    helper.set_include_path(sublime.packages_path() + "/scss/scss/")
    pre = '@import "mixin.scss";\n'
    return helper.compile_string(pre + text).contents.content.decode()
