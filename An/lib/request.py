from urllib import request
from urllib.parse import urlencode

def do_request(url, isGet = True, headers=None, data=None, encoding="UTF-8"):
	if data:
		postdata = urlencode(data, encoding=encoding)
		if isGet:
			url = url + '?' + postdata
			postdata = None
		else:
			postdata = postdata.encode()
	else:
		postdata = None if isGet else b''
	opener = request.build_opener()
	if headers:
		opener.addheaders = [(k, headers[k]) for k in headers];
	result = opener.open(url, postdata)
	the_page = result.read()
	result.close()
	return the_page.decode(encoding)

def get(*args, **keyargs):
	return do_request(*args, **keyargs)

def post(*args, **keyargs):
	keyargs['isGet'] = False
	return do_request(*args, **keyargs)