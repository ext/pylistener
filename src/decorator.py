#/usr/bin/python
# -*- coding: utf-8 -*-

from listener import Listen

def event(func):
    def wrapper(cls, *args, **kwargs):
        return cls._trigger(func, args, kwargs)
    return classmethod(wrapper)

def interface(cls):
    def trigger(func, args, kwargs):
        return Listen._trigger(cls, func, args, kwargs)
    Listen._register_class(cls)
    cls._listener = []
    cls._trigger = staticmethod(trigger)
    return cls
