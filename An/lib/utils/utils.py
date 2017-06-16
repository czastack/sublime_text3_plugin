
def lazyproperty(func):
    def _deco(self):
        name = '_' + func.__name__
        val = getattr(self, name, None)
        if val is None:
            val = func(self)
            setattr(self, name, val)
        return val
    return property(_deco)


def lazyclassproperty(func):
    def _deco(self):
        name = '_' + func.__name__
        val = getattr(self.__class__, name, None)
        if val is None:
            val = func(self)
            setattr(self.__class__, name, val)
        return val
    return property(_deco)