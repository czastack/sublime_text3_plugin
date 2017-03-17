import platform, sys

from os import path as Path

system     = platform.system()
is_windows = system == "Windows"
is_linux   = system == "Linux"
is_mac     = system == "Darwin"

py_ver     = sys.version_info.major
is_py2     = py_ver == 2
is_py3     = py_ver == 3


# 把兄弟文件夹添加到sys.path
def add_brother_path(selfpath, brother):
    dirpath = Path.join(Path.dirname(Path.abspath(selfpath)), brother)
    if dirpath not in sys.path:
        sys.path.append(dirpath)