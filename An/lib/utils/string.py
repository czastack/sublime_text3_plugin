import re

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


def str2codes(s):
	return [ord(ch) for ch in s]


def codes2str(cs):
	return ''.join(chr(c) for c in cs)


def matchAll(reg, text, fn):
	if isinstance(fn, (list, tuple)):
		arg = fn
		fn = lambda x: [x.group(i) for i in arg]

	elif isinstance(fn, int):
		arg = fn
		fn = lambda x: x.group(arg)

	return [fn(m) for m in re.finditer(reg, text)]


def replace(s, rulers):
	"""字符串批量替换"""
	for patterm, rep in rulers:
		s = re.sub(patterm, rep, s)
	return s
