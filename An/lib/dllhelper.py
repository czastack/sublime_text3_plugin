import ctypes
import platform
import os
Path = os.path

class DllHelper:
    __slots__ = ()

    """
    :field __libname__: (pypath, name)
    :classmethod fnsign() -> (name, argtypes, restypes)
        eg. (('attach', None, c_bool),)
    """

    def __new__(cls):
        if getattr(cls, 'clib', None) is None:
            cls._load()
        return super().__new__(cls)

    @classmethod
    def _load(cls):
        pyfile, libname = cls.__libname__
        osname = platform.system()
        libdir = Path.dirname(pyfile)
        oldir = None

        if osname == 'Windows':
            libname = ('%s_x86.dll' if platform.architecture()[0].startswith('32') else '%s.dll') % libname
        elif osname == 'Darwin':
            libname = '%s.dylib' % libname
            oldir = os.getcwd()
            os.chdir(libdir)
        else:
            libname = '%s.so' % libname

        libpath = Path.join(libdir, libname)

        if Path.exists(libname):
            try:
                cls.clib = ctypes.cdll.LoadLibrary(libname)
            except Exception as e:
                if oldir:
                    os.chdir(oldir)
                raise e
            if oldir:
                os.chdir(oldir)
        else:
            raise Exception("Could not load " + libpath)

        for name, arg, ret in cls.fnsign():
            fn = getattr(cls.clib, name)
            fn.argtypes = arg
            fn.restype = ret