
def bind(fn, ins):
    return fn.__get__(ins, ins.__class__)
