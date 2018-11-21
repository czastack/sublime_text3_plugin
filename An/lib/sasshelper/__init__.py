import ctypes
from dllhelper import DllHelper


class SassHelper(DllHelper):

    __libname__ = __file__, 'sasshelper'

    @classmethod
    def fnsign(cls):
        char_p = [ctypes.c_char_p]
        return (
            ('set_include_path', char_p, None),
            ('sass_compile_string', char_p * 2, ctypes.c_int),
            ('sass_compile_file', char_p, ctypes.c_int),
            ('sass_get_result', char_p, None),
        )

    def set_include_path(self, path):
        p = ctypes.create_string_buffer(path.encode())
        self.clib.set_include_path(p)

    def compile_string(self, text, path=''):
        text = ctypes.create_string_buffer(text.encode())
        path = ctypes.create_string_buffer(path.encode())
        size_status = self.clib.sass_compile_string(text, path)
        return self._get_result(size_status)

    def compile_file(self, file):
        p = ctypes.create_string_buffer(file.encode())
        size_status = self.clib.sass_compile_file(p)
        return self._get_result(size_status)

    def _get_result(self, size_status):
        status = bool(size_status & 1)
        size = size_status >> 1
        buff = ctypes.create_string_buffer(size)
        self.clib.sass_get_result(buff)
        return status, buff.value.decode()


if __name__ == '__main__':
    helper = SassHelper()
    print(helper.compile_string('$fontSize: 12px;\nbody{\nfont-size:$fontSize;\n}'))
