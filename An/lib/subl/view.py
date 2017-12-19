import sublime


class ViewWriter:
    __slots__ = ('view')

    def __init__(self, view):
        self.view = view

    def flush(self):
        pass

    def write(self, s):
        self.view.run_command('append', {"characters": s})

    def cls(self):
        self.view.run_command('clear_text')


def view_region(view):
    return sublime.Region(0, view.size())


def view_text(view):
    return view.substr(view_region(view))


def get_lines(view):
    return view_text(view).split('\n')


def lines_region(view):
    return view.lines(region(view))


def selected_text(view):
    texts = []
    for region in view.selection:
        if region.empty():
            region = view.line(region.a)
        texts.append(view.substr(region))
    return texts