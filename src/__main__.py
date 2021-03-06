from listener import Listen
from decorator import event, interface

@interface
class SampleListener(Listen):
    @event
    def foo(self,a,b,c):
        raise NotImplementedError

class Sample(SampleListener):
    def foo(self,a,b,c):
        print a,b,c

a = Sample()
SampleListener.foo(1,2,c=3)
