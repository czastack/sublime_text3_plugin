if __name__ == 'An':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
    del os, sys

    from subl.an import An
    an = An()
else:
    def plugin_loaded():
        from An import an
        an.onload()

        import subl
        import sys
        paths = subl.load_platform_settings('an_python_path')
        if paths:
            sys.path[:0] = paths
