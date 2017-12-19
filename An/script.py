import sublime_plugin
from An import an

class AnScriptCommand(sublime_plugin.TextCommand):
    def run(self, edit, name, args=[], kwargs={}):
        an.set(self.view, edit)
        
        module, name = name.rsplit('.', 1)
        if module[0] == '.':
            module = 'An.scripts' + module

        fn = getattr(__import__(module, fromlist=[name]), name)
        fn(*args, **kwargs)
