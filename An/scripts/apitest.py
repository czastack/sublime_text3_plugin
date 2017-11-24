from utils.thread import newthread
from An import an
import requester

def wrapper(fn):
    @newthread
    def _deco(url, *args, **keyArgs):
        try:
            if an.urlpre:
                url = an.host + url
            result = fn(url, *args, **keyArgs)
            result = result.encode().decode('unicode_escape')
            an.echo(url, result)
        except Exception as e:
            an.echo(e)
    return _deco

an.api_get = wrapper(requester.get)
an.api_post = wrapper(requester.post)
