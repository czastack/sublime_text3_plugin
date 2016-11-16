import platform, sys
system = platform.system
is_linux = platform == "Linux"
is_windows = platform == "Windows"
py_ver = sys.version_info.major
is_py2 = py_ver == 2
is_py3 = py_ver == 3
del platform, sys, system
