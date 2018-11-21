import sublime_plugin
from An import an


class AnSnippetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if an._snip is None:
            an._snip = SnippetContainer()

        key = self.view.substr(self.view.selection[0])
        content = an._snip.get_snippet(key, self.view)
        if content:
            self.view.run_command('insert_snippet', {"contents": content})


class SnippetContainer(object):
    def get_snippets_map(self, view=None):
        snippets_map = an._snippets
        if snippets_map is None:
            snippets_map = an._snippets = {}
        return snippets_map

    def clear(self, snippets, view=None):
        self.get_snippets_map()[view and view.view_id] = None

    def clearAll(self, snippets, view=None):
        self.an._snippets = None

    def get_snippets(self, view):
        snippets_map = self.get_snippets_map()
        view = view and view.view_id
        snippets = snippets_map.get(view, None)
        if snippets is None:
            snippets = snippets_map[view] = {}
        return snippets

    def register(self, snippets, view=None):
        self.get_snippets(view).update(snippets)

    def get_snippet(self, key, view=None):
        return self.get_snippets(view).get(key, None) or self.get_snippets(None).get(key, None)
