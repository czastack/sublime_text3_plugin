# 确保是字符串类型
def astr(text):
	return text if isinstance(text, str) else str(text)

# 是否是列表或元组
def is_list_or_tuple(var):
	return isinstance(var, list) or isinstance(var, tuple)

def list_re(li, fn):
	for i in range(len(li)):
		li[i] = fn(li[i])

def getif(data, name):
	return data.get(name, None)

def popif(data, key):
	return data.pop(key, None)

# 更新dict全部或指定字段
# dst: 模板dict, src: 来源dict
def puts(dst, src, keys = None):
	for key in keys or src:
		dst[key] = src[key]

# 依次测试keys中的key，返回第一个存在的或者None
# def gets_or(data, keys):
# 	for key in keys:
# 		if key in data:
# 			return data[key]
# 	return None

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

	__puts__ = puts

# data = Dict({'a': 1})
# print(data.a) # get 1
class Dict:
	__slots__ = ('__dict__')

	def __init__(self, obj = None):
		if obj:
			object.__setattr__(self, '__dict__', obj)

	def __getattr__(self, name):
		return self.__dict__.get(name, getattr(self.__dict__, name, None))

	def __setattr__(self, name, value):
		self.__dict__[name] = value

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

	getif = getif
	popif = popif
	puts = puts

# add_method_proxy(Dict, '__dict__', ['__str__', '__iter__', '__getitem__', '__setitem__'])

# 接收字典列表
# datas = Dict([{'a': 1}, {'a': 2}])
# for data in datas:
#     print(data.a)
class Dicts:
	__slots__ = ('__ref', 'data')

	def __init__(self, array):
		if is_list_or_tuple(array):
			self.__ref = None
			self.data = array
		else:
			raise TypeError('array must be a list or tuple')

	def __iter__(self):
		if not self.__ref:
			self.__ref = Dict()
		
		for item in self.data:
			self.__ref.__init__(item)
			yield self.__ref