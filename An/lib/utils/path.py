import os
import types


def run_at(fn, new_dir):
    """在指定路径运行"""
    def wrapper(*args, **kwargs):
        # 暂存当前目录
        if new_dir:
            oldir = os.getcwd()
            os.chdir(new_dir)
        # 运行目标
        ret = fn(*args, **kwargs)
        # 切回当前目录
        if new_dir:
            os.chdir(oldir)
        return ret
    return wrapper


def get_file(obj):
    """获取一个python对象所在文件"""
    if isinstance(obj, str):
        return obj

    if isinstance(obj, types.ModuleType):
        return obj.__file__

    if isinstance(obj, types.FunctionType) and obj.__code__:
        return obj.__code__.co_filename

    if isinstance(obj, type):
        if obj.__module__ != 'builtins':
            return __import__(obj.__module__).__file__