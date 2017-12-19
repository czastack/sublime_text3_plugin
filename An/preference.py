import sublime, sublime_plugin

class LoadPlatformPreferences(sublime_plugin.ApplicationCommand):
    __slots__ = ()

    def __init__(self):
        sublime.set_timeout(self.start)

    def start(self):
        self.settings = sublime.load_settings('Preferences.sublime-settings')
        self.platform_setting = sublime.load_settings('Platform.sublime-settings')
        self.platform_setting.add_on_change('an_platform_setting', self.load_settings)
        self.load_settings()

    def load_settings(self):
        new_settings = self.platform_setting.get(sublime.platform())
        if new_settings:
            for key, val in new_settings.items():
                self.settings.set(key, val)