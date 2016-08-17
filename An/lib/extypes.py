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

# 方法代理
def method_proxy(member, key):
	def fn(self, *args, **kwargs):
		return getattr(getattr(self, member), key)(*args, **kwargs)
	return fn

# 给类添加方法代理
def add_method_proxy(cls, member, keys):
	for key in keys:
		setattr(cls, key, method_proxy(member, key))

class Map(dict):
	__slots__ = ()

	def __getattr__(self, name):
		return self[name] if name in self else None

	def __setattr__(self, name, value):
		self[name] = value

	def __puts__(self, src, keys = None):
		puts(self, src, keys)

# data = Dict({'a': 1})
# print(data.a) # get 1
class Dict:
	__slots__ = ('__dict__')

	def __init__(self, obj):
		if isinstance(obj, dict):
			object.__setattr__(self, '__dict__', obj)
		else:
			raise TypeError('obj must be a dict')

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

	def __get__(self, name, defalut = None):
		return self.__dict__.get(name, defalut)

	def __puts__(self, src, keys = None):
		puts(self, src, keys)

	def __str__(self):
		return self.__dict__.__str__()

	def __iter__(self):
		return self.__dict__.__iter__()

	def __getitem__(self, key):
		if isinstance(key, tuple):
			return (self.__dict__[k] for k in key)
		elif isinstance(key, list):
			return [self.__dict__[k] for k in key]
		return self.__dict__[key]

	def __setitem__(self, key, value):
		if is_list_or_tuple(key):
			if is_list_or_tuple(value):
				val = iter(value).__next__
			else:
				val = lambda: value
			for k in key:
				self.__dict__[k] = val()
		else:
			self.__dict__[key] = value

	def __repr__(self):
		return __class__.__name__ + '(' + self.__str__() + ')'

	def __and__(self, keys):
		if is_list_or_tuple(keys):
			return __class__({key: self.__getattr__(key) for key in keys})

# add_method_proxy(Dict, '__dict__', ['__str__', '__iter__', '__getitem__', '__setitem__'])

# 接收字典列表
# datas = Dict([{'a': 1}, {'a': 2}])
# for data in datas:
#     print(data.a)
class Dicts:
	__slots__ = ('__ref', '__iter')

	def __init__(self, array):
		if is_list_or_tuple(array):
			self.__ref = None
			self.__iter = array.__iter__()
		else:
			raise TypeError('array must be a list or tuple')

	def __iter__(self):
		return self

	def __next__(self):
		data = next(self.__iter)
		if not self.__ref:
			self.__ref = Dict(data)
		else:
			self.__ref.__init__(data)
		return self.__ref

	next = __next__