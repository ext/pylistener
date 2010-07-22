#/usr/bin/python
# -*- coding: utf-8 -*-

from listener import Listen
from decorator import event, interface

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
