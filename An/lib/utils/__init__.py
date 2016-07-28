import sys
from os import path as Path

# 把兄弟文件夹添加到sys.path
def add_brother_path(selfpath, brother):
    dirpath = Path.join(Path.dirname(Path.abspath(selfpath)), brother)
    if dirpath not in sys.path:
        sys.path.append(dirpath)

# 生成字符序列
def strsq(a, b, split = ''):
	def check_param(ch):
		ok = False
		if isinstance(ch, str):
			if len(ch) == 1:
				ch = ord(ch)
				ok = True
		elif isinstance(ch, int):
			ok = True
		if ok:
			return ch
		else:
			raise ValueError('参数必须是字符或者整数')
	a = check_param(a)
	b = check_param(b)
	if a > b:
		a, b = b, a
	sq = (chr(x) for x in range(a, b + 1))
	return split.join(sq) if isinstance(split, str) else sq

# def python_version():
#     import sys
#     return sys.version_info.major

# def create_module(name):
#     return type(sys)(name)

# def import_to(module_to, source, fromlist):
#     source_module = __import__(source, fromlist=fromlist)
#     for attr in fromlist:
#         module_to.__dict__[attr] = source_module.__dict__[attr]

# is_py2 = python_version() == 2

# if is_py2:
#     from urllib2 import HTTPError
#     request = create_module('request')
#     import_to(request, 'urllib2', 
#         ['urlopen', 'Request', 'HTTPSHandler', 'HTTPCookieProcessor', 'ProxyHandler', 'ProxyHandler', 'build_opener', 'install_opener'])
#     parse = create_module('parse')
#     import_to(parse, 'urllib', ['urlencode', 'quote', 'unquote'])
#     import_to(parse, 'urlparse', ['parse_qs', 'urlparse'])
# else:
#     from urllib import request, parse