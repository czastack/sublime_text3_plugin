import request, os, threading
from functools import partial
class Runner(threading.Thread):
	def __init__(self, method, host, headers=None, data=None):
		super(Runner, self).__init__()
		self.host = an.host + host
		self.method = method
		self.headers = headers
		self.data = data

	def run(self):
		an.tout()
		method = self.method
		try:
			an.echo(method(self.host, headers = self.headers, data = self.data))
		except Exception as e:
			an.echo(e)

def wrapper(callee):
	def fn(*args, **keyArgs):
		Runner(callee, *args, **keyArgs).start()
	return fn
an.api_get = wrapper(request.get)
an.api_post = wrapper(request.post)
