from utils.thread import newthread
from An import an
import requester


def wrapper(fn):
    @newthread
    def _deco(url, *args, **kwargs):
        try:
            if an.urlpre:
                url = an.host + url
            jsonzh = kwargs.pop('jsonzh', False)
            logurl = kwargs.pop('logurl', False)
            result = fn(url, *args, **kwargs)
            if jsonzh:
                if isinstance(result, str):
                    result = result.encode()
                result = result.decode('unicode_escape')
            if logurl:
                an.echo(url, end=" ")
            an.echo(result)
        except Exception as e:
            an.echo(e)
    return _deco


an.api_get = wrapper(requester.get)
an.api_post = wrapper(requester.post)
