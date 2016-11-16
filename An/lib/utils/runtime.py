import platform, sys
system     = platform.system()
is_windows = system == "Windows"
is_linux   = system == "Linux"
is_mac     = system == "Darwin"

py_ver     = sys.version_info.major
is_py2     = py_ver == 2
is_py3     = py_ver == 3
del platform, sys, system
