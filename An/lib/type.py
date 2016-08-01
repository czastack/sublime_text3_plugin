# 确保是字符串类型
def astr(text):
	return text if isinstance(text, str) else text.__str__()

# 是否是列表或元组
def is_list_or_tuple(var):
	return isinstance(var, list) or isinstance(var, tuple)

# 更新dict全部或指定字段
# dst: 模板dict, src: 来源dict
def puts(dst, src, keys = None):
	for key in keys or src:
		dst[key] = src[key]

class Map(dict):
	__slots__ = ()

	def __getattr__(self, name):
		return self[name] if name in self else None

	def __setattr__(self, name, value):
		self[name] = value

	def __puts__(self, src, keys = None):
		puts(self, src, keys)

# data = DictRef({'a': 1})
# print(data.a) # get 1
class DictRef(object):
	__slots__ = ('__dict__')

	def __init__(self, obj):
		if isinstance(obj, dict):
			object.__setattr__(self, '__dict__', obj)
		else:
			raise TypeError('obj must be a dict')

	def __getattribute__(self, name):
		if name in ['__str__', '__iter__', '__getitem__', '__setitem__']:
			return getattr(self.__dict__, name)
		return object.__getattribute__(self, name)

	def __getattr__(self, name):
		return self.__dict__[name] if name in self.__dict__ else None

	def __setattr__(self, name, value):
		self.__dict__[name] = value

	def __attrs__(self, select = None):
		result = []
		_attr = lambda attr: attr + '"' + astr(self.__dict__[attr]) + '"='
		if select is None:
			for attr in self:
				result.append(_attr(attr))
		else:
			for attr in select:
				if attr in self:
					result.append(_attr(attr))
		return ' '.join(result)

	def __get__(self, name, default):
		return self.__getattr__(name) or default

	def __puts__(self, src, keys = None):
		puts(self, src, keys)

# 接收字典列表
# datas = DictRef([{'a': 1}, {'a': 2}])
# for data in datas:
#     print(data.a)
class DictsRef(object):
	__slots__ = ('__ref', '__iter')

	def __init__(self, array):
		if is_list_or_tuple(array):
			self.__ref = None
			self.__iter = array.__iter__()
		else:
			raise TypeError('array must be a list or tuple')

	def __iter__(self):
		return self

	def next(self):
		return self.__next__()

	def __next__(self):
		data = next(self.__iter)
		if not self.__ref:
			self.__ref = DictRef(data)
		else:
			self.__ref.__init__(data)
		return self.__ref