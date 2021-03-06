from An import an
import sublime
import sublime_plugin
import sasshelper
import os

helper = None


def get_settings():
    return sublime.load_settings('an_sass.sublime-settings')


def compile(view):
    Path = os.path
    filename = view.file_name()
    if not filename:
        return False

    global helper
    if not helper:
        helper = sasshelper.SassHelper()

    an.attach(view)

    settings = get_settings()
    include_path = settings.get('include_path')
    if include_path:
        if '@' in include_path:
            include_path = include_path.replace('@', sublime.packages_path() + Path.sep)
        helper.set_include_path(include_path)
    autoload = settings.get('autoload')

    # 要编译的文本
    text = an.text()

    if autoload:
        text = ''.join(['@import "%s";\n' % item for item in autoload]) + text

    status, content = helper.compile_string(text, Path.dirname(filename))

    if status:
        dirname = Path.dirname(filename)
        filename = Path.join(dirname, '..', 'css', Path.splitext(Path.basename(filename))[0] + '.css')
        cssdir = Path.dirname(filename)
        if not Path.exists(cssdir):
            os.mkdir(cssdir)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        sublime.status_message('编译成功')
        return True
    else:
        an.set_output(content)
        return False


class SassCompileCommand(sublime_plugin.WindowCommand):
    def run(self):
        compile(self.window.active_view())


class BuildonSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        filename = view.file_name()
        if (filename and filename.endswith('.scss') and ('parts' not in filename)
                and get_settings().get('build_on_save')):
            compile(view)
