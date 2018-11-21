from urllib import request
from urllib.parse import urlencode, quote


def do_request(url, data=None, headers={}, isget=True, encoding="UTF-8"):
    if data:
        if isinstance(data, str):
            data = data.encode(encoding=encoding)
        else:
            data = urlencode(data, encoding=encoding)
            if isget:
                url = url + ('&' if '?' in url else '?') + data
                data = None
            else:
                data = data.encode(encoding=encoding)
    else:
        data = None if isget else b''
    opener = request.build_opener()
    req = request.Request(url=url, data=data, headers=headers)
    result = opener.open(req)
    content = result.read()
    result.close()
    try:
        content = content.decode(encoding)
    except Exception:
        pass
    return content


def get(*args, **keyargs):
    return do_request(*args, **keyargs)


def post(*args, **keyargs):
    keyargs['isget'] = False
    return do_request(*args, **keyargs)
