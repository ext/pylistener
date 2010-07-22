#/usr/bin/python
# -*- coding: utf-8 -*-

import types, weakref

class Listen:
    cls = {}
    listeners = {}

    def __init__(self):
        for cls in Listen.find_observable(Listen, self.__class__):
            # don't add twice, may happen when using multiple inheritance
            if self in [x() for x in cls._listener]:
                return
            
            cls._listener.append(weakref.ref(self))

    def __del__(self):
        for cls in Listen.find_observable(Listen, self.__class__):
            cls._listener = [x for x in cls._listener if x() is not None]

    @staticmethod
    def find_observable(needle, cls):
        if cls is None:
            return
        
        if needle in cls.__bases__:
            yield cls

        for x in cls.__bases__:
            for y in Listen.find_observable(needle, x):
                yield y

        return
    
    @staticmethod
    def _register_class(cls):
        Listen.cls[cls] = cls.__name__

    @staticmethod # fake classmethod =)
    def _trigger(cls, func, args, kwargs):
        def bind(inst, func):
            # search for the function in the derived class
            f = getattr(inst, func.__name__)

            # if func isn't implemented in the derived class the original func
            # is bound and called.
            if f.__name__ is 'wrapper':
                f = types.MethodType(func, inst, inst.__class__)

            return f

        for x in cls._listener:
            f = bind(x(), func)

            # finally, call the function
            f(*args, **kwargs)
