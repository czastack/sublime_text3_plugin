from utils.thread import newthread
import request

def wrapper(fn):
    @newthread
    def _deco(host, *args, **keyArgs):
        try:
            result = fn(an.host + host, *args, **keyArgs)
            result = result.encode().decode('unicode_escape')
            an.echo(result)
        except Exception as e:
            an.echo(e)
    return _deco

an.api_get = wrapper(request.get)
an.api_post = wrapper(request.post)
