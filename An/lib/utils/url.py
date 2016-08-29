from urllib import parse
def urldecode(url):
	"""
	解析url参数字符串
	:returns dict
	"""
	parsed = parse.unquote(url)
	data = {}
	for item in parsed.split('&'):
		key, value = item.split('=')
		data[key] = value
	return data