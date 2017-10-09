from functools import partial


def bind(fn, ins):
    return fn.__get__(ins, ins.__class__)

def binds(fn, ins, *args, **kwargs):
    fn = bind(fn, ins)
    if args or kwargs:
        return partial(fn, *args, **kwargs)
