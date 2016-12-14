from utils.thread import newthread
import request

def wrapper(fn):
	@newthread
	def _deco(host, *args, **keyArgs):
		try:
			an.echo(fn(an.host + host, *args, **keyArgs))
		except Exception as e:
			an.echo(e)
	return _deco

an.api_get = wrapper(request.get)
an.api_post = wrapper(request.post)
