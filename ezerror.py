
class EZException(Exception):
    '''
    >>> EZException('hello')
    EZException: hello
    
    >>> try:
    ...     1 / 0
    ... except Exception as exc:
    ...     print(repr(EZException.fromException(exc)))
    EZZeroDivisionError: division by zero
    '''
    
    format = '{my.info}' 
    defargs = ('info',)
    info = None
    
    def __init__(self, *_, info=None, **_kw):
        self.info = _ if info is None else info
        for name, value in zip(self.defargs, _):
            setattr(self, name, value)
        self.__dict__.update(_kw)
        
    def __str__(self):
        format = self.format
        while True:
            replace = format.format(my=self)
            if replace == format:
                break
            else:
                format = replace
        return replace
        
    def __repr__(self):
        return '%s: %s' % (type(self).__name__, self)
       
    pytypes = {}        
        
    @classmethod
    def registerPyType(cls, pytype, **_kw):
        fiierrtype = type('EZ' + pytype.__name__, (cls, pytype), {})
        cls.pytypes[id(pytype)] = (fiierrtype, _kw)
        return fiierrtype
        
    @classmethod
    def fromException(cls, exc, default=TypeError):
        translation = cls.pytypes.get(id(type(exc)))
        if translation is None:
            if isinstance(default, Exception):
                raise default('Cannot get EZException from %r' % exc)
            else:
                return default
        else:            
            fiitype, kw = translation
            kwargs = {}
            for fii_name, src_name in kw:
                kwargs[fii_name] = getattr(exc, src_name, None)
            return fiitype(info=str(exc), **kwargs)                

EZTypeError = EZException.registerPyType(TypeError)
EZZeroDivisionError = EZException.registerPyType(ZeroDivisionError)

