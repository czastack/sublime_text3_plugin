from subl.view import get_lines
import sublime
import difflib


def view_diff(viewa, viewa, titlea, titleb):
    diff = difflib.unified_diff(get_lines(viewa), get_lines(viewb), titlea, titleb)
    difftxt = u"".join(line for line in diff)

    if difftxt == "":
        sublime.status_message("Files are identical")
    else:
        v = viewa.window().new_file()
        v.set_name(titlea + " -> " + titleb)
        v.set_scratch(True)
        v.assign_syntax('Packages/Diff/Diff.sublime-syntax')
        v.run_command('append', {'characters': difftxt})
