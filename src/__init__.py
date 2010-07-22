#/usr/bin/python

import types, weakref

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
        for x in cls._listener:
            # search for the function in the derived class
            f = getattr(x(), func.__name__)

            # if func isn't implemented in the derived class the original func
            # is bound and called.
            if f.__name__ is 'wrapper':
                f = types.MethodType(func, x(), x().__class__)

            # finally, call the function
            f(*args, **kwargs)

if __name__ == '__main__':

    @interface
    class ListenA (Listen):
        @event
        def trigger(self, *args, **kwargs):
            print 'ListenA::trigger', self.a
            
        @event
        def foo(self):
            print 'ListenA::foo', self
            
    @interface
    class ListenB (Listen):
        @event
        def fred(self, a, b, c):
            print 'ListenB::fred', a, b, c

    class ConcreteA (ListenA):
        def __init__(self, value):
            ListenA.__init__(self)
            self.a = value
            
        def trigger(self, *args, **kwargs):
            print 'ConcreteA::trigger', self.a

    class ConcreteB (ListenB):
        def fred(self, a,b,c):
            print 'ConcreteB::fred', a,b,c

    class ConcreteB2 (ConcreteB):
        def fred(self, a,b,c):
            print 'ConcreteB2::fred', a,b,c

    class ConcreteAB(ConcreteA, ConcreteB):
        def __init__(self, value):
            ConcreteA.__init__(self, value)
            ConcreteB.__init__(self)

        def trigger(self, *args, **kwargs):
            print 'ConcreteAB::trigger', self.a

        def fred(self, a,b,c):
            print 'ConcreteAB::fred', a,b,c


    a = ConcreteA(1)
    d = ConcreteAB(2)

    ListenA.trigger(1, 2, foo=3)
    ListenB.fred(1, 2, c=3)
    
    del a

    ListenA.trigger(1, 2, foo=3)
